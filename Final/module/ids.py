import numpy as np

'''
def add_ids(rotated_positions):
    # Crear un array con IDs enteros y posiciones concatenados
    rotated_positions_with_ids = np.column_stack((np.arange(len(rotated_positions), dtype=int), rotated_positions))
    return rotated_positions_with_ids
'''
def add_ids(data_rotated):
    # Extraer las posiciones rotadas del diccionario
    rotated_positions = data_rotated['rotated_positions']
    
    # Crear un array de IDs enteros y concatenarlos con las posiciones rotadas
    ids = np.arange(len(rotated_positions), dtype=int).reshape(-1, 1)  # IDs como columna
    rotated_positions_with_ids = np.hstack((ids, rotated_positions))  # Concatenar IDs y posiciones
    
    # Actualizar el diccionario data_rotated con los IDs añadidos
    data_rotated['rotated_positions_with_ids'] = rotated_positions_with_ids
    
    return data_rotated
