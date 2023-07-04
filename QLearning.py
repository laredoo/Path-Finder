import numpy as np
import funcoes as f
import sys
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation

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
# q_values = f.startEnvironmentZeros(matrix) # Função Utilizada para Inicializar o Ambiente com Valores Nulos
q_values = f.startEnvironmentRandom(matrix)

# inicializar as recompensas e a posicao de inicio
rewards, start_position = f.setRewards(matrix, reward_value)
start_row_index, start_column_index = start_position

# definir as acoes
# 0 = up, 1 = right, 2 = down, 3 = left
actions = ['up', 'right', 'down', 'left']

# Imprimir os valores lidos
f.printData(iterations, learning_rate, discount_factor, 
            reward_value, epsilon, dimensions, matrix)

#run through 1000 training episodes
for episode in range(iterations):
    # posicao de inicio
    row_index, column_index = start_position

    while not f.is_terminal_state(matrix, rewards, row_index, column_index):
        # Escolha qual a proxima ação a tomar
        action_index = f.get_next_action(q_values, row_index, column_index, epsilon)

        # Faça a ação escolhida e transicione para o próximo estado
        old_row_index, old_column_index = row_index, column_index # store the old row and column indexes
        aux_row, aux_column = f.get_next_location(matrix, row_index, column_index, action_index)
        # row_index, column_index = f.get_next_location(matrix, row_index, column_index, action_index)

        # proibindo posicoes fora da matriz
        if aux_row < 0 or aux_row >= rows or aux_column < 0 or aux_column >= columns:
            break

        row_index, column_index = aux_row, aux_column

        # Receba a recompensa pela transição para o novo estado e calcule a temporal difference
        reward = rewards[row_index, column_index]
        old_q_value = q_values[old_row_index, old_column_index, action_index]
        temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

        # Atualize o Q-value para o estado passado e o par de ação
        new_q_value = old_q_value + (learning_rate * temporal_difference) # Bellman Equation
        q_values[old_row_index, old_column_index, action_index] = new_q_value

print('Training complete!')
# best_actions = f.get_best_actions(matrix, rewards, rows, columns, q_values)
maior_qvalue  = np.max(q_values, axis=2)
best_actions = f.get_best_actions(maior_qvalue , rewards, rows, columns, q_values)
shortest_path, data_list, final_reward = f.get_shortest_path(matrix, rewards, q_values, epsilon, start_row_index, start_column_index)
print(shortest_path)
# print('A recompensa final obtida ao longo de todo o caminho (contando o estado terminal final, em que a recompensa é +1) é igual à:', final_reward)
print('\nLembrando que o agente pode deslizar no meio do caminho!')

sns.heatmap(maior_qvalue , cbar = True, square= True, annot = best_actions, fmt='', vmin=np.min(maior_qvalue), vmax=np.max(maior_qvalue))
# sns.heatmap(matrix, cbar = False, square= True, annot = best_actions, fmt='')
plt.savefig(output_file+'.png')

fig = plt.figure()

# NxN é o tamanho da matriz em questão
def init(N):
    sns.heatmap(np.zeros((N,N)), square = True, cbar = False)

def animate(i):
    data = data_list[i]
    sns.heatmap(data, square = True, cbar = False)

anim = animation.FuncAnimation(fig, animate, init_func = init(rows), frames = len(data_list), repeat = False)
pillowwriter = animation.PillowWriter(fps = 7)

anim.save(output_file+'.gif', writer=pillowwriter)
