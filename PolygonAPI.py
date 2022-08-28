from datetime import datetime, timedelta
import requests


# url = "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2022-07-01/2022-08-01?adjusted=true&sort=asc&limit=5000"
# api_key = "c7Eb8zf4Eptgc6WyITtNPrbJITWpxp_i"

class Polygon_API:
    def __init__(self, url, key):
        self.__url = url
        self.__api_key = key


    def get(self):

        self.__ticker = self.get_ticker()
        self.__first_date = self.get_date("Ingrese la fecha inicial (YYYY-MM-DD): ")
        self.__end_date = self.get_date("Ingrese la fecha final (YYYY-MM-DD): ")

        header = {
            "Authorization": "Bearer " + self.__api_key
        }

        print("Obteniendo datos...")

        self.__request_url = self.__url + "/aggs/ticker/" + self.__ticker + "/range/1/day/" + self.__first_date + "/" + \
                             self.__end_date + "?adjusted=true&sort=asc&limit=15000"

        response = requests.get(self.__request_url, headers=header)
        print(response.json())


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
