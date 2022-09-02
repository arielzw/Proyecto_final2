from datetime import datetime, timedelta
import requests
#import pandas as pd
import sqlite3
from pathlib import Path

# url = "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2022-07-01/2022-08-01?adjusted=true&sort=asc&limit=5000"
# api_key = "c7Eb8zf4Eptgc6WyITtNPrbJITWpxp_i"

class Polygon_API:
    def __init__(self, url, key):
        self.__url = url
        self.__api_key = key


    def get(self):

        self.__ticker = "MELI"
        self.__first_date = "2022-08-22"
        self.__end_date = "2022-08-26"


        # self.__ticker = self.get_ticker()
        # self.__first_date = self.get_date("Ingrese la fecha inicial (YYYY-MM-DD): ")
        # self.__end_date = self.get_date("Ingrese la fecha final (YYYY-MM-DD): ")

        header = {
            "Authorization": "Bearer " + self.__api_key
        }

        print("Obteniendo datos...")

        self.__request_url = self.__url + "/aggs/ticker/" + self.__ticker + "/range/1/day/" + self.__first_date + "/" + \
                             self.__end_date + "?adjusted=true&sort=asc&limit=15000"

        response = requests.get(self.__request_url, headers=header)
        # Se transforma el diccionario en una dataframe de panda oriendado en columnas (opción index)
        lista_datos = response.json()['results']

        # Se agrega una columna "Fecha" con la mecha en YYYY-MM-DD convertida desde el timestamp de la columna t
        # pd_datos['Fecha'] = [datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d') for x in pd_datos['t']]

        columns = ', '.join(lista_datos[0].keys())
        print(columns)
        # columns = ', '.join(pd_datos.keys())

        #TODO: Se debe modificar porque cuando se ingresan los datos se debe crear una nueva tabla por lo que se
        #debe verificar si existe en otro lugar
        path = Path('Base.db')
        if path.exists():
            con = sqlite3.connect('Base.db')
            cur = con.cursor()
        else:
            con = sqlite3.connect('Base.db')
            cur = con.cursor()
            cur.execute("CREATE TABLE MELI(" + columns + ")")

        query = 'INSERT INTO MELI VALUES(?, ?, ?, ?, ?, ?, ?, ?)'

        for dic in lista_datos:
            cur.execute(query, tuple(dic.values()))
        con.commit()

        input()

    def get_ticker(self):
        ticker = input("Ingrese el ticker: ").upper()
        return ticker


    def get_date(self, text):
        while(True):
            date = input(text)
            date_now = datetime.today()

            #Se verifica que la fecha ingresada tenga el formato correcto
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                print("Formato de fecha incorrecto, debe ingresarse como YYYY-MM-DD")
            else:
                if(date.date() > date_now.date()):
                    print("La fecha ingresada no puede ser mayor a la fecha actual")
                if(date < (date_now - timedelta(days=2*365))):
                    print("No se pueden solicitar registros con más de 2 años de antiguedad") #Limitación cuenta Polygon
                else:
                    return str(date.date())
