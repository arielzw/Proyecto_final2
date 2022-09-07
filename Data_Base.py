from datetime import datetime, timedelta
import time
import sqlite3

# Se agrega una columna "Fecha" con la mecha en YYYY-MM-DD convertida desde el timestamp de la columna t
# pd_datos['Fecha'] = [datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d') for x in pd_datos['t']]

class DataBase:
    def __init__(self, file):
        self.con = sqlite3.connect(file)
        self.cur = self.con.cursor()


    def save(self, datos_json):
        self.__lista = datos_json['results']
        self.__ticker = datos_json['ticker']
        self.crear_tabla()

        query = 'INSERT INTO ' + self.__ticker + ' VALUES(?, ?, ?, ?, ?, ?, ?, ?)'

        for item in self.__lista:
            self.cur.execute(query, tuple(item.values()))

        self.con.commit()

    def read(self, ticker, from_date, to_date):
        #Se suma 7200 para corregir la zona horaria, ya que BUE es -5 y NYC es -3. El timestamp devuelto por la api de
        #polygon está en ms referido a UTC -5
        ts_from = int(1000 * (7200 + datetime.timestamp(datetime.strptime(from_date, '%Y-%m-%d'))))
        ts_to = int(1000 * (7200 + datetime.timestamp(datetime.strptime(to_date, '%Y-%m-%d'))))
        self.__ticker = ticker

        #todo Implementar la lectura de la base de datos y devolverla en una lista de diccionarios
        #para después pasarla como argumento a show data
        query = 'INSERT INTO ' + self.__ticker + ' VALUES(?, ?, ?, ?, ?, ?, ?, ?)'

        for item in self.__lista:
            self.cur.execute(query, tuple(item.values()))

    def crear_tabla(self):
        columns = ', '.join(self.__lista[0].keys())

        try:
            self.cur.execute('SELECT * FROM ' + self.__ticker)
        except:
            self.cur.execute('CREATE TABLE ' + self.__ticker + ' (' + columns + ')')