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


#Introduce you angular tolerance
AH = 45  # Angular sector

#Introduce you normal tolerance / bins
VH = 25  # Step / Normal Tolerance

#Select you variables

VAR = "Al" # Variable 1
VAR2 = "Co" # Variable 2
# Variable global para almacenar la matriz final
final_rotation = None

# Parámetros de rotación y movimiento
rotation_angle_degrees = 5
rotation_x, rotation_y, rotation_z = 0.0, 0.0, 0.0
plane_position = np.array([0.0, 0.0, 0.0])
camera_position = np.array([10.0, 10.0, 10.0])
camera_target = np.array([0.0, 0.0, 0.0])
move_step = 1  # Tamaño del paso para mover el plano y la cámara
'''
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
'''
final_rotation = [[0.4698463103929543, -0.8660254037844386, 0.17101007166283438], 
                [0.8137976813493737, 0.5000000000000001, 0.2961981327260238], 
                  [-0.3420201433256687, 0.0, 0.9396926207859084]]
#mirar cuando puedo utilizar la final rotation 

def load_data(input_file=None, default_file='test_data.csv'):

    # Determine the file path
    if input_file is None:
        input_file = os.path.join(os.path.dirname(__file__), default_file)
    
    # Get absolute path and validate existence
    input_file = os.path.abspath(input_file)
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"File not found: {input_file}")
    
    print(f"Input file: {input_file}")
    return input_file
'''
#Applied the rotation to the imput file
def apply_rotation(input_file):
    
    # Aplying rotation
    data = pd.read_csv(input_file)  # Read the input file
    x = data['x'].values  # Convert column to NumPy array
    y = data['y'].values  # Convert column to NumPy array
    z = data['Z'].values  # Convert column to NumPy array
    
    positions = np.vstack((x, y, z))  # Stack x, y, z as a 2D array
    rotated_positions = np.dot(final_rotation, positions)  # Apply rotation
    rotated_positions = rotated_positions.T

    # Convert VAR and VAR2 to NumPy arrays
    var = data[VAR].values.astype(float)  # Convert VAR to NumPy array
    var2 = data[VAR2].values.astype(float)  # Convert VAR2 to NumPy array
    
    # Optionally, you can return all data as a dictionary or individual arrays
    return {
        'rotated_positions': rotated_positions,
        'xr': rotated_positions[:, 0],
        'yr': rotated_positions[:, 1],
        'zr': rotated_positions[:, 2],
        'VAR': var,
        'VAR2': var2
    }
    
'''
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


# ADDING THE ID 
def add_ids(rotated_positions):
    # Crear un array con IDs enteros y posiciones concatenados
    rotated_positions_with_ids = np.column_stack((np.arange(len(rotated_positions), dtype=int), rotated_positions))
    return rotated_positions_with_ids

## ## ##


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


## ## ##


# CLASSIFYING DISTANCES
'''
def classify_distances(distances, pairs, AH):
    def classify_increment(distance_x, distance_y):
        # Calculando los ángulos
        angle = np.degrees(np.arctan2(distance_y, distance_x))
        angle[angle < 0] += 360  # Corrigiendo ángulos negativos
        angle = angle % 180  # Reducción a [0, 180)
        return (angle // AH).astype(int)

    # Clasificando los sectores con incrementos de distancia
    sectors = classify_increment(distances['Distance_x'], distances['Distance_y'])
    
    #Agregar 'sector' al diccionario de distances
    distances['sector'] = sectors
    
    #Asignar los sectores correspondientes a los pares
    ID_1 = pairs['ID_1'].astype(int) - 1  # Restamos 1 ya que los índices de pairs inician en 1
    pairs['sector'] = distances['sector'][ID_1]  # Asignar sector a los pares usando indexación

    return distances, pairs



def classify_distances(distances, pairs, AH):
    # Cálculo directo de sectores basado en los ángulos
    angles = np.degrees(np.arctan2(distances['Distance_y'], distances['Distance_x'])) % 180
    distances['sector'] = (angles // AH).astype(int)
    
    # Asignación de sectores a los pares
    pairs['sector'] = distances['sector'][pairs['ID_1'] - 1]  # Indexación directa ajustada a Python
    ID_1 = pairs['ID_1'].astype(int) -1 # Restamos 1 ya que los índices de pairs inician en 1
    pairs['sector'] = distances['sector'][ID_1]
    
    return distances, pairs
'''

