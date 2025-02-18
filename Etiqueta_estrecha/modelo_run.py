from ultralytics import YOLO
import cv2
import os

# Cargar el modelo YOLOv8 previamente entrenado
model = YOLO('D:/Imagenes/Etiqueta_estrecha/runs/segmentation_model18/weights/best.pt')  # Cambia por la ruta de tu modelo YOLOv8 entrenado

# Configuración de directorios
input_dir = r'D:/Imagenes/pruebas_img/image'  # Directorio con imágenes nuevas
output_dir = r'D:/Imagenes/pruebas_img/RelultadosSeg0'  # Directorio para guardar los resultados

# Crear el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Procesar cada imagen del directorio de entrada
for image_name in os.listdir(input_dir):
    if image_name.lower().endswith(('.jpg', '.jpeg', '.png')):  # Filtro para imágenes
        # Leer la imagen
        image_path = os.path.join(input_dir, image_name)
        image = cv2.imread(image_path)
        
        # Realizar predicción
        results = model.predict(source=image, conf=0.25, save=False)  # Ajusta el umbral de confianza
        
        # Dibujar las predicciones en la imagen
        annotated_image = results[0].plot()  # Visualiza y dibuja los resultados
        
        # Guardar la imagen anotada
        output_path = os.path.join(output_dir, image_name)
        cv2.imwrite(output_path, annotated_image)

        print(f"Procesada: {image_name}, guardada en: {output_path}")

print("Todas las imágenes han sido procesadas.")
