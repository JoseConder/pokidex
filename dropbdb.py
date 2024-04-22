from dbcon import *
import os

coleccion = input("Cual colección deseas eliminar?")
dropCollection(coleccion)

carpeta = '/resources/pokemon'
for archivo in os.listdir(carpeta):
    ruta_completa = os.path.join(carpeta, archivo)
    if os.path.isfile(ruta_completa):
        os.remove(ruta_completa)
