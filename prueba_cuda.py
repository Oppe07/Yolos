import torch
import ultralytics
print("CUDA disponible:", torch.cuda.is_available())
print("Dispositivo GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No detectado")
