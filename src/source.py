# ------------------------------- Configuração ------------------------------- #
# Importar bibliotecas
from IPython.core.display import display
import numpy as np
import pandas as pd
import random as rd
import matplotlib.pyplot as plt
from IPython.display import Markdown

from src.plotting import *
from src.settings import *

# Determinar a seed do RNG
rng = np.random.default_rng(SEED)



# --------------------------------- Simulação -------------------------------- #

def run_sim_and_plot(parameters=parameters):
    '''
    Executa a simulação (run_sim) e plota os resultados (plot_results).
    '''
    print_title(parameters)
    results = run_sim(parameters)
    print_results(results)
    plot_result(results)   
    
    return results


def run_sim(parameters):
    '''
    Executa a simulação e retorna resultados.
    '''    
    # Computar dados de Simulação e Resultados 
    interrarival_times, service_times, arrival_times, event_types = generate_times(parameters)
    
    ## Criação de dataframes de tarefas e eventos
    df_jobs = build_jobs_df(parameters, interrarival_times, arrival_times, service_times, event_types)
    df_events = build_events_df(parameters, df_jobs)
    
    return get_result(parameters, df_jobs, df_events)
    

def generate_from_distribution(rng, scale, distribution, constant=0):
    if distribution == 'exponential':
        return rng.exponential(scale=scale)
    elif distribution == 'triangular':
        return rng.triangular(0, scale, scale*10)
    elif distribution == 'normal':
        return rng.normal(scale, scale/10)
    elif distribution == 'uniform':
        return rng.uniform(0, scale*2)
    elif distribution == 'constant':
        return constant


def generate_times(parameters):
    # Parâmetros de simulação
    NUM_JOBS = parameters['NUM_JOBS']
    MEAN_INTERARRIVAL_TIME = parameters['MEAN_INTERARRIVAL_TIME']
    MEAN_SERVICE_TIME = parameters['MEAN_SERVICE_TIME']
    EVENT_TYPES = parameters['EVENT_TYPES']
    EVENT_WEIGHTS = parameters['EVENT_WEIGHTS']
    DISTRIBUTION = parameters['DISTRIBUTION']
    
    interrarival_times = []
    service_times = []
    
    event_types = [np.random.choice(EVENT_TYPES, 1, p=EVENT_WEIGHTS)[0] for i in range(NUM_JOBS)]
    for i in range(NUM_JOBS):
        if event_types[i] == '1':
            # Evento 1: Atendimento ocorro normalmente.
            interrarival_times.append( generate_from_distribution(rng, scale=MEAN_INTERARRIVAL_TIME, distribution='exponential') )
            service_times.append( generate_from_distribution(rng, scale=MEAN_SERVICE_TIME, distribution=DISTRIBUTION) )
            
        elif event_types[i] == '2':
            # Evento 2: Caso de imprevisto, atendimento leva um tempo de 5 a 10x maior.
            delay = np.random.rand() * (8-3) + 3
            interrarival_times.append( generate_from_distribution(rng, scale=MEAN_INTERARRIVAL_TIME, distribution='exponential') )
            service_times.append( generate_from_distribution(rng, scale=MEAN_SERVICE_TIME, distribution=DISTRIBUTION)*delay )
        
        elif event_types[i] =='3':
            # Evento 3: Não é possível realizar atendimento, tempo de serviço = 0.
            delay = np.random.rand() * (10-5) + 5
            interrarival_times.append( generate_from_distribution(rng, scale=MEAN_INTERARRIVAL_TIME, distribution='exponential') )
            service_times.append( generate_from_distribution(rng, scale=MEAN_SERVICE_TIME, distribution=DISTRIBUTION)/delay )
    
    
    arrival_times = np.cumsum(interrarival_times)   
    
    return interrarival_times, service_times, arrival_times, event_types


