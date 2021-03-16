-- SQLite
CREATE TABLE VACUNADO(
ID_VACUNADO INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
CEDULA TEXT,
NOMBRE TEXT, 
APELLIDO TEXT,
FECHA_N TEXT,
VACUNA TEXT,
PROVINCIA TEXT,
FECHA_P TEXT,
FECHA_S TEXT DEFAULT NULL,
SIGNO TEXT,
DOSIS INTEGER DEFAULT 1
)

DROP TABLE VACUNADO
SELECT * FROM VACUNADO WHERE NOMBRE='BELLA LUZ'
SELECT * FROM VACUNA

SELECT V.MARCA, COUNT(*)
    FROM VACUNADO VO
    LEFT JOIN VACUNA V
    ON VO.VACUNA = V.MARCA
    GROUP BY VO.VACUNA

SELECT V.MARCA, COUNT(VO.VACUNA) AS CANTIDAD
        FROM VACUNA V
        LEFT JOIN VACUNADO VO
        ON V.MARCA = VO.VACUNA
        GROUP BY V.MARCA

CREATE TABLE SIGNO(
ID_SIGNO INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
NOMBRE_S TEXT
)
"Capricornio", "Acuario", "Piscis", "Aries", "Tauro", "Géminis", "Cáncer", "Leo", "Virgo", "Libra", "Escorpio", "Sagitario"
INSERT INTO SIGNO (NOMBRE_S) VALUES ('Capricornio')
INSERT INTO SIGNO (NOMBRE_S) VALUES ('Acuario')
INSERT INTO SIGNO (NOMBRE_S) VALUES ('Piscis')
INSERT INTO SIGNO (NOMBRE_S) VALUES ('Aries')
INSERT INTO SIGNO (NOMBRE_S) VALUES ('Tauro')
INSERT INTO SIGNO (NOMBRE_S) VALUES ('Géminis')
INSERT INTO SIGNO (NOMBRE_S) VALUES ('Cáncer')
INSERT INTO SIGNO (NOMBRE_S) VALUES ('Leo')
INSERT INTO SIGNO (NOMBRE_S) VALUES ('Virgo')
INSERT INTO SIGNO (NOMBRE_S) VALUES ('Libra')
INSERT INTO SIGNO (NOMBRE_S) VALUES ('Escorpio')
INSERT INTO SIGNO (NOMBRE_S) VALUES ('Sagitario')


SELECT S.NOMBRE_S, COUNT(V.SIGNO) AS CANTIDAD
    FROM SIGNO S
    LEFT JOIN VACUNADO V
    ON S.NOMBRE_S = V.SIGNO
    GROUP BY S.NOMBRE_S

    SELECT * FROM SIGNO
    SELECT * FROM VACUNADO
INSERT INTO VACUNADO(CEDULA,NOMBRE,APELLIDO,FECHA_N,VACUNA,PROVINCIA,FECHA_P,SIGNO) VALUES ('5646456','DANNY','OZUNA','2002-12-03','S','LOS RIOS','2020-03-12','Acuario')
SELECT * FROM VACUNA WHERE CANTIDAD > 0

CREATE TABLE PROVINCIAS(
    ProvinciaID INTEGER
    , Nombre TEXT DEFAULT NULL
)

INSERT INTO PROVINCIAS VALUES
    (1,'Azua')
    ,(2,'Bahoruco')
    ,(3,'Barahona')
    ,(4,'Dajabón')
    ,(5,'Distrito Nacional')
    ,(6,'Duarte')
    ,(7,'Elías Piña')
    ,(8,'El Seibo')
    ,(9,'Espaillat')
    ,(10,'Hato Mayor')
    ,(11,'Hermanas Mirabal')
    ,(12,'Independencia')
    ,(13,'La Altagracia')
    ,(14,'La Romana')
    ,(15,'La Vega')
    ,(16,'María Trinidad Sánchez')
    ,(17,'Monseñor Nouel')
    ,(18,'Monte Cristi')
    ,(19,'Monte Plata')
    ,(20,'Pedernales')
    ,(21,'Peravia')
    ,(22,'Puerto Plata')
    ,(23,'Samaná')
    ,(24,'Sánchez Ramírez')
    ,(25,'San Cristóbal')
    ,(26,'San José de Ocoa')
    ,(27,'San Juan')
    ,(28,'San Pedro de Macorís')
    ,(29,'Santiago')
    ,(30,'Santiago Rodríguez')
    ,(31,'Santo Domingo')
    ,(32,'Valverde')
DROP TABLE Provincias