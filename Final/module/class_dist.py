import numpy as np    

def classify_distances(distances, pairs, AH):
    # Cálculo de sectores basado en los ángulos
    
    angles = np.degrees(np.arctan2(distances['Distance_y'], distances['Distance_x'])) % 180
    pairs['sector'] = (angles // AH).astype(int)
    
    

    '''
    Por si hicera falta tenerlo tambien en distances
    pairs['sector'] = ((np.arctan2(distances['Distance_y'], distances['Distance_x']) * (180 / np.pi)) % 180 // AH).astype(int)
    distances['sector']= pairs['sector'] 
    '''

    return distances, pairs