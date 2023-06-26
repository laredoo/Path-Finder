import numpy as np

def startEnvironment(environment):
    #Create a 3D numpy array to hold the current Q-values for each state and action pair: Q(s, a) 
    #The array contains n rows and n columns (to match the shape of the environment), as well as a third "action" dimension.
    #The "action" dimension consists of 4 layers that will allow us to keep track of the Q-values for each possible action in
    #each state (see next cell for a description of possible actions). 
    #The value of each (state, action) pair is initialized to 0.
    rows, columns = environment.shape
    q_values = np.zeros((rows, columns, 4))
    # agora, setamos a recompensa como +1, -1 e 0 nos terminais.
    # Iterar sobre a matriz
    for i in range(environment.shape[0]):
        for j in range(environment.shape[1]):
            value = environment[i, j]
            if value == -1:
                q_values[i,j] = 0
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
  if current_row_index < 0 or current_row_index >= rows or current_column_index < 0 or current_column_index >= columns:
     return True
  else:
    #if the reward for this location is -1, then it is not a terminal state (i.e., it is a 'white square')
    if rewards[current_row_index, current_column_index] == -1. or rewards[current_row_index, 
                current_column_index] == 1. or rewards[current_row_index, current_column_index] == 0.:
        return True
    else:
        return False
  
#define an epsilon greedy algorithm that will choose which action to take next (i.e., where to move next)
def get_next_action(q_values, current_row_index, current_column_index, epsilon):
  #if a randomly chosen value between 0 and 1 is less than epsilon, 
  #then choose the most promising value from the Q-table for this state.
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_row_index, current_column_index])
  else: #choose a random action
    return np.random.randint(4)
  
#define a function that will get the next location based on the chosen action
def get_next_location(environment, current_row_index, current_column_index, action_index):
  rows, columns = environment.shape
  # sorteamos um valor aleatorio entre 0 e 1
  # se slide_factor < 80% nao escorrega
  # caso contrario, sorteamos as outras opcoes
  slide_factor = np.random.random()
  actions = ['up', 'right', 'down', 'left']
  new_row_index = current_row_index
  new_column_index = current_column_index

  if actions[action_index] == 'up' and current_row_index > 0:
    if slide_factor < 0.8:
        new_row_index -= 1
    else:
       if np.random.randint(2) == 0:
          new_column_index += 1 # escorrego para direita
       new_column_index -= 1 # escorrego para esquerda

  elif actions[action_index] == 'right' and current_column_index < columns - 1:
    if slide_factor < 0.8:    
        new_column_index += 1
    else:
       if np.random.randint(2) == 0:
          new_row_index -= 1 # escorrego para cima
       new_row_index += 1 # escorrego para baixo

  elif actions[action_index] == 'down' and current_row_index < rows - 1:
    if slide_factor < 0.8:
        new_row_index += 1
    else:
       if np.random.randint(2) == 0:
          new_column_index += 1 # escorrego para direita
       new_column_index -= 1 # escorrego para esquerda

  elif actions[action_index] == 'left' and current_column_index > 0:
    if slide_factor < 0.8:
        new_column_index -= 1
    else:
       if np.random.randint(2) == 0:
          new_row_index -= 1 # escorrego para cima
       new_row_index += 1 # escorrego para baixo

  return new_row_index, new_column_index

#Define a function that will get the shortest path between any location within the warehouse that 
#the robot is allowed to travel and the item packaging location.
def get_shortest_path(environment, rewards, start_row_index, start_column_index):
  rows, columns = environment.shape
  #return immediately if this is an invalid starting location
  if is_terminal_state(environment, rewards, start_row_index, start_column_index):
    return []
  else: #if this is a 'legal' starting location
    current_row_index, current_column_index = start_row_index, start_column_index
    shortest_path = []
    shortest_path.append([current_row_index, current_column_index])
    #continue moving along the path until we reach the goal (i.e., the item packaging location)
    while not is_terminal_state(environment, rewards, current_row_index, current_column_index):
      #get the best action to take
      action_index = get_next_action(environment, current_row_index, current_column_index, 1)
      
      #move to the next location on the path, and add the new location to the list
      current_row_index, current_column_index = get_next_location(environment, current_row_index, current_column_index, action_index)
      
      # proibindo posicoes fora da matriz
      if current_row_index < 0 or current_row_index >= rows or current_column_index < 0 or current_column_index >= columns:
        break
      
      shortest_path.append([current_row_index, current_column_index])
    return shortest_path

def printData(i, alpha, gamma, r, epsilon, d, matrix):
    print("Número de iterações:", i)
    print("Taxa de aprendizado (alpha):", alpha)
    print("Fator de desconto (gamma):", gamma)
    print("Valor da recompensa:", r)
    print("Valor de epsilon (e):", epsilon)
    print("Dimensões da matriz:", d)
    # print("Matriz:")
    # print(matrix)