def classify_distances(distances, pairs, AH):
    # Cálculo de sectores basado en los ángulos
    angles = np.degrees(np.arctan2(distances['Distance_y'], distances['Distance_x'])) % 180
    distances['sector'] = (angles // AH).astype(int)
    
    
    # Ajuste para pares: calculamos índices (0-based)
    ID_1_indices = pairs['ID_1'].astype(int) - 1  # Convertir a entero y ajustar índice
    if np.any(ID_1_indices < 0) or np.any(ID_1_indices >= len(distances['sector'])):
        raise IndexError("ID_1 contiene valores fuera del rango de distances['sector']")

    # Asignación de sectores a los pares
    pairs['sector'] = distances['sector'][ID_1_indices]  # Indexación directa ajustada a Python
    
    pairs['ID_1'] = pairs['ID_1'].astype(int)   
    pairs['ID_2'] = pairs['ID_2'].astype(int)

    print("pairs['ID_1'] dtype:", pairs['ID_1'].dtype)
    print("ID_1_indices dtype:", ID_1_indices.dtype)
    print("distances['sector'] dtype:", distances['sector'].dtype)

    return distances, pairs

###########################################################################################

# Clasify en longitudinal areas

def classify_point_in_longitudinal_areas(distances, pairs):
    '''
    def classify_normal(distance_x, distance_y, sector):
        angle_bisectrix = sector * AH + (AH / 2)
        angle_rad = np.radians(angle_bisectrix)
        dx = np.cos(angle_rad)
        dy = np.sin(angle_rad)
        x_rel = distance_x
        y_rel = distance_y
        width = AH
        
        
        proj = x_rel * dx + y_rel * dy
        b = np.sqrt(distance_x**2 + distance_y**2 - proj**2)
        # Verificación si la variable está dentro de la normal
        return b <= (width / 2)
    '''
    ##################################################################################### OTRA OPCION DE CODIGO
    
    # Precalcula ángulos y anchura si AH es constante y se tiene un número fijo de sectores
    angle_cache = {}
    half_width_squared = (AH / 2) ** 2
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






# Calcular el step 

def step(distances, pairs):
    global VH
    
    # Crear una máscara para obtener solo los IDs en común entre distances y pairs
    mask = np.isin(distances['ID_1'], pairs['ID_1']) & np.isin(distances['ID_2'], pairs['ID_2'])
    
    # Obtener los índices donde la máscara es True
    indices = np.where(mask)[0]
    
    # Aplicar los índices a distance_x y distance_y asegurando que sean unidimensionales
    distance_x = distances['Distance_x'][indices].flatten()
    distance_y = distances['Distance_y'][indices].flatten()
    
    # Calcular el valor de 'step'
    step_values = np.round((distance_x**2 + distance_y**2) / (VH**2)).astype(int) ##################### Revisar
    
    # Asignar los valores de 'step' a los pares filtrados
    pairs['step'] = step_values
    
    return pairs



def create_var_dicts(var, var2):
    # Crear un array de IDs, partiendo desde 1
    num_elements = len(var)
    ids = np.arange(1, num_elements + 1)
    
    # Crear dos diccionarios separados
    var_dict = {
        'ID': ids,
        'VAR': var
    }
    var2_dict = {
        'ID': ids,
        'VAR2': var2
    }
    
    return var_dict, var2_dict



def diferencias(pairs, var_dict, var2_dict):
    # Inicializar listas para almacenar los resultados
    
    var_diffs_squared = []
    var2_diffs_squared = []

    # Asegúrate de que ID_1 y ID_2 son enteros
    id_1_indices = pairs['ID_1']
    id_2_indices = pairs['ID_2']
    
    # Crear diccionarios que mapean los IDs a los valores correspondientes en VAR y VAR2
    var_map = dict(zip(var_dict['ID'], var_dict['VAR']))
    var2_map = dict(zip(var2_dict['ID'], var2_dict['VAR2']))

    # Calcular las variaciones al cuadrado utilizando los valores de `VAR` y `VAR2` en los diccionarios
    for id_1, id_2 in zip(id_1_indices, id_2_indices):
        var_diffs_squared.append((var_map[id_2] - var_map[id_1]) ** 2)
        var2_diffs_squared.append((var2_map[id_2] - var2_map[id_1]) ** 2)

    # Añadir los resultados como nuevos arrays en el diccionario existente de `pairs`
    pairs['VAR'] = np.array(var_diffs_squared)
    pairs['VAR2'] = np.array(var2_diffs_squared)
    
    return pairs

'''
def variogram(pairs, VH):
    # Calcular el máximo del 'step' y definir los límites de los bins
    max_step = np.max(pairs['step'])
    bin_limits = list(range(0, int(max_step + VH), int(VH)))

    # Inicializar lista para almacenar los resultados
    results = []

    # Agrupar datos por sector y bin de step
    for sector in np.unique(pairs['sector']):
        # Filtrar solo los datos del sector actual
        sector_indices = np.where(pairs['sector'] == sector)[0]
        sector_steps = np.array(pairs['step'])[sector_indices]
        sector_VAR = np.array(pairs['VAR'])[sector_indices]

        # Clasificar los steps de este sector en los bins
        sector_step_bins = np.digitize(sector_steps, bins=bin_limits, right=True)

        for bin_index in range(1, len(bin_limits)):
            # Crear una máscara para los datos que caen en el bin actual
            bin_mask = sector_step_bins == bin_index

            if np.any(bin_mask):  # Solo si hay datos en el bin
                media_VAR_cuadrado = np.mean(sector_VAR[bin_mask])  # VAR ya contiene el valor al cuadrado
                media_step = np.mean(sector_steps[bin_mask])
            else:
                media_VAR_cuadrado = 0  # o np.nan si prefieres indicar que el bin está vacío
                media_step = (bin_limits[bin_index - 1] + bin_limits[bin_index]) / 2  # Centro del bin

            # Agregar resultados a la lista
            results.append({
                'step_bin': bin_limits[bin_index - 1],
                'sector': sector,
                'media_VAR_cuadrado': media_VAR_cuadrado,
                'media_step': media_step
            })

    # Convertir los resultados en un DataFrame para graficar
    result_df = pd.DataFrame(results)

    # Graficar
    plt.figure(figsize=(10, 6))
    
    for sector in result_df['sector'].unique():
        sector_data = result_df[result_df['sector'] == sector]
        plt.plot(sector_data['media_step'], sector_data['media_VAR_cuadrado'], 
                 marker='o', label=f'Sector {sector}')
    
    plt.xlabel('Step')
    plt.ylabel('VAR al Cuadrado')
    plt.title('Variogram cloud')
    plt.legend(title='Sector')
    plt.grid(True)

    return pairs
'''

def variogram(pairs, VH):
    # Calcular el máximo del 'step' y definir los límites de los bins
    max_step = np.max(pairs['step'])
    bin_limits = list(range(0, int(max_step + VH), int(VH)))

    # Inicializar lista para almacenar los resultados
    results = []

    # Agrupar datos por sector
    for sector in np.unique(pairs['sector']):
        # Filtrar datos del sector actual
        sector_indices = np.where(pairs['sector'] == sector)[0]
        sector_steps = np.array(pairs['step'])[sector_indices]
        sector_VAR = np.array(pairs['VAR'])[sector_indices]

        # Clasificar los steps de este sector en los bins
        sector_step_bins = np.digitize(sector_steps, bins=bin_limits, right=True)

        # Calcular medias de step y VAR por bin dentro del sector
        for bin_index in range(1, len(bin_limits)):
            # Máscara para datos en el bin actual
            bin_mask = sector_step_bins == bin_index

            if np.any(bin_mask):  # Solo si hay datos en el bin
                # Calcular media de 'step' y media de 'VAR' en el bin actual
                media_step = np.mean(sector_steps[bin_mask])
                media_VAR = np.mean(sector_VAR[bin_mask])  # VAR ya contiene el valor al cuadrado
            else:
                # Definir valores para bins vacíos
                media_step = (bin_limits[bin_index - 1] + bin_limits[bin_index]) / 2
                media_VAR = 0  # o np.nan si prefieres indicar que el bin está vacío

            # Agregar resultados a la lista
            results.append({
                'step_bin': bin_limits[bin_index - 1],
                'sector': sector,
                'media_VAR': media_VAR,
                'media_step': media_step
            })

    # Convertir los resultados en un DataFrame para graficar
    result_df = pd.DataFrame(results)

    # Graficar
    plt.figure(figsize=(10, 6))
    
    for sector in result_df['sector'].unique():
        sector_data = result_df[result_df['sector'] == sector]
        plt.plot(sector_data['media_step'], sector_data['media_VAR'], 
                 marker='o', label=f'Sector {sector}')
    
    plt.xlabel('Step')
    plt.ylabel('Media de VAR')
    plt.title('Variogram cloud')
    plt.legend(title='Sector')
    plt.grid(True)

    return result_df

# MODIFICAR LA VARIABLE STEP QUE NO SEA UN INT


def main(): 
    # Ejecutar la escena
    #matrix = create_3d_scene()
    #print("Final Rotation Matrix:", matrix)
    input_file = "C:\\Users\\marsa\\OneDrive\\GitHUB\\Objective\\test_data.csv"
    input_file = load_data(input_file)
    
    
    
    puntos_rotados = apply_rotation(input_file)
    rotated_positions = puntos_rotados['rotated_positions']
    var = puntos_rotados['VAR']
    var2 = puntos_rotados['VAR2']
    
    '''
        print(type(x), x.shape)
        print(type(y), y.shape)
        print(type(z), z.shape)
        print("Formato de rotated_positions:")
        print("Tipo de dato:", type(rotated_positions))  # Tipo de dato
        print("Dimensiones:", rotated_positions.shape)    # Dimensiones
        print("Tipo de los elementos:", rotated_positions.dtype)  # Tipo de los elementos
        print("Primeras columnas de los puntos rotados:\n", rotated_positions[:, :5])  # Primeras 5 columnas
        print("Rotated Positions Shape:", rotated_positions.shape)  # Imprime las dimensiones
        print("VAR Array:", var)  # Imprime el array VAR
        print("VAR2 Array:", var2)  # Imprime el array VAR2
    '''
    
    
    
    rotated_positions_with_ids = add_ids(rotated_positions)  # Llamar a add_ids
    puntos_rotados['ID'] = rotated_positions_with_ids
    
    
  

    '''
    checks
    print("xr (first 5):", puntos_rotados['rotated_positions'][:5, 0])
    print("yr (first 5):", puntos_rotados['rotated_positions'][:5, 1])
    print("zr (first 5):", puntos_rotados['rotated_positions'][:5, 2])
    print("ID (first 5):", puntos_rotados['ID'][:7])  # Imprime los primeros 5 IDs
    print(puntos_rotados)
    print(puntos_rotados.keys())
    '''
    
    
    
    distances_dict, pairs_dict = generate_pairs(puntos_rotados,VH)
    
    '''
    # Ver las "columnas" (claves) de distances_dict
    print("Columnas en distances_dict:", distances_dict.keys())

    # Ver las "columnas" (claves) de pairs_dict
    print("Columnas en pairs_dict:", pairs_dict.keys())

    # Ver los primeros 10 valores de cada clave en distances_dict
    print("Primeros 10 valores en distances_dict:")
    for key, value in distances_dict.items():
        print(f"{key}: {value[:10]}")

    # Ver los primeros 10 valores de cada clave en pairs_dict
    print("\nPrimeros 10 valores en pairs_dict:")
    for key, value in pairs_dict.items():
        print(f"{key}: {value[:10]}")
    
    print("Tamaño original de los pares:", len(pairs['ID_1']))
    print("Tamaño original de los pares:", len(distances['ID_1']))
    '''



    distances, pairs = classify_distances(distances_dict, pairs_dict, AH)
    
    '''
   # Ver las keys y los primeros valores
    print("Distances keys:", distances_dict.keys())
    print("First few distances:", {k: v[:5] for k, v in distances_dict.items()})
    
    print("\nPairs keys:", pairs_dict.keys())
    print("First few pairs:", {k: v[:5] for k, v in pairs_dict.items()})
    print(type(pairs))
    print(type(distances))
    
    print("pairs['ID_1'] dtype:", pairs['ID_1'].dtype)
    print("distances['sector'] dtype:", distances['sector'].dtype)
    print("Distances keys:", distances_dict.keys())
    print("First few distances:", {k: v[:5] for k, v in distances_dict.items()})
    
    print("\nPairs keys:", pairs_dict.keys())
    print("First few pairs:", {k: v[:5] for k, v in pairs_dict.items()})
    print(type(pairs))
    print(type(distances))
    
    '''
    
    
    pairs = classify_point_in_longitudinal_areas(distances, pairs)
    
    
    
    '''
    print("Distances keys:", distances_dict.keys())
    print("First few distances:", {k: v[:5] for k, v in distances_dict.items()})
    print("\nPairs keys:", pairs_dict.keys())
    print("First few pairs:", {k: v[:5] for k, v in pairs_dict.items()})
    print("Tamaño nuevo de los pares:", len(pairs['ID_1']))
    print("Tamaño nuevo de los pares:", len(distances['ID_1']))
    
    '''
    
    pairs = step(distances, pairs)
    
    '''
    print(pairs.keys())
    print("First few pairs:", {k: v[:5] for k, v in pairs.items()})
    print("Claves de distances antes:", distances.keys())
    
    '''
    var_dict, var2_dict = create_var_dicts(var, var2)
    
    '''
    # Revisar las claves y los primeros valores de cada diccionario
    print("var_dict keys:", var_dict.keys())
    print("var_dict first values:", {k: v[0] for k, v in var_dict.items()})
    
    print("var2_dict keys:", var2_dict.keys())
    print("var2_dict first values:", {k: v[0] for k, v in var2_dict.items()})
    '''
    
    pairs = diferencias(pairs, var_dict, var2_dict)
    
    '''
    print(pairs.keys())
    print({key: value[-20:] for key, value in pairs.items()})
    '''
    pairs = variogram(pairs,VH)
    plt.show()
    
    '''
    print("Valores de step:", pairs['step'])
    print("Valores de step_bins:", step_bins)
    print("Límites de bins:", bin_limits)
    
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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
    
    
