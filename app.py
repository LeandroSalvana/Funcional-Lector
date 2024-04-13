from flask import Flask, render_template, request
from pyzxing.pepito import procesar_codigo, redimensionar_imagen
import os


app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/procesar_imagen', methods=['POST'])
def procesar_imagen():
    if 'imagen' not in request.files:
        return 'No se proporcionó ninguna imagen.'
    imagen = request.files['imagen']
    if imagen.filename == '':
        resultado = 'No se seleccionó ningún archivo.'
        return resultado

    # Redimensionar la imagen
    imagen_redimensionada = redimensionar_imagen(imagen)

    # Crear un nombre de archivo temporal
    temp_filename = 'temp_image.png'

    try:
        # Guardar la imagen redimensionada temporalmente en disco
        with open(temp_filename, 'wb') as temp_file:
            temp_file.write(imagen_redimensionada.getvalue())

        # Procesar la imagen con el nombre del archivo temporal
        resultado = procesar_codigo(temp_filename)
        if isinstance(resultado, str):
            # Si el resultado es una cadena, crea un diccionario con un mensaje de error
            resultado = {'error': resultado}
    except Exception as e:
        # Capturar cualquier otro error y devolver un diccionario con un mensaje de error
        resultado = {'error': 'Codigo no encontrada en la imagen'}
    finally:
        # Eliminar el archivo temporal
        os.remove(temp_filename)

    return render_template('resultado.html', resultado=resultado)

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=3020)
    app.run(debug=True)
