# Funções para Plotagem dos Resultados das Simulações

import matplotlib.pyplot as plt
from numpy.core.fromnumeric import size
import seaborn as sns
from src.settings import *

sns.set_style('darkgrid')

def plot_result(results):
    '''
    Função principal, chama as demais funções de plotagem.
    '''
    parameters = results['parameters']
    jobs = results['jobs']
    events = results['events']
    
    _plot_gantt_chart(parameters, jobs)
    _plot_queue_over_time(events)
    _plot_histogram(parameters, jobs['interarrival_time'], 'Histograma de Tempos entre Chegadas', 'Tempo entre Chegadas')
    _plot_histogram(parameters, jobs['wait_time'], 'Histograma de Tempos de Espera', 'Tempo de Espera')
    _plot_histogram(parameters, jobs['service_time'], 'Histograma de Tempos de Serviço', 'Tempo de Serviço')
    
    mean_service_time_per_type = results['jobs'][['event_type', 'service_time']].groupby('event_type').mean()
    _plot_bar(mean_service_time_per_type.index, mean_service_time_per_type['service_time'],
              'Tempo Médio de Serviço por Tipo de Atendimento', 'Tempo Médio de Serviço', 'Tipo')
    
    
def _plot_gantt_chart(parameters, jobs):
    '''
    Tarefas representadas pelo Diagrama de Gantt.
    '''
    num_jobs = parameters['NUM_JOBS']
    start_job = int(num_jobs/5)
    end_job = start_job+50
    trunc_df = jobs[start_job:end_job]
    
    colors=[]
    for l in trunc_df['event_type']:
        if l=='1':
            colors.append('limegreen')
        elif l=='2':
            colors.append('crimson')
        else:
            colors.append('gold')
    
    plt.figure(figsize=GANTT_SIZE)
    plt.title('Diagrama de Gantt Parcial (Atendimentos)', size=TITLE_SIZE)
    plt.xlabel('Tempo', size=LABEL_SIZE)
    plt.ylabel('ID do Cliente', size=LABEL_SIZE)
    
    plt.barh(
        y=trunc_df.index,
        left=trunc_df['arrive_time'],
        width=trunc_df['response_time'],
        alpha=0.5,
        height=0.5,
        color=colors,
        edgecolor='black',
    )

    plt.barh(
        y=trunc_df.index,
        left=trunc_df['start_time'],
        width=trunc_df['service_time'],
        alpha=1.0,
        height=0.8,
        color=colors,
        edgecolor='black',
    )
    
    plt.gca().invert_yaxis()
    plt.show()


def _plot_queue_over_time(events):
    '''
    Plotagem do número de itens no sistema ao longo do tempo.
    '''
    plt.figure(figsize=FIG_SIZE)
    plt.title('Número de Clientes na Fila', size=TITLE_SIZE)
    plt.xlabel('Tempo', size=LABEL_SIZE)
    plt.ylabel('Clientes na Fila', size=LABEL_SIZE)
    plt.plot(events['lo_bd'], events['jobs_in_queue'])
    plt.show()


def _plot_histogram(parameters, data, title, xlabel):
    '''
    Plotagem de Histogramas.
    '''
    plt.figure(figsize=FIG_SIZE)
    plt.title(title, size=TITLE_SIZE)
    plt.xlabel(xlabel, size=LABEL_SIZE)
    plt.ylabel('Count', size=LABEL_SIZE)
    plt.hist(data, bins=HIST_BINS)
    plt.show()
    
    
def _plot_bar(x, y, title, xlabel, ylabel):
    '''
    Plotagem em Barras.
    '''
    plt.figure(figsize=FIG_SIZE)
    plt.title(title, size=TITLE_SIZE)
    plt.xlabel(xlabel, size=LABEL_SIZE)
    plt.ylabel(ylabel, size=LABEL_SIZE)
    plt.bar(x=x, height=y)
    plt.show()