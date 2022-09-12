# -*- coding: utf-8 -*-
"""
Created on Sun Apr  17 15:43:20 2022

@author: romano
"""

import zipfile
import os
import pandas as pd
import cx_Oracle


def get_data(path):
    dict_dataframes = {}
    return_df = pd.DataFrame()
    #iterar arquivos excel
    for excel_file in os.listdir(f'{path}'):
        excel = pd.ExcelFile(f'{path}/{excel_file}')
        df = pd.read_excel(f'{path}/{excel_file}')
        df.set_index('Date', inplace=True, drop=True)
        #iterar tabelas do excel
        for sheet in excel.sheet_names[1:]:
            df_sheet = pd.read_excel(f'{path}/{excel_file}', sheet_name=sheet)
            df_sheet.set_index('Date', inplace=True, drop=True)
            print(excel_file)
            try:
                df = pd.concat([df, df_sheet], axis=1)
            except:
                df = df.join(df_sheet, how='outer')

        return_df = pd.concat([return_df, df])

    return return_df

def sort_index(dict_frames):
    for key, dataframe in dict_frames.items():
        dataframe.sort_index(inplace=True)


class oracle_fiap:
    
    def __init__(self, user, password):
        self.dsn = cx_Oracle.makedsn("oracle.fiap.com.br", 1521, service_name="orcl.fiap.com.br")
        
        self.con= cx_Oracle.connect(
                user=user,
                password=password,
                dsn=self.dsn
                )
        
        self.cur = self.con.cursor()
        
    def get_data(self):
        
        self.cur.execute("""
                         select  cd_empresa,nm_fantasia,cd_maquina, 
                         nm_maquina, nr_serie_maquina, nr_ano_fabricacao,
                         ds_voltagem 
                         from pf0110.v_dados_cli_maq_jkcontrol 
                         where cd_empresa = 8 order by cd_maquina
                         """)
        
        
        ### pesquisar comando para extrair nome das colunas direto do oracle
        columns =  ['cd_empresa','Empresa','Nome máquina', 
        'Tipo máquina', 'N série', 'Ano fabricação',
        'Voltagem']
        
        df = pd.DataFrame(self.cur.fetchall(), columns=columns)
        
    
        return df
    
    def insert_data(self, data):
        
        def make_queries(columns):
            query = '('
            for column in columns:
                if column != columns[-1]:
                    query = f'{query}:{column}, '
                else:
                    query = f'{query}:{column}'
            
            query = f'{query})'
            
            return query
        
        for tabela, df in data.items():
            uniques = df.drop_duplicates()
            query = f'INSERT INTO {tabela} VALUES {make_queries(uniques.columns)}'
            exec_list = []
            for index, row in uniques.iterrows():
                query_content = []
                for element in row:
                    query_content.append(element)
                
                exec_list.append(query_content)
            
            try:
                self.cur.executemany(query, exec_list)
            except cx_Oracle.IntegrityError as e:
                error_obj, = e.args
                if error_obj.code == 1:
                    print(error_obj.message)
                    continue
                else:
                    raise(error_obj.message)

            self.con.commit()
            
        return None


def transform_plantas(plantas):
    new_df = pd.DataFrame(columns=['DATA', 'ACAO', 'MAQUINA', 'VALOR'])
    for column in plantas.columns:
        notnull = plantas[column][plantas[column].notna()]
        new_df2 = pd.DataFrame({'DATA':notnull.index,
                                'CD_MAQUINA' : column,
                                'VALOR' : notnull.values})
        new_df = pd.concat([new_df, new_df2])
        
        new_df.sort_values(by='DATA', inplace=True)
        new_df['ACAO'] = new_df['CD_MAQUINA'].apply(lambda x: x.split(' ')[0])
        new_df['MAQUINA'] = new_df['CD_MAQUINA'].apply(
            lambda x: x.split(' ')[1][1:] + ' ' +  x.split(' ')[2][:-1]
            )
        
    new_df.drop(columns=['CD_MAQUINA'], inplace=True)

    return new_df

def agrupamento_dia_maquina(df_defeitos):
    df_defeitos['DATA'] = pd.to_datetime(df_defeitos['DATA'])
    df_defeitos.set_index('DATA', inplace=True)
    defeitos_agrupados = df_defeitos.groupby([pd.Grouper(freq='D'), 'MAQUINA']).sum()
    defeitos_agrupados.reset_index(inplace=True)
    defeitos_agrupados['DATA'] = defeitos_agrupados['DATA'].dt.date
    
    return defeitos_agrupados


def build_tempo_parada(df_parada):
    df_tempo_parada = pd.DataFrame(columns=['MAQUINA', 'TEMPO'])
    df_parada['DATA'] = pd.to_datetime(df_parada['DATA'])
    for index, row in df_parada.iterrows():
        if row['VALOR'] == 0:
            inicio = row['DATA']
        if row['VALOR'] == 1:
            fim = row['DATA']
            delta_tempo = fim - inicio
            minutos = delta_tempo.total_seconds()
            df_tempo_parada.loc[len(df_tempo_parada)] = [row['MAQUINA'], minutos]
    
    return df_tempo_parada

def rmv_outliers(df_tempo_parada, valor):
    q1 = df_tempo_parada[valor].quantile(0.25)
    q3 = df_tempo_parada[valor].quantile(0.75)
    iqr = q3 - q1
    
    filtro = (df_tempo_parada[valor] >= q1 - 1.5*iqr) & (df_tempo_parada[valor] <= q3 + 1.5*iqr)
    
    return df_tempo_parada.loc[filtro]

def add_motivo(df_cod_maq):
    df_cod_maq['rfid_value'] = df_cod_maq['rfid_value'].astype(int)
    def convert_code(code):
        dict_conversion = {
            1 : 'Falta de energia',
            2 : 'Falta operador',
            3 : 'Falta MP',
            5 : 'Set-up',
            6 : 'Ajuste Maquina',
            7 : 'Limpeza canhão',
            8 : 'Limpeza maquina',
            10 : 'Refeição',
            13 : 'Manutenção ferramentaria',
            15 : 'Manutenção máquina',
            17 : 'Aquecimento máquina',
            22 : 'Teste material',
            24 : 'Manutenção preventiva',
            25 : 'Try Out Molde',
            34 : 'Abastecimento',
            35 : 'Parada Programada'
            }
        try:
            conversion = dict_conversion[code]
        except KeyError:
            return 'Desconhecido'
    
        return conversion
    
    df_cod_maq['MOTIVO_PARADA'] = df_cod_maq['rfid_value'].apply(lambda value: convert_code(value))
    
def df_to_list(df):
    return_list = [list(df.columns)]
    
    for index, row in df.iterrows():
        return_list.append(list(row))
    
    return return_list
    

    