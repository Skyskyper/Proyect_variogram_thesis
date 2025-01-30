import numpy as np 
import matplotlib.pyplot as plt  

def step(distances, pairs, VH):
    
    # Asegurarse de que los valores de distancia sean unidimensionales
    distance_x = distances['Distance_x']
    distance_y = distances['Distance_y']

    # Calcular el valor de 'step'
    step_values = (np.sqrt(distance_x**2 + distance_y**2) / VH).astype(int)
    

    # Asignar los valores de 'step' directamente a los pares
    pairs['step'] = step_values
    
    
    plt.hist(pairs['step'],bins = 10)    
    plt.show()
    

    return pairs
