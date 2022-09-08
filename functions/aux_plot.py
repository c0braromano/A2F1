# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 16:00:16 2022

@author: roman
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from functions.helper import agrupamento_dia_maquina

def plot(df_defeitos, title_list):
    
    defeitos_agrupados = agrupamento_dia_maquina(df_defeitos)
    
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(16, 9))
    sns.barplot(x='DATA', y='VALOR', hue='MAQUINA', data=defeitos_agrupados)
    plt.xticks(rotation=45)
    plt.title(f"{title_list[0]}")
    fig.savefig(f'plots/{title_list[0]}.png', bbox_inches='tight', dpi=100)
    plt.show()
    
    explode = (0.05, 0.05)
    a = defeitos_agrupados.groupby('MAQUINA').sum()
    
    fig = plt.figure(figsize=(16, 9))
    
    plt.pie(a['VALOR'].values, labels=list(a.index),
            autopct='%1.1f%%', pctdistance=0.85,
            explode=explode)
    
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title(f"{title_list[1]}")
    fig.savefig(f'plots/{title_list[1]}.png', bbox_inches='tight', dpi=100)
    plt.show()