def build_jobs_df(parameters, interrarival_times, arrival_times, service_times, event_types):
    '''
    Cria um dataframe para armazenar detalhes das tarefas.
    '''
    
    # Cria dataframe de tarefas    
    df_jobs = pd.DataFrame({
        'interarrival_time': interrarival_times,
        'arrive_time': arrival_times,
        'service_time': service_times,
        'start_time': np.zeros(parameters['NUM_JOBS']),
        'depart_time': np.zeros(parameters['NUM_JOBS']),
        'event_type': event_types
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
    

def build_events_df(parameters, df_jobs):
    '''
    Cria um dataframe para armazenar detalhes dos eventos.
    '''
    NUM_JOBS = parameters['NUM_JOBS']
    arrivals = df_jobs['arrive_time']
    starts = df_jobs['start_time']
    departures = df_jobs['depart_time']
    event_types = df_jobs['event_type']
    
    # Width = up_bd - lo_bd
    # jobs_in_qeue = jobs_in_system - 1
        
    df_events = pd.DataFrame(columns=['event_type', 'lo_bd', 'up_bd', 'width',
                                      'jobs_in_system', 'jobs_in_queue'])
    
    lo_bd = 0
    arrive_idx = 0
    start_idx = 0
    depart_idx = 0
    jobs_in_system = 0
    jobs_in_queue = 0
    
    while depart_idx < NUM_JOBS:
        # Armazena chegada, inicio e saida da tarefa atual
        arrival = arrivals[arrive_idx] if arrive_idx < NUM_JOBS else float('inf')
        start = starts[start_idx] if start_idx < NUM_JOBS else float('inf')
        departure = departures[depart_idx]
        type = event_types[depart_idx]
        
        # Controla fluxo de chegadas, partidas e fila
        if arrival <= start and arrival <= departure:
            up_bd = arrival
            n_change, nq_change = 1, 1
            arrive_idx += 1
            
        elif start <= arrival and start <= departure:
            up_bd = start 
            n_change, nq_change = 0, -1
            start_idx += 1
            
        else: 
            up_bd = departure
            n_change, nq_change = -1, 0
            depart_idx += 1

        width = up_bd - lo_bd
            
        # Adiciona dados no dataframe de eventos
        df_events = df_events.append({
            'event_type': type,
            'lo_bd': lo_bd,
            'up_bd': up_bd,
            'width': width,
            'jobs_in_system': jobs_in_system,
            'jobs_in_queue': jobs_in_queue,
            'jobs_in_system_change': n_change,
            'jobs_in_queue_change': nq_change,
        }, ignore_index=True)
        
        # Atualiza o numero de itens no sistema e na fila
        jobs_in_system += n_change
        jobs_in_queue += nq_change
        
        lo_bd = up_bd
        
    return df_events


def get_total_width(df_jobs):
    return df_jobs.iloc[-1]['depart_time'] - df_jobs.iloc[0]['arrive_time']


def estimate_utilization(df_jobs):
    busy = (df_jobs['depart_time'] - df_jobs['start_time']).sum()
    return busy / get_total_width(df_jobs)


def get_result(parameters, df_jobs, df_events):
    
    sim_mean_interarrival_time = df_jobs['interarrival_time'].mean()
    sim_mean_arrival_rate = 1.0 / sim_mean_interarrival_time
    sim_mean_service_time = df_jobs['service_time'].mean()
    sim_mean_service_rate = 1.0 / sim_mean_service_time
    sim_mean_wait_time = df_jobs['wait_time'].mean()
    sim_response_time_mean = df_jobs['response_time'].mean()
    sim_response_time_var = df_jobs['response_time'].var()
    
    width = df_events['width']
    total_weighted_num_jobs_in_system = (width * df_events['jobs_in_system']).sum()
    total_weighted_num_jobs_in_queue  = (width * df_events['jobs_in_queue']).sum()
    sim_mean_jobs_in_system = total_weighted_num_jobs_in_system / get_total_width(df_jobs)
    sim_mean_jobs_in_queue  = total_weighted_num_jobs_in_queue / get_total_width(df_jobs)
    
    departures = df_events.loc[df_events['jobs_in_system_change'] == -1.0, 'lo_bd']
    hist, _ = np.histogram(departures, bins=int(get_total_width(df_jobs)) + 1)
    sim_throughput_mean = np.mean(hist)
    utilization = estimate_utilization(df_jobs)    
    
    results = {
        'parameters': parameters,
        'jobs': df_jobs,
        'events': df_events,
        'total_duration': get_total_width(df_jobs),
        'mean_arrival_rate': sim_mean_arrival_rate,
        'mean_interarrival_time': sim_mean_interarrival_time,
        'mean_service_rate': sim_mean_service_rate,
        'mean_service_time': sim_mean_service_time,
        'mean_wait_time': sim_mean_wait_time,
        'response_time_mean': sim_response_time_mean,
        'response_time_var': sim_response_time_var,
        'mean_jobs_in_system': sim_mean_jobs_in_system,
        'mean_jobs_in_queue': sim_mean_jobs_in_queue,
        'throughput_mean': sim_throughput_mean,
        'utilization': utilization
        }
    
    return results


# ---------------------------- Imprimir Resultados --------------------------- #

def format(value):
    return f"{value:,.4f}"


def print_title(parameters):

    print('Simulação')
    print('-------------------------')
    print(f'Número de Clientes:              = {format( parameters["NUM_JOBS"] )}')
    print(f'Taxa Média de Chegada (Lambda)   = {format( parameters["MEAN_ARRIVAL_RATE"] )}')
    print(f'Taxa Média de Serviço (Mu)       = {format( parameters["MEAN_SERVICE_RATE"] )}')
    print(f'Tempo Médio Entre Chegadas       = {format( 1.0/parameters["MEAN_ARRIVAL_RATE"])}')
    print(f'Tempo Médio de Serviço           = {format( 1.0/parameters["MEAN_SERVICE_RATE"])}')
    print()
    print()
    print()
    

def print_results(results):
    parameters = results['parameters']
    jobs = results['jobs']
    response_time = jobs['response_time']
    mean_arrival_rate = results['mean_arrival_rate']
    mean_service_rate = results['mean_service_rate']
    mean_service_time = results['mean_service_time']
    mean_response_time = results['response_time_mean']
    mean_throughput = results['throughput_mean']
    util = results['utilization']
    mean_jobs_in_system = results['mean_jobs_in_system']
    
    print('Estatísticas de Simulação')    
    print('-------------------------')
    
    print(f'Duração Total                   = {format( results["total_duration"] )}')
    print()
    print()
    print()
    print('Taxas Médias:')
    print()
    print(f'Taxa de Chegada                 = {format( mean_arrival_rate )}') 
    print(f'Tempo entre Chegadas            = {format( results["mean_interarrival_time"] )}')
    print(f'Tempo de Resposta               = {format( mean_response_time )}')
    print(f'Tempo de Espera                 = {format( results["mean_wait_time"] )}')
    print(f'Taxa de Serviço                 = {format( mean_service_rate )}')
    print(f'Tempo de Serviço                = {format( mean_service_time )}')
    print(f'Clientes no Sistema             = {format( mean_jobs_in_system )}')
    print(f'Clientes na Fila                = {format( results["mean_jobs_in_queue"] )}')
    print(f'Throughput                      = {format( mean_throughput )}')
    print(f'Utilização                      = {format( util)}')
    print()
    print()
    print()
    
    
