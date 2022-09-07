from Polygon_API import *
from Data_Base import *
from Show_Data import *


api = Polygon_API("https://api.polygon.io/v2", "c7Eb8zf4Eptgc6WyITtNPrbJITWpxp_i")
db = DataBase('Base.db')


Repetir = True

while(Repetir):
    print("1. Actualización de datos")
    print("2. Visualización de datos")
    print("3. Para salir")

    Option = input("\n¿Opción? ")

    if(Option == "1"):
        db.save(api.get())
    if(Option == "2"):
        db.read('MELI', '2022-01-03', '2022-02-01')
        #show_data()
    if (Option == "3"):
        print("Programa terminado")
        Repetir = False

