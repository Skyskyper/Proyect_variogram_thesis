from module.common_imports import *
from module import interface 
from module import Load_file
from module import p_rotation 
from module import ids


def main(): 
    
    #matrix = interface.create_3d_scene()
    #print("Final Rotation Matrix:", matrix)
    
    input_file = "C:\\Users\\marsa\\OneDrive\\GitHub_ordenado\\Versiones\\test_data.csv"
    input_file = Load_file.load_data(input_file)
    
    
    data_rotated = p_rotation.apply_rotation(input_file)
    rotated_positions = data_rotated['rotated_positions']
    print(rotated_positions.keys())
    
    
    
    



if __name__ == "__main__":
    main()