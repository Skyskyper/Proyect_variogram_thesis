import numpy as np
import pandas as pd

def add_ids(data):
    """
    Añade IDs únicos como una nueva columna al diccionario de arrays.
    
    Args:
        input_file (dict): Diccionario con arrays de NumPy. 
                           Los arrays deben tener el mismo número de filas.

    Returns:
        dict: Diccionario actualizado con una clave adicional 'dataid',
              que contiene los IDs concatenados con las posiciones originales.
    """
    
    ids = np.arange(len(data), dtype=int).reshape(-1, 1)  # IDs como columna
    
    # Concatenar los IDs con las columnas originales
    data_array = data.to_numpy()  # Convertir el DataFrame a un arreglo NumPy
    
    dataid = np.hstack((ids, data_array))  # Combinar los IDs con los datos
    
    dataid_array = np.hstack((ids, data_array))
    
    dataid = {'ID': dataid[:, 0].astype(int)}  # Primera columna como IDs enteros
    for idx, col in enumerate(data.columns):
        dataid[col] = dataid_array[:, idx + 1]
        
    return dataid

