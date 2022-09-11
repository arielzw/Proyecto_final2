from Polygon_API import *
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

class Show_Data():

    def show(self, dtf, ticker):
        print(dtf)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_xlabel('Fecha')
        ax.tick_params(axis='x', labelrotation=-45, grid_color='r', grid_alpha=0.8)
        ax.set_ylabel('USD')
        ax.set_title('Ticker: ' + ticker)
        ax.plot(dtf.t, dtf.c, label='Valor de cierre')
        ax.plot(dtf.t, dtf.o, label='Valor de apertura')
        plt.legend()
        plt.show()







