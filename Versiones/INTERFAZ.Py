'''
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import radians, sin, cos

# Variable global para almacenar la matriz final
final_rotation = None

# Parámetros de rotación y movimiento
rotation_angle_degrees = 5
rotation_x, rotation_y, rotation_z = 0.0, 0.0, 0.0
cube_position = np.array([0.0, 0.0, 0.0])
camera_position = np.array([10.0, 10.0, 10.0])
camera_target = np.array([0.0, 0.0, 0.0])
move_step = 0.5  # Tamaño del paso para mover el cubo y la cámara

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

def update_plot(ax, fig, canvas):
    """Actualiza la visualización del objeto 3D."""
    ax.clear()

    # Dibujar el eje XYZ
    axis_length = 5
    ax.quiver(0, 0, 0, axis_length, 0, 0, color='red', label='X')
    ax.quiver(0, 0, 0, 0, axis_length, 0, color='green', label='Y')
    ax.quiver(0, 0, 0, 0, 0, axis_length, color='blue', label='Z')

    # Crear un cubo centrado en `cube_position`
    cube_vertices = np.array([[-1, -1, -1],
                              [1, -1, -1],
                              [1, 1, -1],
                              [-1, 1, -1],
                              [-1, -1, 1],
                              [1, -1, 1],
                              [1, 1, 1],
                              [-1, 1, 1]])
    
    # Aplicar matriz de rotación a los vértices del cubo
    rotation_matrix = euler_to_matrix(rotation_x, rotation_y, rotation_z)
    rotated_vertices = np.dot(cube_vertices, rotation_matrix.T) + cube_position

    # Dibujar las líneas del cubo
    edges = [(0, 1), (1, 2), (2, 3), (3, 0),  # Base inferior
             (4, 5), (5, 6), (6, 7), (7, 4),  # Base superior
             (0, 4), (1, 5), (2, 6), (3, 7)]  # Conexiones verticales
    for edge in edges:
        start, end = rotated_vertices[edge[0]], rotated_vertices[edge[1]]
        ax.plot3D(*zip(start, end), color='black')

    # Ajustar cámara
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=camera_position[1], azim=camera_position[0])

    ax.set_title("3D Rotation and Movement")
    ax.legend()

    # Actualizar canvas
    canvas.draw()

def create_3d_scene():
    global final_rotation, rotation_x, rotation_y, rotation_z, cube_position, camera_position

    # Crear ventana principal
    root = tk.Tk()
    root.title("3D Rotation and Movement Scene")

    # Crear figura de matplotlib
    fig = Figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Dibujar el gráfico inicial
    update_plot(ax, fig, canvas)

    def handle_keypress(event):
        """Maneja eventos de teclas para mover o rotar el cubo y la cámara."""
        global rotation_x, rotation_y, rotation_z, cube_position, camera_position
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

        # Movimiento del cubo
        if key == 'Up':
            cube_position[1] += move_step
        elif key == 'Down':
            cube_position[1] -= move_step
        elif key == 'Left':
            cube_position[0] -= move_step
        elif key == 'Right':
            cube_position[0] += move_step
        elif key == 'w':
            cube_position[2] += move_step
        elif key == 's':
            cube_position[2] -= move_step

        # Movimiento de la cámara
        if key == 'i':
            camera_position[1] += move_step
        elif key == 'k':
            camera_position[1] -= move_step
        elif key == 'j':
            camera_position[0] -= move_step
        elif key == 'l':
            camera_position[0] += move_step

        update_plot(ax, fig, canvas)

    def save_rotation():
        """Guardar la matriz de rotación final."""
        global final_rotation
        final_rotation = euler_to_matrix(rotation_x, rotation_y, rotation_z)
        messagebox.showinfo("Saved", f"Matrix Saved:\n{final_rotation}")

    def close_window():
        """Cerrar la ventana."""
        root.destroy()

    # Botones para guardar y cerrar
    button_frame = tk.Frame(root)
    button_frame.pack()
    save_button = tk.Button(button_frame, text="Save Rotation", command=save_rotation)
    save_button.pack(side=tk.LEFT)
    close_button = tk.Button(button_frame, text="Close", command=close_window)
    close_button.pack(side=tk.LEFT)

    # Vincular las teclas para movimiento y rotación
    root.bind("<KeyPress>", handle_keypress)

    # Ejecutar la ventana
    root.mainloop()

    return final_rotation

# Ejecutar la escena
matrix = create_3d_scene()
print("Final Rotation Matrix:", matrix)
'''
'''
import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import radians, sin, cos

# Variables globales
rotation_x, rotation_y, rotation_z = 0.0, 0.0, 0.0
plane_position = np.array([0.0, 0.0, 0.0])
camera_elevation = 30.0
camera_azimuth = 45.0
rotation_matrix = np.eye(3)  # Matriz de rotación inicial

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

def update_plot(ax, fig, canvas):
    """Actualiza la visualización del plano."""
    ax.clear()

    # Dibujar el eje XYZ
    axis_length = 5
    ax.quiver(0, 0, 0, axis_length, 0, 0, color='red', label='X')
    ax.quiver(0, 0, 0, 0, axis_length, 0, color='green', label='Y')
    ax.quiver(0, 0, 0, 0, 0, axis_length, color='blue', label='Z')

    # Crear un plano 2D
    grid_size = 5
    x = np.linspace(-grid_size, grid_size, 10)
    y = np.linspace(-grid_size, grid_size, 10)
    x, y = np.meshgrid(x, y)
    z = np.zeros_like(x)

    # Aplicar rotación y traslación
    global rotation_matrix
    points = np.stack((x.flatten(), y.flatten(), z.flatten()), axis=1)
    rotated_points = np.dot(points, rotation_matrix.T)
    rotated_points += plane_position

    x_rot, y_rot, z_rot = rotated_points[:, 0], rotated_points[:, 1], rotated_points[:, 2]
    x_rot = x_rot.reshape(x.shape)
    y_rot = y_rot.reshape(y.shape)
    z_rot = z_rot.reshape(z.shape)

    ax.plot_surface(x_rot, y_rot, z_rot, alpha=0.5, color='cyan')

    # Configurar cámara
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])
    ax.view_init(elev=camera_elevation, azim=camera_azimuth)

    ax.set_title("3D Plane Movement")
    ax.legend()
    canvas.draw()

def create_3d_scene():
    global rotation_x, rotation_y, rotation_z, plane_position, camera_elevation, camera_azimuth, rotation_matrix

    root = tk.Tk()
    root.title("3D Plane Viewer")

    # Crear figura 3D
    fig = Figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Funciones
    def rotate(axis, angle):
        """Rota el plano alrededor de un eje."""
        global rotation_matrix
        if axis == 'x':
            rotation_matrix = np.dot(euler_to_matrix(angle, 0, 0), rotation_matrix)
        elif axis == 'y':
            rotation_matrix = np.dot(euler_to_matrix(0, angle, 0), rotation_matrix)
        elif axis == 'z':
            rotation_matrix = np.dot(euler_to_matrix(0, 0, angle), rotation_matrix)
        update_plot(ax, fig, canvas)

    def move_camera(direction):
        """Mueve la cámara ajustando elevación o azimuth."""
        global camera_elevation, camera_azimuth
        if direction == 'up':
            camera_elevation += 5
        elif direction == 'down':
            camera_elevation -= 5
        elif direction == 'left':
            camera_azimuth -= 5
        elif direction == 'right':
            camera_azimuth += 5
        update_plot(ax, fig, canvas)

    def save_matrix():
        """Guarda la matriz de rotación en un archivo."""
        with open("rotation_matrix.txt", "w") as f:
            np.savetxt(f, rotation_matrix, fmt="%.4f")
        messagebox.showinfo("Guardado", "Matriz de rotación guardada en 'rotation_matrix.txt'.")

    def load_matrix():
        """Permite ingresar una matriz personalizada."""
        try:
            matrix_input = simpledialog.askstring("Ingresar Matriz", "Introduce una matriz 3x3 separada por comas:")
            if matrix_input:
                rows = matrix_input.split(";")
                new_matrix = np.array([list(map(float, row.split(","))) for row in rows])
                if new_matrix.shape == (3, 3):
                    global rotation_matrix
                    rotation_matrix = new_matrix
                    update_plot(ax, fig, canvas)
                else:
                    raise ValueError
        except Exception:
            messagebox.showerror("Error", "La matriz ingresada no es válida. Asegúrate de que tenga dimensiones 3x3.")

    # Crear botones
    button_frame = tk.Frame(root)
    button_frame.pack()

    tk.Button(button_frame, text="Rotar X+", command=lambda: rotate('x', radians(10))).grid(row=0, column=0)
    tk.Button(button_frame, text="Rotar Y+", command=lambda: rotate('y', radians(10))).grid(row=0, column=1)
    tk.Button(button_frame, text="Rotar Z+", command=lambda: rotate('z', radians(10))).grid(row=0, column=2)

    tk.Button(button_frame, text="Camara Arriba", command=lambda: move_camera('up')).grid(row=1, column=0)
    tk.Button(button_frame, text="Camara Abajo", command=lambda: move_camera('down')).grid(row=1, column=1)
    tk.Button(button_frame, text="Camara Izquierda", command=lambda: move_camera('left')).grid(row=1, column=2)
    tk.Button(button_frame, text="Camara Derecha", command=lambda: move_camera('right')).grid(row=1, column=3)

    tk.Button(button_frame, text="Guardar Matriz", command=save_matrix).grid(row=2, column=0)
    tk.Button(button_frame, text="Cargar Matriz", command=load_matrix).grid(row=2, column=1)
    tk.Button(button_frame, text="Cerrar", command=root.destroy).grid(row=2, column=2)

    # Actualización periódica
    def update_scene():
        update_plot(ax, fig, canvas)
        root.after(16, update_scene)  # Aumenta la tasa de refresco

    update_scene()
    root.mainloop()

# Ejecutar la aplicación
create_3d_scene()
'''
import tkinter as tk
from tkinter import messagebox, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import radians, sin, cos

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



# Ejecutar la escena
matrix = create_3d_scene()
print("Final Rotation Matrix:", matrix)
