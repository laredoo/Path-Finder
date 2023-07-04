import numpy as np

def startEnvironmentZeros(environment):
    rows, columns = environment.shape
    q_values = np.zeros((rows, columns, 4))
    # agora, setamos a recompensa como +1, -1 e 0 nos terminais.
    # Iterar sobre a matriz
    for i in range(environment.shape[0]):
        for j in range(environment.shape[1]):
            value = environment[i, j]
            if value == -1:
                q_values[i,j] = -1
            elif value == 7:
                q_values[i,j] = 1 
            elif value == 4:
                q_values[i,j] = -1
    
    return q_values

def startEnvironmentRandom(environment):
    rows, columns = environment.shape
    q_values = np.random.rand(rows, columns, 4)
    # agora, setamos a recompensa como +1, -1 e 0 nos terminais.
    # Iterar sobre a matriz
    for i in range(environment.shape[0]):
        for j in range(environment.shape[1]):
            value = environment[i, j]
            if value == -1:
                q_values[i,j] = -1
            elif value == 7:
                q_values[i,j] = 1 
            elif value == 4:
                q_values[i,j] = -1
    
    return q_values

def setRewards(environment, reward_value):
    rows, columns = environment.shape
    rewards = np.full((rows, columns), reward_value) # crio um np.array 2x2 para as recompensas
    # agora, setamos a recompensa como +1, -1 e 0 nos terminais.
    # Iterar sobre a matriz
    for i in range(environment.shape[0]):
        for j in range(environment.shape[1]):
            value = environment[i, j]
            if value == -1:
                rewards[i][j] = 0
            elif value == 7:
                rewards[i][j] = 1 
            elif value == 4:
                rewards[i][j] = -1
            elif value == 10:
                start_position = (i,j)
    # aproveitamos para já definir a posicao de inicio do agente
    return rewards, start_position

#define a function that determines if the specified location is a terminal state
def is_terminal_state(environment, rewards, current_row_index, current_column_index):
  rows, columns = environment.shape
  # out of bounds
  if current_row_index < 0 or current_row_index >= rows or current_column_index < 0 or current_column_index >= columns:
     return True
  else:
    #if the reward for this location is -1, then it is not a terminal state (i.e., it is a 'white square')
    if rewards[current_row_index, current_column_index] == -1. or rewards[current_row_index, 
                current_column_index] == 1. or rewards[current_row_index, current_column_index] == 0.:
        return True
    else:
        return False
  
# Defina um algoritmo epsilon greedy que irá escolher a próxima ação
def get_next_action(q_values, current_row_index, current_column_index, epsilon):
  # Se um valor aleatoriamente escolhido entre 0 e 1 é menor que epsilon,
  # escolha o valor mais promissor da Q-Table para esse estado.
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_row_index, current_column_index])
  else: # Escolha uma ação aleatória
    # print('epsilon greedy in action')
    return np.random.randint(4)
  
# Defina uma função que vai retornar o próximo estado baseado na ação escolhida
def get_next_location(environment, current_row_index, current_column_index, action_index):
  rows, columns = environment.shape
  # sorteamos um valor aleatorio entre 0 e 1
  # se slide_factor < 80% nao escorrega
  # caso contrario, sorteamos as outras opcoes
  slide_factor = np.random.random()
  # slide_factor = 0.79
  actions = ['up', 'right', 'down', 'left']
  new_row_index = current_row_index
  new_column_index = current_column_index

  if actions[action_index] == 'up' and current_row_index > 0:
    if slide_factor < 0.8:
        new_row_index -= 1
    else:
       if np.random.randint(2) == 0:
          # print('Escorreguei para a direita')
          new_column_index += 1 # escorrego para direita
       else:
          # print('Escorreguei para a esquerda') 
          new_column_index -= 1 # escorrego para esquerda

  elif actions[action_index] == 'right' and current_column_index < columns - 1:
    if slide_factor < 0.8:    
        new_column_index += 1
    else:
       if np.random.randint(2) == 0:
          # print('Escorreguei para cima')
          new_row_index -= 1 # escorrego para cima
       else:
          # print('Escorreguei para baixo')   
          new_row_index += 1 # escorrego para baixo

  elif actions[action_index] == 'down' and current_row_index < rows - 1:
    if slide_factor < 0.8:
        new_row_index += 1
    else:
       if np.random.randint(2) == 0:
          # print('Escorreguei para a direita')
          new_column_index += 1 # escorrego para direita
       else:
          # print('Escorreguei para a esquerda')    
          new_column_index -= 1 # escorrego para esquerda

  elif actions[action_index] == 'left' and current_column_index > 0:
    if slide_factor < 0.8:
        new_column_index -= 1
    else:
       if np.random.randint(2) == 0:
          # print('Escorreguei para cima') 
          new_row_index -= 1 # escorrego para cima
       else:  
          # print('Escorreguei para baixo')    
          new_row_index += 1 # escorrego para baixo

  return new_row_index, new_column_index

def translate_action(action_index):
   if action_index == 0:
      return 'c'
   elif action_index == 1:
      return 'd'
   elif action_index == 2:
      return 'b'
   elif action_index == 3:
      return 'e'

