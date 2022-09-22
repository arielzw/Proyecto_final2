# TP final de certificación profesional en Python

##  Propósito
Se implementa un programa que permite leer datos de una API de finanzas, guardarlos en una base de datos y graficarlos.

## Objetivo de diseño
* Se desarrolla el diseño con el objetivo de lograr un software completamente modular con código reutilizable.
* Se implementa chequeo de errores de ingreso de usuario (Ticker inválido, formato de fecha incorrecto, rango de fecha incorrecto) y de la API (Excepción de request, timeout, error http, etc.).
* Se avisa al usuario que no se obtuvieron resultados (en caso de que el rango de fechas sea feriado)
* Se previene la carga de datos duplicados en la DB
* Se muestra un sumario de los datos en la DB indicando Ticker, fecha del registro más antiguo, fecha del registro más reciente y cantidad de registros para ese Ticker.
* Se muestran los datos en forma gráfica, graficando el valor de Apertura, Cierre, Máximo y Mínimo.


## Definición de clases
El software consta de 3 módulos fundamentales:
* Obtención de datos de la API
* Gestión de base de datos
* Muestra de información en pantalla

Para cada uno de los módulos se implementa una clase encargada de gestionar todas las funciones relacionadas. La gestión de la interfaz de usuario es delegada al programa principal, ya que dicha función es específica para cada aplicación por lo que no se busca la modularización de la misma.

## Clase Polygon_API
Esta clase permite acceder a los datos de stocks de la API Polygon.io. 
Se utiliza esta API por ser la propuesta por la consigna y porque cumple con los requisitos del software aunque conociendo las limitaciones que genera la utilización de una Key gratuita:
* Solo se pueden acceder a datos de hasta dos años de antigüedad: Se considera suficiente para el testeo de la aplicación
* No se pueden obtener los datos en tiempo real, sino que solo los datos de cierre: Esta limitación no permite implementar gráficos en tiempo real, pero no es una característica que se desee implementar.
* Se pueden realizar hasta 5 llamadas a la API por minuto: Se considera suficiente para el testeo de la aplicación

### Acceso a la API
En primera instancia se crea una cuenta ingresando a la página https://polygon.io/ y seleccionando "Get free API key". Una vez creada la cuenta y obtendida la clave, se accede a la documentación de stocks de la API en https://polygon.io/docs/stocks/getting-started

Para acceder a la API se debe hacer un request a la dirección https://api.polygon.io/v2 y pasando los parámetros directamente en dicha dirección como en el siguiente ejemplo:

https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2020-06-01/2020-06-17?apiKey=c7Eb8zf4Eptgc6WyITtNPrbJITWpxp_i

Opcionalmente, se puede enviar la apikey a través de un Authorization header, y es como se implementa en este software, en donde se carga la url con todos los parámetros solicitados por el usuario y se envía la key en el header:
```python
requests.get(request_url, headers=header)
```
Se opta por obtener un período de agregación de 1 día de forma de obtener la máxima resolución posible otorgada por la key gratuita.

### Métodos de la clase

Al instanciar la clase se llama a la función constructora, enviando como argumento dirección de la API y la key:
```phyton
api = Polygon_API("https://api.polygon.io/v2", "c7Eb8zf4Eptgc6WyITtNPrbJITWpxp_i")
```
Ambos argumentos se guardan en variables de instancia privadas (ya que no deben ser modificadas por fuera de la clase):

```python
class Polygon_API:
    def __init__(self, url, key):
        self.__url = url
        self.__api_key = key
```

#### Método get

Obtiene los registros de la API solicitando el ticker y la fecha de inicio y de fin al usuario mediante métodos auxiliares que verifican el correcto ingreso de los datos. Los ingresos del usuario se guardan en variables de instancia privadas para ser usadas por otros métodos, luego, los datos obtenidos de la API se devuelven en formato *json*, salvo que se produzca un error, en ese caso devuelve cero.

***Chequeo de errores:***

* La fecha inicial es más reciente que la fecha final. En ese caso se vuelve a solicitar un nuevo ingreso para ambas fechas.
* Excepción de timeout. Si la API se demora en entregar los resultados más de lo esperado, se informa al usuario del error y se retorna cero.
* Excepción de request. Si el servidor no responde (este error se produce por ejemplo cuando no hay conexión de internet), se informa al usuario del error y se retorna cero.  
* Excepción de TooManyRedirects y HTTPError (respuesta diferente de 200). En ambos casos se pasa la descripción del error que devuelve la excepción al usuario y se retorna cero.
* En caso de otro error se informa al usuario que se produjo un error desconocido y se retorna cero.

#### Método get_ticker

Solicita al usuario que ingrese el ticker a consultar y retorna el valor ingresado, pasado previamente a upper case.

#### Método get_date

Es un método genérico que sirve para solicitar una fecha en el formato admitido por la API. Recibe como argumento un texto a mostrar al usuario para indicarle el dato que debe ingresar. En caso de error vuelve a solicitar el ingreso.

***Chequeo de errores***:
* Formato de fecha incorrecto (no respesta YYYY-MM-DD)
* Rango de fecha incorrecto. Si se solicitan registros de más de dos años debido a la limitación de la cuenta gratuita de la API.
* Fecha ingresada mayor a la fecha actual

#### Librerías utilizadas
* Librería ***datetime***: De esta librería se importan los métodos datetime y timedelta. Estos se utilizan para realizar las comprobaciones de las fechas ingresadas y realizar operaciones aritméticas entre ellas.
* Librería ***request***: Se utiliza para hacer los llamados a la API.



#### Detalle de la implementación










