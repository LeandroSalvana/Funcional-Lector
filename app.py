from flask import Flask, render_template, request, g
from pyzxing.pepito import procesar_codigo, redimensionar_imagen, tupla_mysql
import os
import mysql.connector
from mysql.connector import IntegrityError, Error as MySQLError

app = Flask(__name__)

# Configuración de la base de datos
app.config['DB_HOST'] = 'localhost'
app.config['DB_USER'] = 'Leandro'
app.config['DB_PASSWORD'] = 'Leandro'
app.config['DB_DATABASE'] = 'dni_lector'

# Función para conectar a la base de datos
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=app.config['DB_HOST'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_DATABASE']
        )
    return g.db

# Función para desconectar de la base de datos
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

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
        else:
            # Obtener la tupla de datos
            tupla = tupla_mysql(temp_filename)
            print(tupla)
            
            # Obtener el cursor de la base de datos
            cursor = get_db().cursor()
            
            # Sentencia SQL para insertar datos
            sentencia = "INSERT INTO dni_datos (n_de_tramite, apellido, nombre, sexo, n_de_dni, tipo, fecha_de_nacimiento, fecha_de_emision) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            
            try:
                # Ejecutar la sentencia SQL
                cursor.execute(sentencia, tupla)
                
                # Confirmar la transacción
                get_db().commit()
            
            except IntegrityError as e:
                # Manejar el error de clave duplicada
                if e.errno == 1062:
                    resultado = {'error': 'Valor duplicado'}
                else:
                    resultado = {'error': 'Código no encontrado'}
            
            finally:
                # Cerrar el cursor
                cursor.close()   
                
    except MySQLError as e:
        # Capturar cualquier otro error de MySQL
        resultado = {'error': 'Error de base de datos: ' + str(e)}
    
    except Exception as e:
        # Capturar cualquier otro error
        resultado = {'error': 'Código no encontrado en la imagen'}
    
    finally:
        # Eliminar el archivo temporal
        os.remove(temp_filename)

        return render_template('resultado.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
