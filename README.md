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

## Clase PolygonAPI
Esta clase permite acceder a los datos de stocks de la API Polygon.io. 
Se utiliza esta API por ser la propuesta por la consigna y porque cumple con los requisitos del software aunque conociendo las limitaciones que genera la utilización de una Key gratuita:
* Solo se pueden acceder a datos de hasta dos años de antigüedad: Se considera suficiente para el testeo de la aplicación
* No se pueden obtener los datos en tiempo real, sino que solo los datos de cierre: Esta limitación no permite implementar gráficos en tiempo real, pero no es una característica que se desee implementar.
* Se pueden realizar hasta 5 llamadas a la API por minuto: Se considera suficiente para el testeo de la aplicación

La API devuelve varios datos en forma de diccionario para cada período de agregación, pero para el caso de esta aplicación los únicos que se consideran son los siguientes:

**o:** Valor de apertura en dólares del ticker.

**c:** Valor de cierre en dólares del ticker.

**h:** Valor en dólares más alto alcanzado por el ticker.

**l:** Valor en dólares más bajo alcanzado por el ticker.

**t:** Time stamp en formato UNIX en milisegundos, correspondientes al inicio del período de agregación. Este valor corresponde a la fecha y hora GMT a las 0 hs de NYC, por lo tanto, en verano de NYC devuelve la hora GMT 4 AM, pero en invierno devuelve la hora GMT 5 AM. Para esta aplicación se trabaja solo con las fechas por lo que no se le da relevancia al huso horario.

**results_count:** Cantidad de registros devueltos en la consulta.

### Librerías utilizadas
* Librería ***datetime***: De esta librería se importan los métodos datetime y timedelta. Estos se utilizan para realizar las comprobaciones de las fechas ingresadas y realizar operaciones aritméticas entre ellas.
* Librería ***request***: Se utiliza para hacer los llamados a la API.

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
api = PolygonAPI("https://api.polygon.io/v2", "c7Eb8zf4Eptgc6WyITtNPrbJITWpxp_i")
```
Ambos argumentos se guardan en variables de instancia privadas (ya que no deben ser modificadas por fuera de la clase):

```python
class PolygonAPI:
    def __init__(self, url, key):
        self.__url = url
        self.__api_key = key
```

#### Método get

Obtiene los registros de la API solicitando el ticker y la fecha de inicio y de fin al usuario mediante métodos auxiliares que verifican el correcto ingreso de los datos. Los ingresos del usuario se guardan en variables de instancia privadas para ser usadas por otros métodos, luego, los datos obtenidos de la API se devuelven en formato *json*, salvo que se produzca un error, en ese caso devuelve cero.

*Chequeo de errores:*

* La fecha inicial es más reciente que la fecha final. En ese caso se vuelve a solicitar un nuevo ingreso para ambas fechas.
* Excepción de timeout. Si la API se demora en entregar los resultados más de lo esperado, se informa al usuario del error y se retorna cero.
* Excepción de request. Si el servidor no responde (este error se produce por ejemplo cuando no hay conexión de internet), se informa al usuario del error y se retorna cero.  
* Excepción de TooManyRedirects y HTTPError (respuesta diferente de 200). En ambos casos se pasa la descripción del error que devuelve la excepción al usuario y se retorna cero.
* En caso de otro error se informa al usuario que se produjo un error desconocido y se retorna cero.

#### Método get_ticker

Solicita al usuario que ingrese el ticker a consultar y retorna el valor ingresado, pasado previamente a upper case.

#### Método get_date

Es un método genérico que sirve para solicitar una fecha en el formato admitido por la API. Recibe como argumento un texto a mostrar al usuario para indicarle el dato que debe ingresar. En caso de error vuelve a solicitar el ingreso.

*Chequeo de errores:*
* Formato de fecha incorrecto (no respesta YYYY-MM-DD)
* Rango de fecha incorrecto. Si se solicitan registros de más de dos años debido a la limitación de la cuenta gratuita de la API.
* Fecha ingresada mayor a la fecha actual

## Clase Database
Esta clase implementa métodos para grabar en una base de datos localmente, la lectura de la misma y la muestra de un sumario de los datos guardados por consola.

### Librerías utilizadas
Librería *datetime*: De esta librería se importa el método datetime. Este se utiliza para formatear las fechas en formato string (YYYY-MM-DD) y para convertir dicho string en timestamp

Librería _sqlite3_: Se utiliza para crear y acceder a la base de datos. Se opta por sqlite debido a que permite acceder a la base de datos como si fuera un simple archivo local, sin tener que acceder y configurar un servidor como sí pasa con SQL.

Librería _pandas_: Se utiliza para convertir los datos de la base de datos en un data frame compuesto por filas y columnas, el cual es más fácil de manejar posteriormente.

### Acceso a la API

### Métodos de la clase

Al instanciar la clase se llama a la función constructora, enviando como argumento el nombre del archivo de la base de datos, el cual se guarda en la raíz del proyecto:
```python
    db = Database('Base.db')
```

. En el momento de instanciar, se establece la conexión y se define la variable cur para acceder a la misma:

```python
    def __init__(self, file):
        self.con = sqlite3.connect(file)
        self.cur = self.con.cursor()
```

#### Método save

Este método recibe como argumento los datos a guardar en formato _json_, luego guarda el nombre del ticker y los datos en una lista.
La tabla se crea mediante:
```python
self.cur.execute(
            'CREATE TABLE IF NOT EXISTS ' + self.__ticker + ' (v, vw, o, c, h, l, t INTEGER PRIMARY KEY NOT NULL ON CONFLICT IGNORE, n)')
```
En donde se define la key _t_ como ID de la tabla, ya que es un parámetro que no se repite, y al definirlo como "ON CONFLICT IGNORE" en el caso que se intente grabar datos existentes en la tabla no se sobrescribe y se ignora el error, para lo cual se usa el comando "INSERT OR IGNORE" para agregar los datos a la tabla:
```python
 query = 'INSERT OR IGNORE INTO ' + self.__ticker + ' VALUES(?, ?, ?, ?, ?, ?, ?, ?)'

        for item in self.__lista:
            self.cur.execute(query, tuple(item.values()))

        self.con.commit()
```

#### Método summary
Se utiliza para mostrar un sumario de la base de datos, de la siguiente manera:
```python
Ticker    Fecha inicial   Fecha final     Registros       
MELI      2021-01-04      2022-02-10         60
AAL       2021-01-04      2022-09-01        292
AAPL      2021-01-04      2021-02-05         24
```

#### Método read
Se utiliza para obtener de la base de datos la información de un ticker determinado, el cual se pasa como argumento. Los datos se devuelven en un data frame de pandas.


## Clase Show_Data
Esta clase se encarga de mostrar los datos en forma gráfica.

### Librerías utilizadas
* matplotlib 

### Métodos de la clase




