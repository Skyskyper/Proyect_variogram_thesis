
import numpy as np 


def apply_rotation(dataid, final_rotation):
    # Asegúrate de que dataid sea un diccionario con las claves 'x', 'y', y 'Z'
    if not all(key in dataid for key in ['x', 'y', 'Z']):
        raise KeyError("dataid debe contener las claves 'x', 'y', y 'Z'")

    # Extraemos las coordenadas 'x', 'y', 'Z' como arrays de NumPy
    positions = np.array([dataid['x'], dataid['y'], dataid['Z']])

    # Aplicamos la rotación utilizando la matriz final_rotation
    rotated_positions = np.dot(final_rotation, positions)

    # Creamos un nuevo diccionario con las coordenadas rotadas y la columna 'ID'
    data_rotated_id = {
        'ID': dataid['ID'],         # La columna 'ID' con las posiciones rotadas
        'x_r': rotated_positions[0, :],   # Coordenadas rotadas en x
        'y_r': rotated_positions[1, :],   # Coordenadas rotadas en y
        'z_r': rotated_positions[2, :]    # Coordenadas rotadas en z
    }

    # Devolvemos el diccionario con solo las variables rotadas y la columna 'ID'
    return data_rotated_id

