from pyzxing import BarCodeReader
from io import BytesIO
import cv2
import numpy as np


def procesar_codigo(imagen):
#Esto es de la libreria
    reader = BarCodeReader()
    results = reader.decode(imagen)

#----------------Aca esta la magia----------------------
    for diccionario in results:
        if len(diccionario) == 1:       
            return("Codigo no encontrado")
        else:
        #Accedo al indice 0 de la lista que me devuelve (que es un diccionario)
            raw = results[0]
            valor_raw = raw["raw"]
            valor_raw = valor_raw.decode("utf-8")
            valor_raw = valor_raw.replace("NXX","Ñ")
            valor_raw = valor_raw.split("@")
            llave_lista = ["N° de Tramite", "Apellido", "Nombre", "Sexo","N° Dni", "Tipo", "Fecha de Nacimiento", "Fecha de emisión"]
            objeto_raw = {llave:valor for llave, valor in zip(llave_lista, valor_raw[:8])}
            return (objeto_raw)


def redimensionar_imagen(imagen):
    # Lee los datos de la imagen y almacénalos en una variable en memoria
    imagen_data = BytesIO(imagen.read())

    # Carga la imagen utilizando OpenCV
    img_array = np.frombuffer(imagen_data.getvalue(), dtype=np.uint8)
    imagen_cv2 = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Obtén las dimensiones de la imagen
    alto, ancho = imagen_cv2.shape[:2]

    # Define el porcentaje de redimensionamiento que deseas aplicar
    porcentaje_redimensionamiento = 0.6  # Ajusta este valor según tus necesidades

    # Calcula las nuevas dimensiones de la imagen
    nuevo_alto = int(alto * porcentaje_redimensionamiento)
    nuevo_ancho = int(ancho * porcentaje_redimensionamiento)

    # Redimensiona la imagen
    imagen_redimensionada = cv2.resize(imagen_cv2, (nuevo_ancho, nuevo_alto))

    # Convierte la imagen redimensionada de nuevo a BytesIO
    _, buffer = cv2.imencode('.png', imagen_redimensionada)
    imagen_redimensionada_bytesio = BytesIO(buffer)

    return imagen_redimensionada_bytesio