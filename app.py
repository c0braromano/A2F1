# -*- coding: utf-8 -*-
"""
Created on Sun Apr  17 15:47:37 2022

@author: romano
"""

import pandas as pd
import ast

from functions.helper import get_data, oracle_fiap, build_tempo_parada
from functions.helper import transform_plantas, rmv_outliers, add_motivo
from functions.helper import df_to_list
from functions.aux_plot import plot, plot_prd_dist, plot_violin, count_plot
from functions.build_pdf import build_pdf
from datetime import datetime


instancia_fiap = oracle_fiap('rm92629', '050396')
info_orcl = instancia_fiap.get_data()
info_orcl.drop_duplicates('N série', inplace=True)
info_orcl.drop(columns=['cd_empresa'], inplace=True)
tab_maquinas = df_to_list(info_orcl)

inicio = datetime.now()

plantas = get_data('data/plantas')

maquina_01 = pd.read_csv(
    'data/maquina_01_device_rfid_variable_Gs5M.csv', 
    )

print(f'leitura de xlsx {datetime.now() - inicio}')


maquina_01['rfid_type'] = maquina_01['context_rfid'].apply(lambda x: list(ast.literal_eval(x).keys())[0])
maquina_01['rfid_value'] = maquina_01['context_rfid'].apply(lambda x: list(ast.literal_eval(x).values())[0])
maquina_01.drop(columns=['context_rfid', 'rfid'], inplace=True)
df_cod_maq = maquina_01[maquina_01['rfid_type'] == 'cod_maq']
add_motivo(df_cod_maq)

df_cod_prd = maquina_01[maquina_01['rfid_type'].isin(['cod_pdr', 'cod_prd'])]
tab_pecas = df_to_list(pd.DataFrame(df_cod_prd['rfid_value'].unique(), columns=['Peças produzidas']))

plantas.sort_index(inplace=True)
df_plantas = transform_plantas(plantas)

df_ciclo = df_plantas[df_plantas['ACAO'] == 'ciclo']
df_ciclo_wout = rmv_outliers(df_ciclo, 'VALOR')
df_ciclo_wout['VALOR'] = df_ciclo_wout['VALOR'].astype(int)

df_defeitos = df_plantas[df_plantas['ACAO'] == 'peca_defeito']

df_injecao = df_plantas[df_plantas['ACAO'] == 'injecao']

df_parada = df_plantas[(df_plantas['ACAO'] == 'parada')]
df_tempo_parada = build_tempo_parada(df_parada)
df_tmp = rmv_outliers(df_tempo_parada, 'TEMPO')

plot(df_defeitos, ["Defeitos diários por máquina", 'Defeitos Totais por máquina'])
plot(df_injecao, ["Produção diária por máquina", "Produção total por máquina"])
plot(df_parada[df_parada['VALOR'] == 1], ["Paradas diárias por máquina", "Paradas totais por máquina"])
plot_violin(df_tempo_parada, 'TEMPO', 'Tempo de parada')
plot_violin(df_ciclo_wout, 'VALOR', 'Tempo de ciclo')
plot_prd_dist(df_tmp)
count_plot(df_cod_maq, 'MOTIVO_PARADA')

build_pdf(tab_maquinas, tab_pecas)


print(datetime.now() - inicio)
