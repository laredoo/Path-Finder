import numpy as np
import funcoes as f
import sys

def read_input_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Ler os parâmetros de entrada
    parameters = lines[0].strip().split()
    iterations = int(parameters[0])
    learning_rate = float(parameters[1])
    discount_factor = float(parameters[2])
    reward_value = float(parameters[3])

    # Ler o valor de e (epsilon)
    if len(parameters) > 4:
        epsilon = float(parameters[4])
    else:
        print('____________________________________\n\nThe epsilon value was not provided\n____________________________________\n')
        epsilon = 1.0

    # Ler as dimensões da matriz
    dimensions = int(lines[1].strip())

    # Ler a matriz
    matrix = []
    for line in lines[2:]:
        row = list(map(int, line.strip().split()))
        row += [0] * (dimensions - len(row))  # Preencher com zeros, se necessário
        matrix.append(row)

    return iterations, learning_rate, discount_factor, reward_value, epsilon, dimensions, np.array(matrix)

# Verificar os argumentos da linha de comando
if len(sys.argv) < 3:
    print("Uso: python3 TP2.py <arquivo_entrada> <arquivo_saida>")
    sys.exit(1)

# Obter os nomes dos arquivos de entrada e saída
input_file = sys.argv[1]
output_file = sys.argv[2]

# Ler o arquivo de entrada
iterations, learning_rate, discount_factor, reward_value, epsilon, dimensions, matrix = read_input_file(input_file)

# inicializar o ambiente
q_values = f.startEnvironment(dimensions, dimensions)

# inicializar as recompensas e a posicao de inicio
rewards, start_position = f.setRewards(matrix, reward_value)
# print('start_position -------> ', start_position)

# definir as acoes
# 0 = up, 1 = right, 2 = down, 3 = left
actions = ['up', 'right', 'down', 'left']

# Imprimir os valores lidos
f.printData(iterations, learning_rate, discount_factor, 
            reward_value, epsilon, dimensions, matrix)

