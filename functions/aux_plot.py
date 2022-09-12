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
    plt.legend(loc=2, prop={'size': 20})
    plt.tick_params(axis='both', labelsize=20)
    fig.savefig(f'plots/{title_list[0]}.png', bbox_inches='tight', dpi=100)
    plt.show()
    
    explode = (0.05, 0.05)
    a = defeitos_agrupados.groupby('MAQUINA').sum()
    
    fig = plt.figure(figsize=(16, 9))
    
    patches, texts, autotexts = plt.pie(a['VALOR'].values, labels=list(a.index),
            autopct='%1.1f%%', pctdistance=0.85,
            explode=explode)
    for text in texts:
        text.set_fontsize(30)
    
    for text in autotexts:
        text.set_fontsize(20)
        
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    fig.savefig(f'plots/{title_list[1]}.png', bbox_inches='tight', dpi=100)
    plt.show()

def plot_prd_dist(df_tmp):
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(18, 9))
    sns.displot(data=df_tmp, x='TEMPO', hue='MAQUINA', kde=True, element='step')
    plt.xlabel('Tempo (segundos)')
    
    plt.savefig('plots/dist.png', bbox_inches='tight', dpi=150)
    

def plot_violin(df, value, titulo):
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(16, 9))
    sns.catplot(data=df, x='MAQUINA', y=value, kind='violin')
    plt.savefig(f'plots/{titulo}_violin.png', bbox_inches='tight', dpi=100)
    
def count_plot(df_cod_maq, value):
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(18, 9))
    sns.countplot(data=df_cod_maq, x=value)
    plt.xticks(rotation=45)
    plt.tick_params(axis='both', labelsize=20)
    fig.savefig(f'plots/count_motivos.png', bbox_inches='tight', dpi=200)
    plt.show()


