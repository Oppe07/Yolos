import os

# Directorios de las carpetas de etiquetas
carpeta_linea = 'D:\Imagenes\Etiqueta_simple\labelY'
carpeta_entrelinea = 'D:\Imagenes\Etiqueta_simple2clases\labelY'
carpeta_salida = 'D:\Imagenes\Etiqueta_simple2clases\labelYC'


# Crear la carpeta de salida si no existe
os.makedirs(carpeta_salida, exist_ok=True)

# Listar los archivos en cada carpeta y convertirlos en conjuntos para comparación
archivos_linea = set(os.listdir(carpeta_linea))
archivos_entrelinea = set(os.listdir(carpeta_entrelinea))

# Obtener solo los archivos con nombres coincidentes en ambas carpetas
archivos_comunes = archivos_linea.intersection(archivos_entrelinea)

for archivo in archivos_comunes:
    # Leer etiquetas de la carpeta de línea
    with open(os.path.join(carpeta_linea, archivo), 'r') as f:
        etiquetas_linea = f.readlines()

    # Leer etiquetas de la carpeta de entrelínea y modificar la clase
    etiquetas_entrelinea_modificadas = []
    with open(os.path.join(carpeta_entrelinea, archivo), 'r') as f:
        for linea in f:
            partes = linea.strip().split()
            if partes[0] == '0':
                partes[0] = '1'  # Cambiar clase 0 a 1
            etiquetas_entrelinea_modificadas.append(' '.join(partes) + '\n')

    # Combinar etiquetas
    etiquetas_combinadas = etiquetas_linea + etiquetas_entrelinea_modificadas

    # Guardar en el archivo de salida
    with open(os.path.join(carpeta_salida, archivo), 'w') as f:
        f.writelines(etiquetas_combinadas)

print("Etiquetas combinadas y guardadas en la carpeta de salida para los archivos coincidentes.")
