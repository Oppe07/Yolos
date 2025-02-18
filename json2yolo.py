import json
import os
import cv2
import numpy as np

def labelme_to_yolo_segmentation(json_file, image_file, output_file):
    # Abre el archivo JSON generado por Labelme
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Carga la imagen original
    #print(f'{image_file}')
    img = cv2.imread(image_file)
    h, w, _ = img.shape
    
    with open(output_file, 'w') as out_file:
        for shape in data['shapes']:
            label = shape['label']
            points = np.array(shape['points'])
            
            # Normaliza las coordenadas del polígono
            points[:, 0] /= w  # Normaliza X
            points[:, 1] /= h  # Normaliza Y
            
            # Calcula las coordenadas del bounding box en formato YOLO (relativas)
            xmin, ymin = np.min(points, axis=0)
            xmax, ymax = np.max(points, axis=0)
            x_center = (xmin + xmax) / 2
            y_center = (ymin + ymax) / 2
            bbox_width = (xmax - xmin)
            bbox_height = (ymax - ymin)
            
            # Aquí puedes asignar un número a cada clase
            class_id = 0  # Si solo tienes una clase
            
            # Convierte los puntos del polígono a una lista de coordenadas
            polygon_points = points.flatten().tolist()
            
            # Escribe la anotación en formato YOLO con segmentación (clase, bounding box y coordenadas del polígono)
            #yolo_format = [class_id, x_center, y_center, bbox_width, bbox_height] + polygon_points
            yolo_format = [class_id] + polygon_points
            out_file.write(" ".join(map(str, yolo_format)) + '\n')






def rename_images_in_folder(folder_path):



    # Recorrer cada archivo en la carpeta
    for filename in os.listdir(folder_path):
        # Filtrar solo archivos de imagen (ejemplo: .jpg, .png)
        if filename.endswith('.json'):
            # Obtener la extensión del archivo
            file_extension = os.path.splitext(filename)[1]
            
            # Crear el nuevo nombre del archivo
            new_name = f"{os.path.splitext(filename)[0]}{file_extension}"
            #new_name = new_name[5:] #++++++++++++++++++++++++++++++++++++++++++++++editado para etiquetas linea##
            
            # Obtener la ruta completa de los archivos antiguo y nuevo
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)
            
            # Renombrar el archivo
            os.rename(old_path, new_path)
            print(f"{filename} renombrado a {new_name} en la ubicacion {folder_path}")
            
            

def recorrido_archivos (folder_path_label,foldetr_path_img,img_format,save_path):

    # Recorrer cada archivo en la carpeta
    for filename in os.listdir(folder_path_label):
        # Filtrar solo archivos de imagen (ejemplo: .jpg, .png)
        if filename.endswith('.json'):
            # Obtener la ruta completa de la imagen
            json_path = os.path.join(folder_path_label, filename)
            name = filename.split('.')
            img_path = f'{foldetr_path_img}/{name[0]}'+'.'+img_format
            out_path = f'{save_path}/{name[0]}.txt'
            print (f'+++++++++++++++++++++++++{out_path}++++++++++++++++++++++++++++++++++')
            
            # Aquí puedes procesar cada imagen, por ejemplo, imprimir su nombre
            print(f"Procesando archivos: {json_path}, {img_path}, {out_path}")

            labelme_to_yolo_segmentation(json_path, img_path, out_path)


#rename_images_in_folder('D:\Imagenes\Etiqueta_simple\label')
#recorrido_archivos('D:\Imagenes\Etiqueta_simple2clases\label','D:\Imagenes\Etiqueta_simple2clases\image','jpg','D:\Imagenes\Etiqueta_simple2clases\labelY')
recorrido_archivos('C:/Users/higar/OneDrive/Escritorio/labels_presentacion/label','C:/Users/higar/OneDrive/Escritorio/labels_presentacion/image','jpg','C:/Users/higar/OneDrive/Escritorio/labels_presentacion/labelY')

