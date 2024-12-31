# Librerías de interfaz gráfica
import tkinter as tk
from tkinter import messagebox, simpledialog

# Librerías para gráficos
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Librerías de cálculo y manipulación de datos
import numpy as np
import pandas as pd
from math import radians, sin, cos
import itertools
import os

# Librerías para visualización 3D
from vpython import radians, cos, sin
from vpython import *  # Ten cuidado con el uso de `*`, puede causar conflictos.

# Librerías para perfilado del código
import cProfile
import pstats

################################################################################################
#VARIABLES
################################################################################################

AH = 45  # Angular sector
VH = 25  # Step / Normal Tolerance
VAR = "Al" # Variable 1
VAR2 = "Co" # Variable 2

################################################################################################
#CREACION DE LA INTERFAZ
################################################################################################

# Variable global para almacenar la matriz final
final_rotation = None
# Parámetros de rotación y movimiento
rotation_angle_degrees = 5
rotation_x, rotation_y, rotation_z = 0.0, 0.0, 0.0
plane_position = np.array([0.0, 0.0, 0.0])
camera_position = np.array([10.0, 10.0, 10.0])
camera_target = np.array([0.0, 0.0, 0.0])
move_step = 1  # Tamaño del paso para mover el plano y la cámara

def euler_to_matrix(rx, ry, rz):
    """Convierte ángulos de Euler a una matriz de rotación."""
    R_x = np.array([[1, 0, 0],
                    [0, cos(rx), -sin(rx)],
                    [0, sin(rx), cos(rx)]])
    R_y = np.array([[cos(ry), 0, sin(ry)],
                    [0, 1, 0],
                    [-sin(ry), 0, cos(ry)]])
    R_z = np.array([[cos(rz), -sin(rz), 0],
                    [sin(rz), cos(rz), 0],
                    [0, 0, 1]])

    return np.dot(np.dot(R_z, R_y), R_x)

def update_plot(ax, fig, canvas, info_label):
    """Actualiza la visualización del objeto 3D y el cuadro de información."""
    ax.clear()

    # Dibujar el eje XYZ
    axis_length = 5
    ax.quiver(0, 0, 0, axis_length, 0, 0, color='red', label='X')
    ax.quiver(0, 0, 0, 0, axis_length, 0, color='green', label='Y')
    ax.quiver(0, 0, 0, 0, 0, axis_length, color='blue', label='Z')

    # Crear un plano centrado en `plane_position`
    plane_vertices = np.array([[-2, -2, 0],
                               [2, -2, 0],
                               [2, 2, 0],
                               [-2, 2, 0]])
    
    # Aplicar matriz de rotación a los vértices del plano
    rotation_matrix = euler_to_matrix(rotation_x, rotation_y, rotation_z)
    rotated_vertices = np.dot(plane_vertices, rotation_matrix.T) + plane_position

    # Dibujar el plano
    ax.add_collection3d(ax.plot_trisurf(rotated_vertices[:, 0], 
                                        rotated_vertices[:, 1], 
                                        rotated_vertices[:, 2], 
                                        color='gray', alpha=0.7))

    # Ajustar cámara
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=camera_position[1], azim=camera_position[0])

    ax.set_title("3D Plane Rotation and Movement")
    ax.legend()

    # Actualizar canvas
    canvas.draw()

    # Actualizar información
    info_label.config(text=f"Rotación: ({np.degrees(rotation_x):.1f}, {np.degrees(rotation_y):.1f}, {np.degrees(rotation_z):.1f})\n"
                           f"Posición del plano: {plane_position}\n"
                           f"Posición de la cámara: {camera_position}")

