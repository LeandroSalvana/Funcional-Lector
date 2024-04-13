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
sql = """INSERT INTO dni_datos (Apellido, Nombre) VALUES (%s, %s)"""
valores = ('Salva', "Karina")

cursor.execute(sql, valores)

conn.commit()

#print(cursor.lastrowid)

#cursor.execute("SHOW TABLES")
#cursor.execute("CREATE DATABASE dni_lector")
#cursor.execute("SHOW DATABASES")
#for datos in cursor:
    #print(datos)

conn.close()