import numpy as np 

def classify_point_in_longitudinal_areas(distances_dict , pairs_dict ,AH,VH):
    
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

    
    # Clasificar directamente usando las distancias y sectores del diccionario `distances`
    inside_normality_tolerance = np.array([
        classify_normal(dx, dy, sector)
        for dx, dy, sector in zip(distances_dict['Distance_x'], distances_dict['Distance_y'], pairs_dict['sector'])
    ])

    # Filtrar los índices donde los pares están dentro de la tolerancia
    filtered_indices = np.where(inside_normality_tolerance)[0]

    
    # Se prefiere aplicar el filtro automaticamente o ver cuales entran y cuales no 
    
    #pairs = {key: np.array(value)[filtered_indices] for key, value in pairs_dict.items()}
    pairs_dict['Normal'] = inside_normality_tolerance
    
    distances_dict = {key: np.array(value)[filtered_indices] for key, value in distances_dict.items()}

    # Devolver los diccionarios actualizados
    return pairs_dict, distances_dict


