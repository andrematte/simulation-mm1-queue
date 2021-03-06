# Configurações de Execução
SEED = 24

# Parâmetros Padrão
NUM_JOBS = 400
MEAN_ARRIVAL_RATE = 16
MEAN_SERVICE_RATE = 32
DISTRIBUTION = 'exponential'

EVENT_TYPES = ['1', '2', '3']
EVENT_WEIGHTS = [0.8, 0.15, 0.05]

# Configurações das Figuras
FIG_SIZE = (16,3)
GANTT_SIZE = (16,10)
TITLE_SIZE = 18
LABEL_SIZE = 14

HIST_BINS = 51

def generate_parameters(NUM_JOBS = 400, MEAN_ARRIVAL_RATE = 16, MEAN_SERVICE_RATE = 32, DISTRIBUTION = 'exponential'):
    parameters = {
        'NUM_JOBS': NUM_JOBS,
        'MEAN_ARRIVAL_RATE': MEAN_ARRIVAL_RATE,
        'MEAN_SERVICE_RATE': MEAN_SERVICE_RATE,
        'MEAN_INTERARRIVAL_TIME': 1.0 / MEAN_ARRIVAL_RATE,
        'MEAN_SERVICE_TIME': 1.0 / MEAN_SERVICE_RATE,
        'NUM_BINS': int(NUM_JOBS / MEAN_ARRIVAL_RATE),
        'EVENT_TYPES': EVENT_TYPES,
        'EVENT_WEIGHTS': EVENT_WEIGHTS,
        'DISTRIBUTION': DISTRIBUTION
    }
    return parameters

parameters = generate_parameters()