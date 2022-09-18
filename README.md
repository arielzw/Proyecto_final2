
# TP final de certificación profesional en Python
<!-- TOC -->

<!-- TOC -->


## Propósito
Se implementa un programa que permite leer datos de una API de finanzas, guardarlos en una base de datos y graficarlos.

## Objetivo de diseño
Se desarrolla el diseño con el objetivo de lograr un software completamente modular con código reutilizable.

### Definición de clases
El software consta de 3 módulos fundamentales:
* Obtención de datos de la API
* Gestión de base de datos
* Muestra de información en pantalla

Para cada uno de los módulos se implementa una clase encargada de gestionar todas las funciones relacionadas. La gestión de la interfaz de usuario es delegada al programa principal, ya que dicha función es específica para cada aplicación por lo que no se busca la modularización en ese aspecto.

### Clase Polygon_API
Esta clase permite acceder a los datos de stocks de la API Polygon.io. 
Se utiliza esta API por ser la propuesta por la consigna y porque cumple con los requisitos del software aunque conociendo las limitaciones que genera la utilización de una Key gratuita:
* Solo se pueden acceder a datos de hasta dos años de antigüedad: Se considera suficiente para el testeo de la aplicación
* No se pueden obtener los datos en tiempo real, sino que solo los datos de cierre: Esta limitación no permite implementar gráficos en tiempo real, pero no es una característica que se desee implementar.
* Se pueden realizar hasta 5 llamadas a la API por minuto: Se considera suficiente para el testeo de la aplicación

#### Acceso a la API
En primera instancia se crea una cuenta ingresando a la página https://polygon.io/ y seleccionando "Get free API key". Una vez creada la cuenta y obtendida la clave, se accede a la documentación de stocks de la API en https://polygon.io/docs/stocks/getting-started

Para acceder a la API se debe hacer un request a la dirección https://api.polygon.io/v2/aggs/ticker y pasando los parámetros directamente en dicha dirección como en el siguiente ejemplo:

https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2020-06-01/2020-06-17?apiKey=c7Eb8zf4Eptgc6WyITtNPrbJITWpxp_i

Opcionalmente se puede enviar la apikey a través de un Authorization header, y es como se implementa en este software, en donde se carga la url con todos los parámetros solicitados por el usuario y se envía la key en el header:
```python
requests.get(request_url, headers=header)
```






#### Librerías utilizadas


#### Detalle de la implementación










