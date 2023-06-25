import numpy as np

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
        matrix.append(row)

    return iterations, learning_rate, discount_factor, reward_value, epsilon, dimensions, np.array(matrix)

# Exemplo de uso
file_name = 'entrada.txt'  # Nome do arquivo de entrada
iterations, learning_rate, discount_factor, reward_value, epsilon, dimensions, matrix = read_input_file(file_name)

# Imprimir os valores lidos
print("Número de iterações:", iterations)
print("Taxa de aprendizado (alpha):", learning_rate)
print("Fator de desconto (gamma):", discount_factor)
print("Valor da recompensa:", reward_value)
print("Valor de epsilon (e):", epsilon)
print("Dimensões da matriz:", dimensions)
print("Matriz:")
print(matrix)
