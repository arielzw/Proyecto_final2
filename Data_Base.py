from datetime import datetime, timezone
import sqlite3
import pandas as pd

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

    def summary(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall() #tables es una lista de tuplas de un elemento

        for table_name in tables:
            #se debe colocar table_name[0] para que devuelva el valor y no una tupla de un elemento
            table = pd.read_sql_query("SELECT * from %s ORDER BY t ASC" % table_name[0], self.con, parse_dates={'t': {'unit': 'ms', 'errors': 'ignore'}})
            print(str(table_name[0]) + ' - ' + str(table.t[0]) + ' <--> ' + str(list(table.t)[-1]))

    def read(self, ticker):
        self.__ticker = ticker
        consulta = 'SELECT * FROM ' + self.__ticker + ' ORDER BY t ASC'
        dt_frame = pd.read_sql(con=self.con, sql=consulta, parse_dates={'t': {'unit': 'ms', 'errors': 'ignore'}})
        return dt_frame

    def read2(self, ticker, from_date, to_date):
        ts_from = int(1000 * (datetime.timestamp(datetime.strptime(from_date, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc))))
        ts_to = int(1000 * (datetime.timestamp(datetime.strptime(to_date, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc))))
        self.__ticker = ticker

        consulta = 'SELECT * FROM ' + self.__ticker + ' WHERE t BETWEEN ' + str(ts_from) + ' AND ' + str(
            ts_to) + ' ORDER BY t ASC'
        dt_frame = pd.read_sql(con=self.con, sql=consulta, parse_dates={'t': {'unit': 'ms', 'errors': 'ignore'}})

        return dt_frame

    def crear_tabla(self):
        columns = ', '.join(self.__lista[0].keys())
        self.cur.execute('CREATE TABLE IF NOT EXISTS ' + self.__ticker + ' (' + columns + ')')
        #self.cur.execute('CREATE TABLE IF NOT EXISTS ' + self.__ticker + ' (t integer primary key not null on conflict ignore, ' + columns + ')')

        # try:
        #     self.cur.execute('SELECT * FROM ' + self.__ticker)
        # except:
        #     self.cur.execute('CREATE TABLE ' + self.__ticker + ' (' + columns + ')')