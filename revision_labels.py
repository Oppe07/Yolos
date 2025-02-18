import os
import cv2
import numpy as np
'''
# Ruta de las imágenes y etiquetas
image_dir = r'D:/Imagenes/Etiqueta_simple2clases/image'  # Cambia a tu directorio de imágenes
label_dir = r'D:/Imagenes/Etiqueta_simple2clases/labelYC'  # Cambia a tu directorio de etiquetas
output_dir = r'D:/Imagenes/Etiqueta_simple2clases/revision_labels'  # Directorio donde guardar imágenes con etiquetas
'''
image_dir = r'C:/Users/higar/OneDrive/Escritorio/labels_presentacion/image'  # Cambia a tu directorio de imágenes
label_dir = r'C:/Users/higar/OneDrive/Escritorio/labels_presentacion/labelY'  # Cambia a tu directorio de etiquetas
output_dir = r'C:/Users/higar/OneDrive/Escritorio/labels_presentacion/revision_labels'  # Directorio donde guardar imágenes con etiquetas

os.makedirs(output_dir, exist_ok=True)

# Definir colores para cada clase
class_colors = {
    0: (0, 255, 0),   # Clase 0: Verde
    1: (255, 0, 0)    # Clase 1: Rojo
}

# Función para dibujar la máscara de segmentación
def draw_segmentation(image, mask_points, color, alpha=0.5):
    overlay = image.copy()
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    mask_points = np.array(mask_points, dtype=np.int32)
    cv2.fillPoly(mask, [mask_points], 255)
    overlay[mask == 255] = color
    return cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

# Iterar sobre las imágenes
for image_name in os.listdir(image_dir):
    if not image_name.endswith(('.jpg', '.png', '.jpeg')):  # Verificar formatos válidos
        continue

    # Cargar imagen
    image_path = os.path.join(image_dir, image_name)
    image = cv2.imread(image_path)
    h, w, _ = image.shape

    # Cargar etiqueta correspondiente
    label_path = os.path.join(label_dir, os.path.splitext(image_name)[0] + '.txt')
    if not os.path.exists(label_path):
        print(f"No se encontró etiqueta para {image_name}")
        continue

    # Leer y procesar las etiquetas
    with open(label_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])  # Identificador de clase
        mask_coordinates = np.array(parts[1:], dtype=float).reshape(-1, 2)

        # Convertir coordenadas normalizadas a píxeles
        mask_coordinates[:, 0] *= w
        mask_coordinates[:, 1] *= h

        # Seleccionar color según la clase
        color = class_colors.get(class_id, (255, 255, 255))  # Blanco si la clase no está definida

        # Dibujar máscara sobre la imagen
        image = draw_segmentation(image, mask_coordinates, color, alpha=0.5)

        # Agregar identificador de clase como texto
        x, y = int(mask_coordinates[0][0]), int(mask_coordinates[0][1])
        cv2.putText(image, f"Clase {class_id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    # Guardar la imagen con las etiquetas dibujadas
    output_path = os.path.join(output_dir, image_name)
    cv2.imwrite(output_path, image)

print("Visualizaciones guardadas en:", output_dir)
