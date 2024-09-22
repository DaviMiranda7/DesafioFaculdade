import random
import numpy as np

# Função a ser minimizada: f(x) = x³ - 6x + 14
def funcao(x):
    return x**3 - 6*x + 14

# Converter vetor binário em valor real
def binario_para_real(binario, limite_inferior, limite_superior):
    valor_decimal = int("".join(str(int(b)) for b in binario), 2)
    return limite_inferior + (valor_decimal / (2**len(binario) - 1)) * (limite_superior - limite_inferior)

# Gerar cromossomo binário
def gerar_cromossomo_binario(tamanho):
    return [random.randint(0, 1) for _ in range(tamanho)]

# Função de crossover (1 ponto de corte)
def crossover(pai1, pai2):
    ponto_corte = random.randint(1, len(pai1) - 1)
    return pai1[:ponto_corte] + pai2[ponto_corte:], pai2[:ponto_corte] + pai1[ponto_corte:]

# Função de mutação
def mutacao(cromossomo, taxa_mutacao):
    for i in range(len(cromossomo)):
        if random.random() < taxa_mutacao:
            cromossomo[i] = 1 - cromossomo[i]
    return cromossomo

# Algoritmo genético
def algoritmo_genetico(limite_inferior, limite_superior, geracoes, numero_individuos, tamanho_binario, taxa_mutacao, elitismo=False):
    populacao = [gerar_cromossomo_binario(tamanho_binario) for _ in range(numero_individuos)]
    melhores_individuos = []

    for _ in range(geracoes):
        fitness_populacao = [(funcao(binario_para_real(cromossomo, limite_inferior, limite_superior)), cromossomo) for cromossomo in populacao]
        fitness_populacao.sort(key=lambda x: x[0])  # Ordena pelo valor da função

        # Elitismo
        if elitismo:
            elite = fitness_populacao[:1]
        else:
            elite = []

        # Melhor cromossomo da geração
        melhores_individuos.append(fitness_populacao[0])

        nova_populacao = elite + fitness_populacao[:numero_individuos // 2]  # Seleção dos melhores
        while len(nova_populacao) < numero_individuos:
            pai1 = random.choice(fitness_populacao)[1]
            pai2 = random.choice(fitness_populacao)[1]
            filho1, filho2 = crossover(pai1, pai2)
            nova_populacao.append((0, mutacao(filho1, taxa_mutacao)))
            nova_populacao.append((0, mutacao(filho2, taxa_mutacao)))

        populacao = [cromossomo for _, cromossomo in nova_populacao]

    return melhores_individuos

# Parâmetros
limite_inferior = -10
limite_superior = 10
geracoes = 50
numero_individuos = 10
tamanho_binario = 16
taxa_mutacao = 0.01
elitismo = True

# Executar algoritmo genético
resultado = algoritmo_genetico(limite_inferior, limite_superior, geracoes, numero_individuos, tamanho_binario, taxa_mutacao, elitismo)
for r in resultado:
    x_real = binario_para_real(r[1], limite_inferior, limite_superior)
    print(f"x: {x_real:.5f}, f(x): {r[0]:.5f}")
