from datetime import datetime, timedelta
import requests
from colorama import Fore


class PolygonAPI:
    def __init__(self, url, key):
        self.__request_url = None
        self.end_date = None
        self.start_date = None
        self.ticker = None
        self.__url = url
        self.__api_key = key

    def get(self):
        self.ticker = self.get_ticker()
    # todo ver de implementar la barra de progreso llamando este proceso en segundo plano y haciendo una animación
        while True:
            self.start_date = self.get_date("Ingrese la fecha de inicio (YYYY-MM-DD):\n")
            self.end_date = self.get_date("Ingrese la fecha de fin (YYYY-MM-DD):\n")
            if self.start_date <= self.end_date:
                break
            else:
                print(f'{Fore.YELLOW}ERROR: La fecha de inicio no puede ser mayor a la fecha de fin{Fore.RESET}')

        header = {
            "Authorization": "Bearer " + self.__api_key
        }

        print("Obteniendo datos...")

        self.__request_url = self.__url + "/aggs/ticker/" + self.ticker + "/range/1/day/" + self.start_date + "/" + \
                             self.end_date + "?adjusted=true&sort=asc&limit=15000"
        try:
            response = requests.get(self.__request_url, headers=header)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            print(f'{Fore.YELLOW}Error de Timeout{Fore.RESET}')
            return 0
        except requests.exceptions.TooManyRedirects as err:
            print(f"{Fore.YELLOW}ERROR:{Fore.RESET}", err)
            return 0
        except requests.exceptions.HTTPError as err:
            print(f"{Fore.YELLOW}ERROR:{Fore.RESET}", err)
            return 0
        except requests.exceptions.RequestException as err:
            print(f"{Fore.YELLOW}ERROR: El servidor no responde. Verifique la conexión{Fore.RESET}")
            return 0
        except:
            print(f'{Fore.YELLOW}Error desconocido{Fore.RESET}')
            return 0
        else:
            if response.json()['resultsCount'] == 0:
                print(f'{Fore.YELLOW}No se obtuvieron resultados, verifique ticker y rango de fechas{Fore.RESET}')
                return 0
            else:

                return response.json()

    def get_ticker(self):
        ticker = input("Ingrese el ticker a pedir: \n").upper()
        return ticker

    def get_date(self, text):
        while True:
            date = input(text)
            date_now = datetime.today()

            # Se verifica que la fecha ingresada tenga el formato correcto
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                print("Formato de fecha incorrecto, debe ingresarse como YYYY-MM-DD")
            else:
                if date.date() > date_now.date():
                    print("La fecha ingresada no puede ser mayor a la fecha actual")
                if date < (date_now - timedelta(days=2*365)):
                    # Limitación cuenta Polygon
                    print("La subscripción gratuita no entrega registros de más de 2 años de antigüedad")
                else:
                    return str(date.date())
