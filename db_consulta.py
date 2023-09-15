import mysql.connector

class MyWindow():
    def __init__(self):
        super().__init__()

    def queryDatabase(self):
        try:
            # Conectar a la base de datos MariaDB
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='cot_app'
            )

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cliente')  # Reemplaza "tabla" con el nombre de tu tabla
            datos = cursor.fetchall()  # Obtén los datos de la consulta

            conn.close()
            print(datos)
            return datos  # Retorna los datos

        except mysql.connector.Error as e:
            print("Error de MariaDB:", e)
