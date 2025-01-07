import numpy as np 
import itertools
'''

def generate_pairs(data_rotated_id, VH,FC):
    
    id_list = data_rotated_id['ID'] [:200]  # Acceso al diccionario
    
    pairs = list(itertools.combinations(id_list, 2))
    distances = []
    valid_pairs = []
    
    # Crear los diferentes pares
    for id1, id2 in pairs:
        # Obtención de los índices
        idx1 = np.where(data_rotated_id['ID'] == id1)[0][0]
        idx2 = np.where(data_rotated_id['ID'] == id2)[0][0]
        
        # Distancia entre las coordenadas
        x_distance = data_rotated_id['x_r'][idx1] - data_rotated_id['x_r'][idx2]
        y_distance = data_rotated_id['y_r'][idx1] - data_rotated_id['y_r'][idx2]
        z_distance = abs(data_rotated_id['z_r'][idx1] - data_rotated_id['z_r'][idx2])

        # Aplicar la tolerancia vertical con corrección
        if z_distance <= (VH*FC ): ############################################################## REVISAR
            distances.append([id1, id2, x_distance, y_distance, z_distance])
            valid_pairs.append([id1, id2])
    
    # Salida en diccionarios de numpy arrays
    pairs_dict = {
        'ID_1': np.array([p[0] for p in valid_pairs]),
        'ID_2': np.array([p[1] for p in valid_pairs])
    }
    
    distances_dict = {
        'ID_1': np.array([d[0] for d in distances]),
        'ID_2': np.array([d[1] for d in distances]),
        'Distance_x': np.array([d[2] for d in distances]),
        'Distance_y': np.array([d[3] for d in distances]),
        'Distance_z': np.array([d[4] for d in distances])
    }
    
    pairs_dict['ID_1'] += 1  # Incrementar todos los valores de ID_1
    pairs_dict['ID_2'] += 1  # Incrementar todos los valores de ID_2
    pairs_dict['ID_1'] = pairs_dict['ID_1'][:, 0]  
    pairs_dict['ID_2'] = pairs_dict['ID_2'][:, 0]
    
    return distances_dict, pairs_dict

'''

import numpy as np
import itertools

def generate_pairs(data_rotated_id, VH, FC):
    # Verificar el tipo de 'ID' y manejar listas de coordenadas
    id_list = data_rotated_id['ID'][:200]  # Acceso al diccionario (limitado a los primeros 200 IDs)
    #print(data_rotated_id.keys())
    #print("Contenido de 'data_rotated_id['ID'][:200]':", id_list[:10])  # Muestra los primeros 10 elementos

    # Convertir las listas de coordenadas en identificadores únicos (como cadenas)
    def convert_to_hashable(value):
        if isinstance(value, np.ndarray):  # Si es un numpy ndarray
            return str(value.tolist())  # Convertir el ndarray a una lista y luego a cadena
        elif isinstance(value, list):  # Si es una lista
            return str(value)  # Convertir la lista a cadena
        return value  # Si no es ndarray o lista, devolverlo tal cual

    # Aplicamos la conversión a todos los elementos de 'id_list'
    id_list = np.array([convert_to_hashable(val) for val in id_list])

    # Crear mapeo de IDs a índices
    id_to_index = {id_: idx for idx, id_ in enumerate(id_list)}  # Diccionario ID -> índice

    # Generar todas las combinaciones posibles de pares
    pairs = np.array(list(itertools.combinations(id_list, 2)))  # Generar pares
    idx1_array = np.array([id_to_index[id1] for id1 in pairs[:, 0]])  # Índices de ID_1
    idx2_array = np.array([id_to_index[id2] for id2 in pairs[:, 1]])  # Índices de ID_2

    # Coordenadas en forma de arrays
    x_coords = data_rotated_id['x_r'][:200]
    y_coords = data_rotated_id['y_r'][:200]
    z_coords = data_rotated_id['z_r'][:200]
    
    z_distances = np.abs(z_coords[idx1_array] - z_coords[idx2_array])
    mask = z_distances <= (VH * FC)
    valid_pairs = pairs[mask]
    
    # Calcular las distancias entre las coordenadas de manera vectorizada
    x_distances = x_coords[idx1_array] - x_coords[idx2_array]
    y_distances = y_coords[idx1_array] - y_coords[idx2_array]
   

    # Filtrar pares válidos según la tolerancia vertical
    

    # Crear diccionarios para las distancias y pares válidos
    
    distances_dict = {
        'ID_1': valid_pairs[:, 0],
        'ID_2': valid_pairs[:, 1],
        'Distance_x': x_distances[mask],
        'Distance_y': y_distances[mask],
        'Distance_z': z_distances[mask]
    }

    pairs_dict = {
        'ID_1': valid_pairs[:, 0],
        'ID_2': valid_pairs[:, 1],
    }

    return distances_dict, pairs_dict

