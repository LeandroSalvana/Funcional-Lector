import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "Leandro",
    password = "Leandro",
    #port = "3306"
    database = 'dni_lector',
)

print(conn)


cursor = conn.cursor()
sql = """INSERT INTO dni_datos (n_de_tramite, apellido, nombre, sexo, n_de_dni, tipo, n_de_nacimiento, fecha_de_nacimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
valores = ()

#sql = """SELECT * FROM dni_datos"""

cursor.execute(sql)

#datos = cursor.fetchall()

conn.commit()

#cursor.execute("SHOW TABLES")
#cursor.execute("CREATE DATABASE dni_lector")
#cursor.execute("SHOW DATABASES")
#for dato in datos:
    #print(dato)

conn.close()