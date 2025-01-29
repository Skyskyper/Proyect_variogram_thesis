import numpy as np

def diferencias(pairs_dict, dataid,VAR,VAR2):
    # Inicializar listas para almacenar los resultados
    var_diffs_squared = []
    var2_diffs_squared = []

    # Obtener los índices de ID_1 e ID_2 desde pairs_dict
    id_1_indices = pairs_dict['ID_1']
    id_2_indices = pairs_dict['ID_2']

    # Extraer los valores de 'ID', 'VAR' y 'VAR2' del diccionario `dataid`
    ids = dataid['ID']
    var_values = dataid[VAR]
    var2_values = dataid[VAR2]

    # Crear mapeos entre IDs y los valores correspondientes
    id_to_var = dict(zip(ids, var_values))
    id_to_var2 = dict(zip(ids, var2_values))

    # Calcular las diferencias al cuadrado para VAR y VAR2
    for id_1, id_2 in zip(id_1_indices, id_2_indices):
        # Calcular y redondear diferencias para VAR
        diff_var = (id_to_var[id_2] - id_to_var[id_1]) ** 2
        var_diffs_squared.append(diff_var)

        # Calcular y redondear diferencias para VAR2
        diff_var2 = (id_to_var2[id_2] - id_to_var2[id_1]) ** 2
        var2_diffs_squared.append(diff_var2)
        
        #TODO hacer producto de las dos diferencias ( pos y neg ) 
        #TODO mirar forma de colocar un round si es seleccionado 
        

    # Añadir los resultados como nuevos arrays en el diccionario `pairs_dict`
    pairs_dict[VAR] = np.array(var_diffs_squared)
    pairs_dict[VAR2] = np.array(var2_diffs_squared)
    
    

    return pairs_dict

