import numpy as np 
import matplotlib.pyplot as plt  
##asda
def step(distances, pairs, VH):
    
    # Asegurarse de que los valores de distancia sean unidimensionales
    distance_x = distances['Distance_x']#.flatten()
    distance_y = distances['Distance_y']#.flatten()

    # Calcular el valor de 'step'
    step_values = ((distance_x**2 + distance_y**2) / (VH**2)).astype(int)
    

    # Asignar los valores de 'step' directamente a los pares
    pairs['step'] = step_values
    '''
    plt.hist(pairs['step'],bins = 10)    
    plt.show()
    '''

    return pairs
