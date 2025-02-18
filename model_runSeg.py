from ultralytics import YOLO
import cv2
import os
import numpy as np

from ultralytics import YOLO

def cargar_modelo(opcion):
    """
    Función para cargar el modelo y configurar el directorio de salida según la opción seleccionada.
    """
    modelos = {
        0: ('D:/Imagenes/Etiqueta_estrecha/runs/segmentation_model18/weights/best.pt',
            r'D:/Imagenes/pruebas_img/ResultadosSeg0/'),
        1: ('D:/Imagenes/Etiqueta_simple/runs/segmentation_model6/weights/best.pt',
            r'D:/Imagenes/pruebas_img/ResultadosSeg1/'),
        2: ('D:/Imagenes/Etiqueta_estrecha2clases/runs/segmentation_model2/weights/best.pt',
            r'D:/Imagenes/pruebas_img/ResultadosSeg2/'),
        3: ('D:/Imagenes/Etiqueta_simple2clases/runs/segmentation_model14/weights/best.pt',
            r'D:/Imagenes/pruebas_img/ResultadosSeg3/')
    }
    
    modelo, output_dir = modelos.get(opcion, (None, None))
    if modelo:
        model = YOLO(modelo)
        print(f"Modelo cargado: {modelo}")
        print(f"Resultados se guardarán en: {output_dir}")
        return model, output_dir
    else:
        print("Opción inválida. Intenta de nuevo.")
        return None, None


"""
Menú principal para seleccionar el modelo.
"""
while True:
    try:
        print("\nSelecciona el modelo de ejecución:")
        print("0: Modelo 18")
        print("1: Modelo 19")
        print("2: Modelo 20")
        print("3: Modelo 21")
        
        opcion = int(input("Ingresa el número correspondiente (0, 1, 2, 3): "))
        
        model, output_dir = cargar_modelo(opcion)
        if model and output_dir:
            # Salir del bucle si la opción es válida
            break
    except ValueError:
        print("Entrada inválida. Por favor, ingresa un número (0, 1, 2, 3).")

print("¡Modelo listo para su uso!")
# Aquí puedes continuar con el procesamiento del modelo y los datos.
    
input_dir = r'D:/Imagenes/pruebas_img/image'  # Directorio con imágenes nuevas



# Crear el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Procesar cada imagen del directorio de entrada
for image_name in os.listdir(input_dir):
    if image_name.lower().endswith(('.jpg', '.jpeg', '.png')):  # Filtro para imágenes
        # Leer la imagen
        image_path = os.path.join(input_dir, image_name)
        image = cv2.imread(image_path)
        
        # Realizar predicción con segmentación
        results = model.predict(source=image, conf=0.25, save=False, task='segment')  # Realizar segmentación
        
        # Extraer la máscara segmentada
        masks = results[0].masks  # Obtiene las máscaras
        if masks is not None:
            mask = masks.data.cpu().numpy()  # Convierte las máscaras a numpy
            
            for single_mask in mask:
                # Redimensionar la máscara segmentada al tamaño de la imagen original
                resized_mask = cv2.resize(single_mask, (image.shape[1], image.shape[0]))
                # Dibujar la máscara en la imagen original
                image[resized_mask > 0.5] = (255, 0, 0)  # Pinta de verde las áreas segmentadas

            # Guardar la imagen con la máscara dibujada
            output_path = os.path.join(output_dir, f"masked_{image_name}")
            cv2.imwrite(output_path, image)

            print(f"Imagen con máscara dibujada guardada en: {output_path}")
        else:
            print(f"No se detectaron máscaras para: {image_name}")

print("Segmentación completada para todas las imágenes.")