def create_3d_scene():
    global final_rotation, rotation_x, rotation_y, rotation_z, plane_position, camera_position

    # Crear ventana principal
    root = tk.Tk()
    root.title("3D Rotation and Movement Scene")

    # Crear figura de matplotlib
    fig = Figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Cuadro de información
    info_label = tk.Label(root, text="", justify=tk.LEFT, font=("Arial", 10))
    info_label.pack()

    # Dibujar el gráfico inicial
    update_plot(ax, fig, canvas, info_label)

    def handle_keypress(event):
        """Maneja eventos de teclas para mover o rotar el plano y la cámara."""
        global rotation_x, rotation_y, rotation_z, plane_position, camera_position
        key = event.keysym

        if key == 'a':  # Rotar en Y positivo
            rotation_y += radians(rotation_angle_degrees)
        elif key == 'd':  # Rotar en Y negativo
            rotation_y -= radians(rotation_angle_degrees)
        elif key == 'q':  # Rotar en X positivo
            rotation_x += radians(rotation_angle_degrees)
        elif key == 'e':  # Rotar en X negativo
            rotation_x -= radians(rotation_angle_degrees)
        elif key == 'z':  # Rotar en Z positivo
            rotation_z += radians(rotation_angle_degrees)
        elif key == 'c':  # Rotar en Z negativo
            rotation_z -= radians(rotation_angle_degrees)

        # Movimiento del plano
        if key == 'Up':
            plane_position[1] += move_step
        elif key == 'Down':
            plane_position[1] -= move_step
        elif key == 'Left':
            plane_position[0] -= move_step
        elif key == 'Right':
            plane_position[0] += move_step
        elif key == 'w':
            plane_position[2] += move_step
        elif key == 's':
            plane_position[2] -= move_step

        # Movimiento de la cámara
        if key == 'i':
            camera_position[1] += move_step
        elif key == 'k':
            camera_position[1] -= move_step
        elif key == 'j':
            camera_position[0] -= move_step
        elif key == 'l':
            camera_position[0] += move_step

        update_plot(ax, fig, canvas, info_label)

    def save_rotation():
        """Guardar la matriz de rotación final."""
        global final_rotation
        final_rotation = euler_to_matrix(rotation_x, rotation_y, rotation_z)
        messagebox.showinfo("Saved", f"Matriz Guardada:\n{final_rotation}")

    def input_matrix():
        """Ingresar una matriz personalizada y actualizar la escena."""
        global rotation_x, rotation_y, rotation_z
        matrix_input = simpledialog.askstring("Input Matrix", "Introduce una matriz (3x3):")
        try:
            custom_matrix = np.array(eval(matrix_input))
            if custom_matrix.shape == (3, 3):
                rotation_x, rotation_y, rotation_z = np.arctan2([custom_matrix[2, 1], custom_matrix[2, 0]], custom_matrix[2, 2])
                update_plot(ax, fig, canvas, info_label)
            else:
                raise ValueError
        except Exception as e:
            messagebox.showerror("Error", "La matriz introducida no es válida.")

    def close_window():
        """Cerrar la ventana."""
        root.destroy()

    # Botones para guardar, introducir matriz y cerrar
    button_frame = tk.Frame(root)
    button_frame.pack()
    save_button = tk.Button(button_frame, text="Guardar Rotación", command=save_rotation)
    save_button.pack(side=tk.LEFT)
    input_button = tk.Button(button_frame, text="Introducir Matriz", command=input_matrix)
    input_button.pack(side=tk.LEFT)
    close_button = tk.Button(button_frame, text="Cerrar", command=close_window)
    close_button.pack(side=tk.LEFT)

    # Vincular las teclas para movimiento y rotación
    root.bind("<KeyPress>", handle_keypress)

    # Ejecutar la ventana
    root.mainloop()

    return final_rotation

################################################################################################
#SCRIPT
################################################################################################

