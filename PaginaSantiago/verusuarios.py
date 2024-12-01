import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('usuarios.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Consultar todos los usuarios
cursor.execute("SELECT * FROM usuario")
usuarios = cursor.fetchall()

# Mostrar los usuarios
for usuario in usuarios:
    print(f"ID: {usuario[0]}, Username: {usuario[1]}, Email: {usuario[2]}")

# Cerrar la conexión
conn.close()
