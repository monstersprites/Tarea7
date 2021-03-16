import sqlite3
import json
import urllib.request
cedula= '10800064148'
conexion=sqlite3.connect('app.db')
registro=conexion.cursor()
data = registro.execute("SELECT * FROM VACUNADO WHERE CEDULA = '"+cedula+"'")
datos = data.fetchall()
for i in datos:
    print(i[5])