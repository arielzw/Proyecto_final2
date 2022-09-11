from Polygon_API import *
from Data_Base import *
from Show_Data import *


api = Polygon_API("https://api.polygon.io/v2", "c7Eb8zf4Eptgc6WyITtNPrbJITWpxp_i")
db = DataBase('Base.db')
show = Show_Data()

Repetir = True

while(Repetir):
    print("1. Actualización de datos")
    print("2. Visualización de datos")
    print("3. Para salir")

    Option = input("\n¿Opción? ")

    if(Option == "1"):
        db.save(api.get())
    if(Option == "2"):
        # ticker = api.get_ticker()
        # dt_from = api.get_date("Ingrese la fecha inicial (YYYY-MM-DD): ")
        # dt_to = api.get_date("Ingrese la fecha final (YYYY-MM-DD): ")
        ticker = 'MELI'
        dt_from = '2022-01-01'
        dt_to = '2022-02-01'
        data = db.read(ticker, dt_from, dt_to)
        show.show(data, ticker)
    if (Option == "3"):
        print("Programa terminado")
        Repetir = False

