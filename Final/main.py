
from module import interface 
from module import Load_file
from module import ids
from module import p_rotation
from module import Pairs
from module import class_dist
from module import Class_long
from module import step 
from module import var_diference
from module import variogram 
from module.Constants import AH,VH,VAR,VAR2,FC,iterations,max_step

import cProfile
import pstats
import os     
import pandas as pd 


def main(): 
    
    matrix = interface.create_3d_scene()
    #matrix = interface.final_rotation_try
    print("Final Rotation Matrix:", matrix)
    
    input_file = "C:\\Users\\marsa\\OneDrive\\GitHub_ordenado\\Versiones\\test_data.csv"
    input_file = Load_file.load_data(input_file)   
     
    dataid = ids.add_ids(input_file)
    
    data_rotated_id = p_rotation.apply_rotation(dataid,matrix)
    
    distances_dict, pairs_dict = Pairs.generate_pairs(data_rotated_id,VH,FC,iterations)
    
    
    pairs_dict = class_dist.classify_distances(distances_dict, pairs_dict, AH)
    
    for clave, array in pairs_dict.items():
        print(f"Claveppp: {clave}, Cantidad de valores: {array.size}")
    for clave, array in distances_dict.items():
        print(f"Clavedddd: {clave}, Cantidad de valores: {array.size}")
    
    pairs_dict, distances_dict = Class_long.classify_point_in_longitudinal_areas(distances_dict,pairs_dict,AH,VH)
    
    pairs_dict = step.step(distances_dict, pairs_dict,VH)
    
    pairs_dict = var_diference.diferencias(pairs_dict,dataid,VAR,VAR2)
    
    pairs_fin = variogram.variogram(pairs_dict,VH,VAR,VAR2,max_step)
  
    
    '''
    printeo = pairs_dict
    nombre = "pairs1.csv"
    # Ruta de la carpeta donde se guardará el archivo  
    folder_path = "C:\\Users\\marsa\\OneDrive\\GitHub_ordenado\\Final\\test"
    # Crear la carpeta si no existe
    if not os.path.exists(folder_path):
        os.makedirs(folder_path) 
    # Convertir el diccionario a un DataFrame
    df = pd.DataFrame(printeo)
    # Ruta completa del archivo CSV
    output_file = os.path.join(folder_path, nombre)
    # Guardar el DataFrame como CSV
    df.to_csv(output_file, index=False)
    '''
    
    
def wrapper_for_profiling():
    # Envoltorio que llama a generate_pairs con los argumentos correctos
    main()
    

if __name__ == "__main__":
    
    profiler = cProfile.Profile()
    
    profiler.enable()
    
    wrapper_for_profiling()
    
    profiler.disable()

    # Crear un objeto pstats para procesar los resultados
    stats = pstats.Stats(profiler)
    # Ordenar por el tiempo total y mostrar solo las 10 funciones más lentas
    stats.strip_dirs().sort_stats('tottime').print_stats(10)
    