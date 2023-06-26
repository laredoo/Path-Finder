import numpy as np
import funcoes as f
import sys
import seaborn as sns
import matplotlib.pyplot as plt


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
rows, columns = matrix.shape

# inicializar o ambiente
q_values = f.startEnvironment(matrix)

# inicializar as recompensas e a posicao de inicio
rewards, start_position = f.setRewards(matrix, reward_value)
start_row_index, start_column_index = start_position
# print(rewards)
# print('start_position -------> ', start_position)

# print(q_values)

# definir as acoes
# 0 = up, 1 = right, 2 = down, 3 = left
actions = ['up', 'right', 'down', 'left']

# print(q_values)
# print(rewards)

# Imprimir os valores lidos
f.printData(iterations, learning_rate, discount_factor, 
            reward_value, epsilon, dimensions, matrix)

#run through 1000 training episodes
for episode in range(iterations):
    # posicao de inicio
    row_index, column_index = start_position

    # continue taking actions (i.e., moving) until we reach a terminal state
    # (i.e., until we reach the +1 or -1 area or crash into a wall)
    while not f.is_terminal_state(matrix, rewards, row_index, column_index):
        # choose which action to take (i.e., where to move next)
        action_index = f.get_next_action(q_values, row_index, column_index, epsilon)

        # perform the chosen action, and transition to the next state (i.e., move to the next location)
        old_row_index, old_column_index = row_index, column_index # store the old row and column indexes
        row_index, column_index = f.get_next_location(matrix, row_index, column_index, action_index)

        # proibindo posicoes fora da matriz
        if row_index < 0 or row_index >= rows or column_index < 0 or column_index >= columns:
            break

        # receive the reward for moving to the new state, and calculate the temporal difference
        reward = rewards[row_index, column_index]
        old_q_value = q_values[old_row_index, old_column_index, action_index]
        temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

        # update the Q-value for the previous state and action pair
        new_q_value = old_q_value + (learning_rate * temporal_difference) # Bellman Equation
        q_values[old_row_index, old_column_index, action_index] = new_q_value

print('Training complete!')

# print(q_values)
# print(f.get_shortest_path(matrix, rewards, start_row_index, start_column_index))

fig = plt.figure()
sns.heatmap(matrix, cbar = True, square= True, fmt='')
plt.savefig(output_file)