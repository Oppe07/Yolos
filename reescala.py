import cv2
import os


input_folder = 'D:/Imagenes/label_bin'
output_folder = 'D:/Imagenes/label_bin512'


os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith('.png') or filename.endswith('.jpg'): 
        
        img = cv2.imread(os.path.join(input_folder, filename))
        img_resized = cv2.resize(img, (512, 512))
        
      
        cv2.imwrite(os.path.join(output_folder, filename), img_resized)
        print(f"Reescalado completado {output_folder, filename}")

print("Reescalado completado.")
