from datetime import datetime
import sqlite3
import pandas as pd



class Database:
    def __init__(self, file):
        self.con = sqlite3.connect(file)
        self.cur = self.con.cursor()


    def save(self, datos_json):
        self.__lista = datos_json['results']
        self.__ticker = datos_json['ticker']

        query = 'CREATE TABLE IF NOT EXISTS ' + self.__ticker + ' (v, vw, o, c, h, l, t INTEGER PRIMARY KEY NOT NULL ON CONFLICT IGNORE, n)'
        self.cur.execute(query)

        query = 'INSERT OR IGNORE INTO ' + self.__ticker + ' VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
        for item in self.__lista:
            self.cur.execute(query, tuple(item.values()))

        # query = 'SELECT * FROM ' + self.__ticker + 'ORDER BY t ASCENDING'
        # self.cur.execute(query)
        # table = tables = self.cur.fetchall()
        # print(table)

        query = 'CREATE TABLE IF NOT EXISTS ' + self.__ticker + '_RANGES' + ' (fecha_inicio, fecha_fin)'
        self.cur.execute(query)

        # query = 'INSERT OR IGNORE INTO ' + self.__ticker + '_RANGES' + ' VALUES(, ?)'
        # self.cur.execute(query)

        self.con.commit()


    def summary(self):
        ####
        self.__ticker = 'MELI'
        query = 'SELECT * FROM ' + 'MELI' + ' ORDER BY t ASC'
        print(query)
        self.cur.execute(query)
        table = tables = self.cur.fetchall()
        print(table)

        ####



        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall() #tables es una lista de tuplas de un elemento

        print(f'{"Ticker":10}{"Fecha inicial":16}{"Fecha final":16}{"Registros":16}')
        for table_name in tables:
            #se debe colocar table_name[0] para que devuelva el valor y no una tupla de un elemento
            table = pd.read_sql_query("SELECT * from %s ORDER BY t ASC" % table_name[0], self.con, parse_dates={'t': {'unit': 'ms', 'errors': 'ignore'}})
            print(f'{str(table_name[0]):9} {str(table.t[0].strftime("%Y-%m-%d")):16}{str(list(table.t)[-1].strftime("%Y-%m-%d")):16}{int(table.size/8):5}')


    def read(self, ticker):
        #todo contemplar la inexistencia el ticker
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



