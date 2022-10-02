import PolygonAPI
import Database
import ShowData
from colorama import Fore, init


# Llamado al método init de la librería colorama para que los colores funcionen en Windows
init(convert=True)

# Declaración de objetos
api = PolygonAPI.PolygonAPI("https://api.polygon.io/v2", "c7Eb8zf4Eptgc6WyITtNPrbJITWpxp_i")
db = Database.Database('Base.db')
show = ShowData.ShowData()

while True:
    print("\nIngrese una opción:")
    print(f"1. Actualización de datos")
    print("2. Visualización de datos")
    print("3. Para salir")
    option_1 = input("¿Opción? ")

    if option_1 == '1':
        res = api.get()     # Se recibe un json con los resultados de la consulta
        if res != 0:        # Si no hubo errores se guarda en la base de datos
            db.save(res, api.start_date, api.end_date)
            print('Datos guardados correctamente')
        else:
            print(f"{Fore.YELLOW}No se actualizó la base de datos{Fore.RESET}")

    elif option_1 == '2':
        while True:
            print("\nIngrese una opción:")
            print("1. Ver resumen")
            print("2. Ver gráfico")
            print("3. Volver")
            option_2 = input("¿Opción? ")

            if option_2 == '1':
                db.summary()
            elif option_2 == '2':
                while True:     # Se realiza un ciclo hasta que los datos ingresados sean correctos
                    ticker = api.get_ticker()
                    data = db.read(ticker)
                    if not data.empty:  # Si la función no devolvió error, salir
                        break
                rangos = db.get_ranges(ticker)  # Se obtienen los rangos de datos guardados para el ticker seleccionado
                show.graph(data, ticker, rangos)    # Se grafica el rango seleccionado
            elif option_2 == '3':
                break
            else:
                print("Ingreso incorrecto !!!")

    elif option_1 == '3':
        print("Programa terminado")
        break
    else:
        print("Ingreso incorrecto !!!")