def load_data(input_file=None, default_file='test_data.csv'):
    
    """
    Load the input file, defaulting to `test_data.csv` in the current script's directory.
    
    Parameters:
        input_file (str): Path to the input file. If None, use the default file.
        default_file (str): Name of the default file in the current directory.

    Returns:
        str: Absolute path to the input file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    
    # Determine the file path
    if input_file is None:
        input_file = os.path.join(os.path.dirname(__file__), default_file)
    
    # Get absolute path and validate existence
    input_file = os.path.abspath(input_file)
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"File not found: {input_file}")
    
    print(f"Input file: {input_file}")
    return input_file


def apply_rotation(input_file):
    """
    Applies a 3D rotation to the input file and extracts additional variables.

    Parameters:
        input_file (str): Path to the input CSV file.

    Returns:
        dict: Dictionary containing rotated positions and variables.
    """
    # Load the data
    data = pd.read_csv(input_file)

    # Extract position columns and convert to NumPy array (efficient bulk conversion)
    positions = data[['x', 'y', 'Z']].to_numpy().T

    # Apply rotation directly using the global final_rotation
    rotated_positions = np.dot(final_rotation, positions)

    # Extract VAR and VAR2 columns using global variable names
    var, var2 = data[[VAR, VAR2]].to_numpy().T

    # Return results in a dictionary
    return {
        'rotated_positions': rotated_positions.T,  # Include full rotated positions (transposed back)
        'xr': rotated_positions[0],               # Rotated x-coordinates
        'yr': rotated_positions[1],               # Rotated y-coordinates
        'zr': rotated_positions[2],               # Rotated z-coordinates
        'VAR': var,                                # First variable as NumPy array
        'VAR2': var2                               # Second variable as NumPy array
    }

def add_ids(rotated_positions):
    # Crear un array con IDs enteros y posiciones concatenados
    rotated_positions_with_ids = np.column_stack((np.arange(len(rotated_positions), dtype=int), rotated_positions))
    return rotated_positions_with_ids

# GENERATING THE PAIRS 

def generate_pairs(puntos_rotados, VH):
    
    id_list = puntos_rotados['ID'] [:500]  # Acceso al diccionario
    
    # Generación de diferentes iteraciones de pares de muestras
    pairs = list(itertools.combinations(id_list, 2))
    distances = []
    valid_pairs = []
    
    # Crear los diferentes pares
    for id1, id2 in pairs:
        # Obtención de los índices
        idx1 = np.where(puntos_rotados['ID'] == id1)[0][0]
        idx2 = np.where(puntos_rotados['ID'] == id2)[0][0]
        
        # Distancia entre las coordenadas
        x_distance = puntos_rotados['xr'][idx1] - puntos_rotados['xr'][idx2]
        y_distance = puntos_rotados['yr'][idx1] - puntos_rotados['yr'][idx2]
        z_distance = abs(puntos_rotados['zr'][idx1] - puntos_rotados['zr'][idx2])

        # Aplicar la tolerancia vertical con corrección
        if z_distance <= (VH*0.5 ): ############################################################## REVISAR
            distances.append([id1, id2, x_distance, y_distance, z_distance])
            valid_pairs.append([id1, id2])
    
    # Salida en diccionarios de numpy arrays
    pairs_dict = {
        'ID_1': np.array([p[0] for p in valid_pairs]),
        'ID_2': np.array([p[1] for p in valid_pairs])
    }
    
    distances_dict = {
        'ID_1': np.array([d[0] for d in distances]),
        'ID_2': np.array([d[1] for d in distances]),
        'Distance_x': np.array([d[2] for d in distances]),
        'Distance_y': np.array([d[3] for d in distances]),
        'Distance_z': np.array([d[4] for d in distances])
    }
    
    pairs_dict['ID_1'] += 1  # Incrementar todos los valores de ID_1
    pairs_dict['ID_2'] += 1  # Incrementar todos los valores de ID_2
    pairs_dict['ID_1'] = pairs_dict['ID_1'][:, 0]  
    pairs_dict['ID_2'] = pairs_dict['ID_2'][:, 0]
    
    return distances_dict, pairs_dict

def classify_distances(distances, pairs, AH):
    # Cálculo de sectores basado en los ángulos
    angles = np.degrees(np.arctan2(distances['Distance_y'], distances['Distance_x'])) % 180
    distances['sector'] = (angles // AH).astype(int)
    
    # Ajuste para pares: calculamos índices (0-based)
    ID_1_indices = pairs['ID_1'].astype(int) - 1  # Convertir a entero y ajustar índice
    
    # Asignación de sectores a los pares
    pairs['sector'] = distances['sector'][ID_1_indices]  # Indexación directa ajustada a Python
    
    pairs['ID_1'] = pairs['ID_1'].astype(int)   
    pairs['ID_2'] = pairs['ID_2'].astype(int)

    print("ID_1_indices dtype:", ID_1_indices.dtype)

    return distances, pairs



def main(): 
    
    ########################## Ejecucion de la interfaz 
    matrix = create_3d_scene()
    print("Final Rotation Matrix:", matrix)
    
    ############################ Load Data
    input_file = "C:\\Users\\marsa\\OneDrive\\GitHUB\\Objective\\test_data.csv"
    input_file = load_data(input_file)
    
    ######################################## 
    puntos_rotados = apply_rotation(input_file)
    rotated_positions = puntos_rotados['rotated_positions']
    var = puntos_rotados['VAR']
    var2 = puntos_rotados['VAR2']
                          
    rotated_positions_with_ids = add_ids(rotated_positions)  # Llamar a add_ids
    puntos_rotados['ID'] = rotated_positions_with_ids
    
    distances_dict, pairs_dict = generate_pairs(puntos_rotados,VH)
    
    distances, pairs = classify_distances(distances_dict, pairs_dict, AH)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def wrapper_for_profiling():
    # Envoltorio que llama a generate_pairs con los argumentos correctos
    main()
    #distances, pairs = classify_distances(distances, pairs, AH)
    
if __name__ == "__main__":
        
    profiler = cProfile.Profile()
    
    # Colocar los argumentos de la funcion de estudio 
    #distances = {}
    #pairs = {}
    
    profiler.enable()
    wrapper_for_profiling()
    
    # Colocar la funcion de estudio 
    #distances, pairs = wrapper_for_profiling(distances, pairs, AH)
    profiler.disable()

    # Crear un objeto pstats para procesar los resultados
    stats = pstats.Stats(profiler)
    # Ordenar por el tiempo total y mostrar solo las 10 funciones más lentas
    stats.strip_dirs().sort_stats('tottime').print_stats(10)
    
    
