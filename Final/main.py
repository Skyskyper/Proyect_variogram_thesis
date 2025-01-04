from common_imports import *
from module import interface 
from module import Load_file
from module import p_rotation 
from module import ids
from module import ids

def main(): 
    
    #matrix = interface.create_3d_scene()
    #print("Final Rotation Matrix:", matrix)
    
    input_file = "C:\\Users\\marsa\\OneDrive\\GitHub_ordenado\\Versiones\\test_data.csv"
    input_file = Load_file.load_data(input_file)
    '''
    data_rotated = p_rotation.apply_rotation(input_file)
    rotated_positions = data_rotated['rotated_positions']
    rotated_positions_with_ids = ids.add_ids(rotated_positions)  # Llamar a add_ids
    '''
    data_rotated = p_rotation.apply_rotation(input_file)
    rotated_positions_with_ids = ids.add_ids(data_rotated)
    
    data_rotated['ID'] = rotated_positions_with_ids
    print ("data id",data_rotated)
    



if __name__ == "__main__":
    main()