import numpy as np 
import itertools



def generate_pairs(data_rotated_id, VH, FC,iterations):
    
    id_list = data_rotated_id['ID'][:iterations] 
    
    pairs = np.array(list(itertools.combinations(id_list, 2)))
    
    idx1_array = pairs[:, 0]  
    idx2_array = pairs[:, 1]
    
    
    z_coords = data_rotated_id['z_r'][:iterations]
    z_distances = np.abs(z_coords[idx1_array] - z_coords[idx2_array])
    mask = z_distances <= (VH * FC)
    valid_pairs = pairs[mask]
    
    x_coords = data_rotated_id['x_r'][:iterations]
    y_coords = data_rotated_id['y_r'][:iterations]
    
    valid_x_coords = x_coords[idx1_array[mask]] - x_coords[idx2_array[mask]]
    valid_y_coords = y_coords[idx1_array[mask]] - y_coords[idx2_array[mask]]

    
    distances_dict = {
        'ID_1': valid_pairs[:, 0],
        'ID_2': valid_pairs[:, 1],
        'Distance_x': valid_x_coords,
        'Distance_y': valid_y_coords,
        'Distance_z': z_distances[mask]
        
    }

    pairs_dict = {
        'ID_1': valid_pairs[:, 0],
        'ID_2': valid_pairs[:, 1],
    }

    pairs_dict['ID_1'] += 1  
    pairs_dict['ID_2'] += 1
    
    return distances_dict, pairs_dict

