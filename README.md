# PPGEE0260: Modelagem e Simulação Discreta de Sistemas

Aluno: Carlos André de Mattos Teixeira

Código baseado em: https://github.com/williewheeler/stats-demos/blob/master/queueing/single-queue-sim.ipynb 

## Descrição do Projeto

**Objetivo:** Adicionar dois novos eventos no simulador de fila M/M/1.

**Requisitos:**

1. Um programa executável e todos os arquivos necessários à sua execução;
2. Um relatório contendo toda a documentação do programa (variáveis, parâmetros, rotinas, fluxogramas das rotinas, etc.);
3. Um pequeno manual sobre como executar o programa e constando a modelagem do sistema.

**Método de Avaliação:**

O simulador será avaliado com base nos seguintes critérios e pesos:

1. Funcionamento de acordo com o solicitado. Isto é, o modelo executado deve ter um comportamento (observável) semelhante ao descrito no escopo desta proposta
2. Implementação de funções aleatórias. Pelo menos as funções: Uniforme, Triangular, Normal e Exponencial. Além da alternativa de uso de um valor constante
3. Interface com o usuário (entrada de dados, visualização dos resultados)
4. Resultados dos experimentos
5. Documentação


## Instruções de Execução


- As simulações são executadas através do arquivo *Jupyter Notebook* [`experiments.ipynb`](https://github.com/andrematte/simulation-mm1-queue/blob/main/experiments.ipynb).
- Para executar uma simulação com as configurações padrão, basta executar a função `run_sim_and_plot(parameters)`. As configurações padrão são as seguintes:
  
  | Parâmetro                | Valor       |
  |--------------------------|-------------|
  | Seed                     | 24          |
  | Número de Clientes       | 400         |
  | Taxa Média de Chegada    | 16          |
  | Taxa Média de Serviço    | 32          |
  | Distribuição             | Exponencial |

- É possível personalizar os experimentos ao sobreescrever o dicionário de parâmetros com a função`generate_parameters()` e, em seguida, executar a função `run_sim_and_plot(parameters)`. Por exemplo:

```python
parameters = generate_parameters(NUM_JOBS, MEAN_ARRIVAL_RATE, MEAN_SERVICE_RATE, DISTRIBUTION)
run_sim_and_plot(parameters)
```

## Referências


[1] https://github.com/williewheeler/stats-demos/blob/master/queueing/single-queue-sim.ipynb 

[2] https://medium.com/wwblog/simulating-an-m-m-1-queue-in-python-f894f5a68db2

[3] https://web.fe.up.pt/~mac/ensino/docs/IO20032004/FilasEspera.pdf
