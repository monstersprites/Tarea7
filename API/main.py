import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
import urllib.request
import datetime
from datetime import date

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api')
def read_root():
    return {'detail': 'Welcome to this app'}

@app.post('/api/Registrar_P/{cedula}/{vacuna}/{provincia}/{fecha_v}')
def Registrar_P(cedula: str, vacuna: str, provincia: str, fecha_v: str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    respuesta = urllib.request.urlopen('https://api.adamix.net/apec/cedula/'+cedula+'')
    data = json.loads(respuesta.read())
    try:
        fecha = str(datetime.datetime.strptime(data['FechaNacimiento'], '%Y-%m-%d %H:%M:%S.%f').date())
        signo = ("Capricornio", "Acuario", "Piscis", "Aries", "Tauro", "Géminis", "Cáncer", "Leo", "Virgo", "Libra", "Escorpio", "Sagitario")
        fechas = (20, 19, 20, 20, 21, 21, 22, 22, 22, 22, 22, 21)
        dia= int(fecha[8:10])
        mes= int(fecha[5:7])
        mes=mes-1
        if dia>fechas[mes]:
            mes=mes+1
        if mes==12:
            mes=0
    except:
        return{"mensaje":"Cedula Invalida"}
    query = registro.execute ("SELECT * FROM VACUNADO Where CEDULA = '"+cedula+"'")
    datos = query.fetchall()
    for dato in datos:
        if dato[1] == cedula and dato[10]!=2:
            sql =("UPDATE VACUNADO SET FECHA_S = '"+fecha_v+"' WHERE CEDULA = '"+cedula+"'")
            registro.execute(sql)
            registro.execute("UPDATE VACUNA SET CANTIDAD = CANTIDAD-1 WHERE MARCA = '"+vacuna+"'")
            registro.execute("UPDATE VACUNADO SET DOSIS = 2 WHERE CEDULA = '"+cedula+"'")
            conexion.commit()
            return {"mensaje":"Segunda dosis agregada","nombre": dato[2],"apellido":dato[3], "fecha_p":dato[7],"signo":dato[9] }
        else:
            return{"mensaje":"Las Dos dosis han sido resivida"}
    if datos == []: 
        try:     
            if data['Cedula']==cedula:
                info= (data['Cedula'],data['Nombres'],data['Apellido1'],datetime.datetime.strptime(data['FechaNacimiento'], '%Y-%m-%d %H:%M:%S.%f').date(),vacuna,provincia,fecha_v,signo[mes])
                sql=''' INSERT INTO VACUNADO(CEDULA,NOMBRE,APELLIDO,FECHA_N,VACUNA,PROVINCIA,FECHA_P,SIGNO) VALUES (?,?,?,?,?,?,?,?) '''
                registro.execute(sql,info)
                registro.execute("UPDATE VACUNA SET CANTIDAD = CANTIDAD-1 WHERE MARCA = '"+vacuna+"'")
                conexion.commit()
                return {"mensaje": "Registro Exitoso"}
        except:
            return{"mensaje":"Cedula invalida"}

@app.post('/api/Registrar_v/{marca}/{cantidad}')
def Registrar_v(marca: str, cantidad: int):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    info = (marca.upper(),cantidad)
    query = ''' INSERT INTO VACUNA(MARCA,CANTIDAD) VALUES (?,?) '''
    registro.execute(query,info)
    conexion.commit()
    return {"mensaje":"Registro Completo"}

@app.get('/api/Consultar_V/{campo}/{buscar}')
def Consultar_V(campo: str, buscar: str):
    a=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT * FROM VACUNADO WHERE "+campo+" LIKE '%"+buscar.upper()+"%'")
    datos = registro.fetchall()
    for i in datos:
        a.append({"NOMBRE":i[2],"APELLIDO":i[3],"DOSIS":i[10]})
    return a
@app.get('/api/List_Prov/{provincia}')
def List_Prov(provincia: str):
    a=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("SELECT * FROM VACUNADO WHERE PROVINCIA = '"+provincia+"'")
    conexion.commit()
    datos= registro.fetchall()
    for i in datos:
        a.append({"CEDULA":i[1],"NOMBRE":i[2],"APELLIDO":i[3],"FECHA_P":i[7],"FECHA_S":i[8]})
    return a

@app.get('/api/List_Marca')
def List_Marca():
    a=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute(''' SELECT V.MARCA, COUNT(VO.VACUNA) AS CANTIDAD
        FROM VACUNA V
        LEFT JOIN VACUNADO VO
        ON V.MARCA = VO.VACUNA
        GROUP BY V.MARCA ''')
    conexion.commit()
    datos = registro.fetchall()
    for i in datos:
        a.append({"MARCA":i[0],"CANTIDAD":i[1]})
    return a

@app.get('/api/List_Signo')
def List_Signo():
    a=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute(''' SELECT S.NOMBRE_S, COUNT(V.SIGNO) AS CANTIDAD
    FROM SIGNO S
    LEFT JOIN VACUNADO V
    ON S.NOMBRE_S = V.SIGNO
    GROUP BY S.NOMBRE_S ''')
    conexion.commit()
    datos = registro.fetchall()
    for i in datos:
        a.append({"NOMBRE_S":i[0],"CANTIDAD":i[1]})
    return a
@app.delete('/api/Eliminar_V/{cedula}')
def Eliminar_V(cedula: str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    data = registro.execute("SELECT * FROM VACUNADO WHERE CEDULA = '"+cedula+"'")
    datos = data.fetchall()
    for i in datos:
        registro.execute("UPDATE VACUNA SET CANTIDAD = CANTIDAD + 1 WHERE MARCA = '"+i[5]+"' ")
    registro.execute("DELETE FROM VACUNADO WHERE CEDULA = '"+cedula+"'")
    conexion.commit()
    return {"mensaje":"Registro Eliminado"}

@app.get('/api/Vacunas')
def Vacunas():
    a=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    data = registro.execute("SELECT * FROM VACUNA WHERE CANTIDAD > 0")
    conexion.commit()
    datos = data.fetchall()
    for i in datos:
        a.append({"MARCA": i[1]})
    return a

@app.get('/api/Provinvias')
def Provinvias():
    a=[]
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    data = registro.execute("SELECT * FROM PROVINCIAS")
    conexion.commit()
    datos = data.fetchall()
    for i in datos:
        a.append({"NOMBRE": i[1]})
    return a

@app.post('/api/Modificar_Pro/{nombre}/{numero}')
def Modificar_Pro(nombre: str,numero: str):
    conexion=sqlite3.connect('app.db')
    registro=conexion.cursor()
    registro.execute("UPDATE PROVINCIAS SET Nombre = '"+nombre+"' WHERE ProvinciaID= '"+numero+"' ")
    conexion.commit()
    return {"mensaje":"Actulizacion Completada Exitosamente!"}




    




    











            



