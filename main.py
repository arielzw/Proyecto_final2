from PolygonAPI import *
from show_data import *

import numpy as np

api = Polygon_API("https://api.polygon.io/v2", "c7Eb8zf4Eptgc6WyITtNPrbJITWpxp_i")


Cont = True

while(Cont):
    print("1. Actualización de datos")
    print("2. Visualización de datos")
    print("3. Para salir")

    Option = input("\n¿Opción? ")

    if(Option == "1"):
        api.get()



    if(Option == "2"):
        show_data()
    if (Option == "3"):
        print("Programa terminado")
        Cont = False



#
# termino = input("Término de búsqueda: ")
# lugar = input("Zona: ")
#
# url = "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/week/2021-07-22/2021-07-29?adjusted=true&sort=asc&limit=120"
# api_key = "c7Eb8zf4Eptgc6WyITtNPrbJITWpxp_i"
#
# header = {
#     "Authorization": "Bearer " + api_key
# }
#
# params = {
#     "term": termino,
#     "location": lugar
# }
#
# response = requests.get(url, headers=header)
# #print(response.text)
# negocios = response.json()["businesses"] #Se transforma el objeto response en un json y se devuelve la lista de la clave
#                                         # 'businesses'
#
# lista = [negocio['name'][:28].ljust(30) + 'Puntuación: ' + str(negocio['rating']).ljust(5) + 'Tel: ' + negocio['phone'] for negocio in negocios]
#
# print('\n')
# print('\n'.join(lista))
#
# input()

