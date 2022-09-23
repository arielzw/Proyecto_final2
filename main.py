from Polygon_API import *
from Database import *
from Show_Data import *


api = Polygon_API("https://api.polygon.io/v2", "c7Eb8zf4Eptgc6WyITtNPrbJITWpxp_i")

show = Show_Data()

repetir_1 = True

while repetir_1:
    print("\nIngrese una opción:")
    print("1. Actualización de datos")
    print("2. Visualización de datos")
    print("3. Para salir")
    option_1 = input("¿Opción? ")

    if option_1 == '1':
        res = api.get()
        if res != 0:
            db.save(res)
        else:
            print("No se actualizó la base de datos")

    elif option_1 == '2':
        repetir_2 = True

        while repetir_2:
            print("\nIngrese una opción:")
            print("1. Ver resumen")
            print("2. Ver gráfico")
            print("3. Volver")
            option_2 = input("¿Opción? ")

            if option_2 == '1':
                db.summary()

            elif option_2 == '2':
                ticker = api.get_ticker()
                data = db.read(ticker)
                show.graph(data, ticker)

            elif (option_2 == '3'):
                repetir_2 = False

            else:
                print("Ingreso incorrecto !!!")

    elif option_1 == '3':
        print("Programa terminado")
        repetir_1 = False

    else:
        print("Ingreso incorrecto !!!")