def get_best_actions(environment, rewards, rows, columns, q_values):
   best_actions= np.zeros((rows, columns), dtype = 'U1')
   for i in range(rows):
      for j in range(columns):
         action_index = get_next_action(q_values, i, j, 1.)
         best_actions[i][j] = translate_action(action_index)
         if is_terminal_state(environment, rewards, i, j):
            best_actions[i][j] = 'n'
   return best_actions

def in_bounds(n, row_index, column_index):
   if row_index >= 0 and row_index < n and column_index >= 0 and column_index < n:
      return True
   return False

def update_agent_position(environment, old_row_index, old_column_index, current_row_index, current_column_index
                          , start_row_index, start_column_index):
   new_env = environment.copy()
   new_env[current_row_index, current_column_index] = 10
   new_env[old_row_index, old_column_index] = 0
   if((current_row_index, current_column_index) != (start_row_index,start_column_index)):
      # print('entrei aqui')
      new_env[start_row_index, start_column_index] = 0
   return new_env
   
# Defina uma função que vai pegar o menor caminho entre qualquer localização de início e a saída,
# considerando as posições que o robô pode caminhar.
def get_shortest_path(environment, rewards, q_values, epsilon, start_row_index, start_column_index):
  rows, columns = environment.shape
  current_environment = environment.copy()
  reward = 0
  # essa lista vai conter todas as matrizes de posicao do meu agente
  data_list = []
  data_list.append(current_environment) # posição de início
  # return immediately if this is an invalid starting location
  if is_terminal_state(environment, rewards, start_row_index, start_column_index):
    return []
  else:
    current_row_index, current_column_index = start_row_index, start_column_index   
    shortest_path = []
    shortest_path.append([current_row_index, current_column_index])
    # continue moving along the path until we reach the goal (i.e., the item packaging location)
    while not rewards[current_row_index, current_column_index] == 1.:
      #choose which action to take (i.e., where to move next)
      action_index = get_next_action(q_values, current_row_index, current_column_index, epsilon)
      # move to the next location on the path, and add the new location to the list
      old_row_index, old_column_index = current_row_index, current_column_index
      current_row_index, current_column_index = get_next_location(environment, current_row_index, current_column_index, action_index)
      # A próxima posição é um terminal
      if (is_terminal_state(environment, rewards, current_row_index, current_column_index)):
         # Dentro do mapa
         if(in_bounds(rows, current_row_index, current_column_index)):
            # Caiu em um BURACO (reward = 0)
            if(rewards[current_row_index,current_column_index] == 0):
               # O agente permanece na mesma posição
               new_environment = current_environment.copy()
               data_list.append(new_environment)
               current_row_index, current_column_index = old_row_index, old_column_index
               reward += rewards[current_row_index, current_column_index]
               # print('nova recompensa\n', reward)
            # Caiu na posição -1
            elif(rewards[current_row_index, current_column_index] == -1.):
               # Coloco o agente nessa posição
               new_environment = current_environment.copy()
               new_environment[old_row_index,old_column_index] = 0
               new_environment[current_row_index,current_column_index] = 10
               data_list.append(new_environment)
               shortest_path.append([current_row_index, current_column_index])
               # Retorno o agente para a posição inicial
               current_row_index, current_column_index = start_row_index, start_column_index
               current_environment = environment.copy()
               data_list.append(environment)
               shortest_path = []
               shortest_path.append([current_row_index, current_column_index])
               reward = 0
               # print('resetei a recompensa, cai no terminal incorreto\n', reward)
            # Chego no resultado
            elif(rewards[current_row_index, current_column_index] == 1.):
               # Coloco a agente na nova posição
               new_environment = environment.copy()
               new_environment[old_row_index,old_column_index] = 0
               new_environment[current_row_index,current_column_index] = 10
               data_list.append(new_environment)
               shortest_path.append([current_row_index, current_column_index])
               reward += rewards[current_row_index, current_column_index]
               # print('recompensa final\n', reward)
               # Acaba o meu laço
               break
         # Fora do mapa
         elif(not in_bounds(rows, current_row_index, current_column_index)):
            # Agente permanece na mesma posição
            new_environment = current_environment.copy()
            data_list.append(new_environment)
            # Retorno o agente para a posição anterior
            current_row_index, current_column_index = old_row_index, old_column_index
      # A proxima posição não é um terminal
      elif(not is_terminal_state(environment, rewards, current_row_index, current_column_index)):
         new_environment = current_environment.copy()
         new_environment[old_row_index, old_column_index] = 0
         new_environment[current_row_index, current_column_index] = 10
         data_list.append(new_environment)
         current_environment = new_environment
         shortest_path.append([current_row_index, current_column_index])
         reward += rewards[current_row_index, current_column_index]
         # print('nova recompensa\n', reward)
    print('O menor caminho percorrido pelo agente foi:\n')
    return shortest_path, data_list, reward

def printData(i, alpha, gamma, r, epsilon, d, matrix):
    print("Número de iterações:", i)
    print("Taxa de aprendizado (alpha):", alpha)
    print("Fator de desconto (gamma):", gamma)
    print("Valor da recompensa:", r)
    print("Valor de epsilon (e):", epsilon)
    print("Dimensões da matriz:", d)
    # print("Matriz:")
    # print(matrix)
