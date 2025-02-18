import os
import shutil
import random

def split_dataset_with_labels(image_folder, label_folder, output_folder, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    # Verificar que los ratios sumen 1
    if train_ratio + val_ratio + test_ratio != 1.0:
        raise ValueError("La suma de train_ratio, val_ratio y test_ratio debe ser 1.")
    
    # Crear carpetas de destino
    for subset in ["train", "val", "test"]:
        os.makedirs(os.path.join(output_folder, "images", subset), exist_ok=True)
        os.makedirs(os.path.join(output_folder, "labels", subset), exist_ok=True)
    
    # Obtener lista de archivos de imagen en la carpeta
    images = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    # Mezclar aleatoriamente la lista de imágenes
    random.shuffle(images)
    
    # Calcular la cantidad de imágenes para cada conjunto
    train_count = int(len(images) * train_ratio)
    val_count = int(len(images) * val_ratio)
    
    # Dividir las imágenes en los conjuntos
    train_images = images[:train_count]
    val_images = images[train_count:train_count + val_count]
    test_images = images[train_count + val_count:]
    
    # Función para copiar imágenes y etiquetas correspondientes
    def copy_images_and_labels(image_list, subset):
        for image in image_list:
            # Ruta de la imagen y de la etiqueta correspondiente
            image_path = os.path.join(image_folder, image)
            label_path = os.path.join(label_folder, os.path.splitext(image)[0] + '.txt')  # Cambiar .txt si las etiquetas tienen otro formato
            
            # Rutas de destino
            dest_image_path = os.path.join(output_folder, "images", subset, image)
            dest_label_path = os.path.join(output_folder, "labels", subset, os.path.basename(label_path))
            
            # Copiar la imagen
            #shutil.copy(image_path, dest_image_path)
            
            # Copiar la etiqueta si existe
            if os.path.exists(label_path):
                shutil.copy(label_path, dest_label_path)
                shutil.copy(image_path, dest_image_path)
            else:
                print(f"Advertencia: No se encontró etiqueta para {image}")

    
    # Copiar las imágenes y etiquetas a sus carpetas correspondientes
    copy_images_and_labels(train_images, "train")
    copy_images_and_labels(val_images, "val")
    copy_images_and_labels(test_images, "test")
    
    print("División completada:")
    print(f"Entrenamiento: {len(train_images)} imágenes")
    print(f"Validación: {len(val_images)} imágenes")
    print(f"Prueba: {len(test_images)} imágenes")

# Uso del script
split_dataset_with_labels('D:\Imagenes\Etiqueta_simple2clases\image', 'D:\Imagenes\Etiqueta_simple2clases\labelYC', 'D:\Imagenes\Etiqueta_simple2clases\YOLODataset', train_ratio=0.7, val_ratio=0.15, test_ratio=0.15)
