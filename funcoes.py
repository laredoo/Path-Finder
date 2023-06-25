import numpy as np

def startEnvironment(environment_rows, environment_columns):
    #Create a 3D numpy array to hold the current Q-values for each state and action pair: Q(s, a) 
    #The array contains n rows and n columns (to match the shape of the environment), as well as a third "action" dimension.
    #The "action" dimension consists of 4 layers that will allow us to keep track of the Q-values for each possible action in
    #each state (see next cell for a description of possible actions). 
    #The value of each (state, action) pair is initialized to 0.
    q_values = np.zeros((environment_rows, environment_columns, 4))
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

def printData(i, alpha, gamma, r, epsilon, d, matrix):
    print("Número de iterações:", i)
    print("Taxa de aprendizado (alpha):", alpha)
    print("Fator de desconto (gamma):", gamma)
    print("Valor da recompensa:", r)
    print("Valor de epsilon (e):", epsilon)
    print("Dimensões da matriz:", d)
    print("Matriz:")
    print(matrix)

