
from module import interface 
from module import Load_file
from module import ids
from module import p_rotation



def main(): 
    
    #matrix = interface.create_3d_scene()
    matrix = interface.final_rotation
    #print("Final Rotation Matrix:", matrix)
    
    input_file = "C:\\Users\\marsa\\OneDrive\\GitHub_ordenado\\Versiones\\test_data.csv"
    input_file = Load_file.load_data(input_file)    
    dataid = ids.add_ids(input_file)
    
    data_rotated_id = p_rotation.apply_rotation(dataid,matrix)
    print(data_rotated_id)
    
    
    
    
      
    



if __name__ == "__main__":
    main()