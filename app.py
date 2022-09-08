# -*- coding: utf-8 -*-
"""
Created on Sun Apr  17 15:47:37 2022

@author: romano
"""

import pandas as pd
import ast

from functions.helper import get_data, oracle_fiap
from functions.helper import transform_plantas
from functions.aux_plot import plot
from datetime import datetime


instancia_fiap = oracle_fiap('rm92629', '050396')
info_orcl = instancia_fiap.get_data()

inicio = datetime.now()

plantas = get_data('data/plantas')

maquina_01 = pd.read_csv(
    'data/maquina_01_device_rfid_variable_Gs5M.csv', 
    )

maquina_01['rfid_type'] = maquina_01['context_rfid'].apply(lambda x: list(ast.literal_eval(x).keys())[0])
maquina_01['rfid_value'] = maquina_01['context_rfid'].apply(lambda x: list(ast.literal_eval(x).values())[0])
maquina_01.drop(columns=['context_rfid', 'rfid'], inplace=True)

print(f'leitura de xlsx {datetime.now() - inicio}')

plantas.sort_index(inplace=True)

df_plantas = transform_plantas(plantas)
df_defeitos = df_plantas[df_plantas['ACAO'] == 'peca_defeito']
df_injecao = df_plantas[df_plantas['ACAO'] == 'injecao']

plot(df_defeitos, ["Defeitos diários por máquina", 'Defeitos Totais por máquina'])
plot(df_injecao, ["Produção diária por máquina", "Produção total por máquina"])


print(datetime.now() - inicio)
