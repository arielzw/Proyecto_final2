# Se agrega una columna "Fecha" con la mecha en YYYY-MM-DD convertida desde el timestamp de la columna t
# pd_datos['Fecha'] = [datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d') for x in pd_datos['t']]

import sqlite3


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


    def crear_tabla(self):
        columns = ', '.join(self.__lista[0].keys())

        try:
            self.cur.execute('SELECT * FROM ' + self.__ticker)
        except:
            self.cur.execute('CREATE TABLE ' + self.__ticker + ' (' + columns + ')')