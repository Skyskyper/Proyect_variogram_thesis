# Librerías de interfaz gráfica
import tkinter as tk
from tkinter import messagebox, simpledialog
# Librerías para gráficos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# Librerías de cálculo y manipulación de datos
import numpy as np
from math import radians, sin, cos
# Librerías para visualización 3D
from vpython import radians, cos, sin
from vpython import *  # Ten cuidado con el uso de `*`, puede causar conflictos.




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

final_rotation = [[0.4698463103929543, -0.8660254037844386, 0.17101007166283438], 
                [0.8137976813493737, 0.5000000000000001, 0.2961981327260238], 
                  [-0.3420201433256687, 0.0, 0.9396926207859084]]