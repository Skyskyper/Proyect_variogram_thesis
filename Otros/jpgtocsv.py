from PIL import Image
import pandas as pd

# Cargar la imagen
imagen = Image.open(r"C:\Users\marsa\OneDrive\GitHub_ordenado\Otros\Captura de pantalla 2025-01-04 172559.png")


# Convertir a escala de grises (opcional)
imagen = imagen.convert("L")

# Convertir la imagen en una lista de píxeles
pixeles = list(imagen.getdata())

# Redimensionar la lista a la forma original de la imagen
ancho, alto = imagen.size
pixeles = [pixeles[i * ancho:(i + 1) * ancho] for i in range(alto)]

# Crear un DataFrame y exportarlo a CSV
df = pd.DataFrame(pixeles)
df.to_csv("imagen.csv", index=False, header=False)

print("¡Archivo CSV generado con éxito!")
