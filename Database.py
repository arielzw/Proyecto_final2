import sqlite3
import pandas as pd
from colorama import Fore


class Database:
    def __init__(self, file):
        self.__ticker = None
        self.__lista = None
        self.con = sqlite3.connect(file)
        self.cur = self.con.cursor()

    def save(self, datos_json, fecha_inicio, fecha_fin):
        self.__lista = datos_json['results']
        self.__ticker = datos_json['ticker']

        query = 'CREATE TABLE IF NOT EXISTS ' + self.__ticker + \
                ' (v, vw, o, c, h, l, t INTEGER PRIMARY KEY NOT NULL ON CONFLICT IGNORE, n)'
        self.cur.execute(query)

        query = 'INSERT OR IGNORE INTO ' + self.__ticker + ' VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
        for item in self.__lista:
            self.cur.execute(query, tuple(item.values()))
        self.con.commit()

        query = 'CREATE TABLE IF NOT EXISTS RANGOS (ticker, fecha_inicio, fecha_fin)'
        self.cur.execute(query)
        self.con.commit()

        query = 'INSERT OR IGNORE INTO RANGOS VALUES(?, ?, ?)'
        self.cur.execute(query, tuple([self.__ticker, fecha_inicio, fecha_fin]))
        self.con.commit()

    def summary(self, ticker='*'):
        if ticker == '*':
            self.cur.execute(f"SELECT * FROM RANGOS")
        else:
            self.cur.execute(f"SELECT * FROM RANGOS WHERE ticker='{ticker}'")

        registros \
            = self.cur.fetchall()
        print(f'\n{"Item":5}{"Ticker":13}{"Fecha inicial":19}{"Fecha final":19}')
        item = 0
        for registro in registros:
            item += 1
            print(f'{str(item):5}{str(registro[0]):12} {str(registro[1]):19}{str(registro[2]):19}')
        return registros

    def get_ranges(self, ticker):
        lista = self.summary(ticker)
        while True:
            try:
                item = int(input('Seleccione el rango a graficar: '))
            except ValueError:
                print('Ingreso incorrecto !!!')
            else:
                if 0 < item <= len(lista):
                    return lista[item - 1]
                else:
                    print('Ingreso incorrecto !!!')

    def read(self, ticker):
        self.__ticker = ticker
        consulta = 'SELECT * FROM ' + self.__ticker + ' ORDER BY t ASC'
        try:
            dt_frame = pd.read_sql(con=self.con, sql=consulta, parse_dates={'t': {'unit': 'ms', 'errors': 'ignore'}})
        except Exception:
            print(f"{Fore.YELLOW}ERROR: Ticker no encontrado{Fore.RESET}")
            return pd.DataFrame(None)
        else:
            return dt_frame
