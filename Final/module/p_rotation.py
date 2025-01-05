import pandas as pd   
import numpy as np 
from module import interface 
from module import Constants

def apply_rotation(input_file):
    
    data = pd.read_csv(input_file)

    # Extract position columns and convert to NumPy array (efficient bulk conversion)
    positions = data[['x', 'y', 'Z']].to_numpy().T

    # Apply rotation directly using the global final_rotation
    rotated_positions = np.dot(interface.final_rotation, positions)

    # Extract VAR and VAR2 columns using global variable names
    var, var2 = data[[Constants.VAR, Constants.VAR2]].to_numpy().T
    
    print(var)

    # Return results in a dictionary
    return {
        'rotated_positions': rotated_positions.T,  # Include full rotated positions (transposed back)
        'xr': rotated_positions[0],               # Rotated x-coordinates
        'yr': rotated_positions[1],               # Rotated y-coordinates
        'zr': rotated_positions[2],               # Rotated z-coordinates
        'VAR': var,                                # First variable as NumPy array
        'VAR2': var2                               # Second variable as NumPy array
    }
