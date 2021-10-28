# ------------------------------- Configuração ------------------------------- #
# Importar bibliotecas
import numpy as np
import pandas as pd
import random as rd
import matplotlib.pyplot as plt

from source import *
from settings import *

# Determinar a seed do RNG
rng = np.random.default_rng(SEED)



# --------------------------------- Simulação -------------------------------- #

def build_parameters(NUM_JOBS=NUM_JOBS, MEAN_ARRIVAL_RATE=MEAN_ARRIVAL_RATE, MEAN_SERVICE_RATE=MEAN_SERVICE_RATE):
    '''
    Calcula e retorna dicionário contendo os parâmetros de simulação.
    '''
    
    parameters = {
        'NUM_JOBS': NUM_JOBS,
        'MEAN_ARRIVAL_RATE': MEAN_ARRIVAL_RATE,
        'MEAN_SERVICE_RATE': MEAN_SERVICE_RATE,
        'MEAN_INTERARRIVAL_TIME': 1.0 / MEAN_ARRIVAL_RATE,
        'MEAN_SERVICE_TIME': 1.0 / MEAN_SERVICE_RATE,
        'NUM_BINS': int(NUM_JOBS / MEAN_ARRIVAL_RATE)
    }
    
    return parameters


def run_sim_and_plot(NUM_JOBS=NUM_JOBS, MEAN_ARRIVAL_RATE=MEAN_ARRIVAL_RATE, MEAN_SERVICE_RATE=MEAN_SERVICE_RATE):
    '''
    Executa a simulação (run_sim) e plota os resultados (plot_results).
    '''
    
    parameters = build_parameters(NUM_JOBS, MEAN_ARRIVAL_RATE, MEAN_SERVICE_RATE)
    #TODO Function: Print simulation details
    result = run_sim(parameters)
    #TODO Function: Dump Stats
    #TODO Function: Plot Result
    


def run_sim(parameters):
    '''
    Executa a simulação e retorna resultados.
    '''
    
    # Parâmetros de simulação
    NUM_JOBS = parameters['NUM_JOBS']
    MEAN_INTERARRIVAL_TIME = parameters['MEAN_INTERARRIVAL_TIME']
    MEAN_SERVICE_TIME = parameters['MEAN_SERVICE_TIME']
    
    # Dados e Resultados ???????
    ## Exponential
    interrarival_times = rng.exponential(scale=MEAN_INTERARRIVAL_TIME, size=NUM_JOBS)
    arrival_times = np.cumsum(interrarival_times)
    service_times = rng.exponential(scale=MEAN_SERVICE_TIME, size=NUM_JOBS)
    
    ## Criação de dataframes de tarefas e eventos
    df_jobs = build_jobs_df(parameters, interrarival_times, arrival_times, service_times)
    #df_events = build_events_df(parameters, df_jobs)
    #total_width = get_total_width(df_jobs)
    
    
    
    


def build_jobs_df(parameters, interrarival_times, arrival_times, service_times):
    '''
    Cria um dataframe para armazenar detalhes das tarefas.
    '''
    
    # Cria dataframe de tarefas    
    df_jobs = pd.DataFrame({
        'interarrival_time': interrarival_times,
        'arrive_time': arrival_times,
        'service_time': service_times,
        'start_time': np.zeros(parameters['NUM_JOBS']),
        'depart_time': np.zeros(parameters['NUM_JOBS'])
    })

    # Preenche tempos de chegada e partida
    df_jobs.loc[0, 'start_time'] = df_jobs.loc[0, 'arrive_time']
    df_jobs.loc[0, 'depart_time'] = df_jobs.loc[0, 'arrive_time'] + df_jobs.loc[0, 'service_time']
    
    for i in range(1, parameters['NUM_JOBS']):
        # O processo inicia no momento de chegada (arrive_time) se o processo anterior estiver finalizado
        df_jobs.loc[i, 'start_time'] = max(df_jobs.loc[i, 'arrive_time'], df_jobs.loc[i-1, 'depart_time'])
        df_jobs.loc[i, 'depart_time'] = df_jobs.loc[i, 'start_time'] + df_jobs.loc[i, 'service_time']
        
    # Adiciona coluna com tempo de resposta (depart time - arrive time)
    df_jobs['response_time'] = df_jobs['depart_time'] - df_jobs['arrive_time']
    
    # Adiciona coluna com tempo de espera (start time - arrive time)
    df_jobs['wait_time'] = df_jobs['start_time'] - df_jobs['arrive_time']
    
    return df_jobs
    

def build_events_df():
    '''
    Cria um dataframe para armazenar detalhes dos eventos.
    '''
    pass


def get_total_width(df_jobs):
    '''
    ?
    '''
    pass


