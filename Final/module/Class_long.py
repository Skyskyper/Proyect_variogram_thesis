import numpy as np 

def classify_point_in_longitudinal_areas(distances, pairs,AH,VH):
    
    # Precalcula ángulos y anchura si AH es constante y se tiene un número fijo de sectores
    angle_cache = {}
    half_width_squared = (VH / 2) #** 2
    total_sectors = int(360/AH)

    for s in range(total_sectors):  # total_sectors es el número de sectores que tienes
        angle_bisectrix = s * AH + (AH / 2)
        angle_rad = np.radians(angle_bisectrix)
        angle_cache[s] = (np.cos(angle_rad), np.sin(angle_rad))
        

    def classify_normal(distance_x, distance_y, sector):
        dx, dy = angle_cache[sector]
        proj = distance_x * dx + distance_y * dy
        b_squared = distance_x**2 + distance_y**2 - proj**2
        # Verificación si la variable está dentro de la normal sin np.sqrt
        return b_squared <= half_width_squared

    
    # Inicializar una lista para almacenar si los pares están dentro de la tolerancia de normalidad
    inside_normality_tolerance = []

    # Iterar sobre los pares y clasificar cada uno
    for i in range(len(pairs['ID_1'])):
        # Encontrar las distancias correspondientes en el diccionario `distances`
        id_1 = pairs['ID_1'][i]
        id_2 = pairs['ID_2'][i]
        
        # Usar np.where para encontrar el índice donde coinciden ID_1 e ID_2
        idx = np.where((distances['ID_1'] == id_1) & (distances['ID_2'] == id_2))
        
        if len(idx[0]) > 0:
            # Obtener el primer índice válido
            index = idx[0][0]
            
            distance_x = distances['Distance_x'][index]
            distance_y = distances['Distance_y'][index]
            sector = pairs['sector'][i]

            # Clasificar si el punto está dentro de la tolerancia de normalidad
            is_inside = classify_normal(distance_x, distance_y, sector)
            inside_normality_tolerance.append(is_inside)
        else:
            # Si no hay un índice válido, agregar `False` como predeterminado
            inside_normality_tolerance.append(False)

    # Filtrar los pares que están dentro de la normalidad
    filtered_indices = np.where(np.array(inside_normality_tolerance))[0]
    

    # Actualizar los arreglos de los diccionarios `pairs` y `distances` con los índices filtrados
    pairs = {key: np.array(value)[filtered_indices] for key, value in pairs.items()}
    distances = {key: np.array(value)[filtered_indices] for key, value in distances.items()}

    return pairs

