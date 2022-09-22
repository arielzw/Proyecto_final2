from datetime import datetime, timedelta
import requests

class Polygon_API:
    def __init__(self, url, key):
        self.__url = url
        self.__api_key = key


    def get(self):
        self.__ticker = self.get_ticker()

        while True:
            self.__start_date = self.get_date("Ingrese la fecha de inicio (YYYY-MM-DD):\n")
            self.__end_date = self.get_date("Ingrese la fecha de fin (YYYY-MM-DD):\n")
            if self.__start_date <= self.__end_date:
                break
            else:
                print('ERROR: La fecha de inicio no puede ser mayor a la fecha de fin')

        header = {
            "Authorization": "Bearer " + self.__api_key
        }

        print("Obteniendo datos...")

        self.__request_url = self.__url + "/aggs/ticker/" + self.__ticker + "/range/1/day/" + self.__start_date + "/" + \
                             self.__end_date + "?adjusted=true&sort=asc&limit=15000"
        try:
            response = requests.get(self.__request_url, headers=header)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            print('Error de Timeout')
            return 0
        except requests.exceptions.RequestException as err:
            print("ERROR: El servidor no responde. Verifique la conexión")
            return 0
        except requests.exceptions.TooManyRedirects as err:
            print("ERROR:", err)
            return 0
        except requests.exceptions.HTTPError as err:
            print("ERROR:", err)
            return 0
        except:
            print('Error desconocido')
            return 0
        else:
            if(response.json()['resultsCount'] == 0):
                print('No se obtuvieron resultados, verifique ticker y rango de fechas')
                return 0
            else:
                return response.json()


    def get_ticker(self):
        ticker = input("Ingrese el ticker a pedir: \n").upper()
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
                if date.date() > date_now.date():
                    print("La fecha ingresada no puede ser mayor a la fecha actual")
                if date < (date_now - timedelta(days=2*365)):
                    print("La subscripción gratuita no entrega registros de más de 2 años de antiguedad") #Limitación cuenta Polygon
                else:
                    return str(date.date())
