import cv2
import numpy as np

# Configuración de la imagen de salida
image_width = 640  # Ajusta según tu imagen
image_height = 640

# Ruta del archivo de etiquetas YOLO
label_path = "C:/Users/higar/OneDrive/Escritorio/labels_presentacion/labelY/0.txt"  # Ajusta según tu archivo

# Leer archivo de etiquetas
with open(label_path, "r") as file:
    lines = file.readlines()

# Crear imagen en negro para la máscara
mask = np.zeros((image_height, image_width), dtype=np.uint8)

# Procesar cada línea de la etiqueta YOLO
for line in lines:
    values = line.strip().split()
    class_id = int(values[0])  # Clase (no se usa en este caso)
    points = np.array(values[1:], dtype=np.float32).reshape(-1, 2)  # Puntos normalizados

    # Convertir a coordenadas de píxeles
    points[:, 0] *= image_width  # Escalar X
    points[:, 1] *= image_height  # Escalar Y
    points = points.astype(np.int32)  # Convertir a enteros

    # Dibujar polígono en la máscara
    cv2.fillPoly(mask, [points], 255)

# Guardar la máscara como imagen binaria
cv2.imwrite("C:/Users/higar/OneDrive/Escritorio/labels_presentacion/labelY/0mask.jpg", mask)

print("Máscara guardada exitosamente.")
