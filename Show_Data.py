import matplotlib.pyplot as plt
import pandas as pd
import datetime

class Show_Data():
#todo corregir ausencia de datos para que no interpole
#todo corregir que las lineas secundarias no coinciden con los ticks
    def graph(self, dtf, ticker):
        #print(dtf.to_string())
        index = pd.date_range('4/1/2021', periods=740, freq='1D')
        # print(index)
        # df2 = dtf.resample(index)
        # print(df2)


        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.21)
        #    ax.set_xticks = (20)

        ax.set_xlabel('Fecha')
        ax.tick_params(axis='x', labelrotation=-45, width=2, which='major')
        ax.tick_params(axis='y', grid_alpha=0.8, width=2, which='major')
        ax.tick_params(axis='both', grid_alpha=0.8, which='minor')
        ax.grid(color='gray', linestyle='-', alpha=0.8, linewidth=1, which='major')
        ax.grid(color='gray', linestyle='-', alpha=0.5, linewidth=0.5, which='minor')
        ax.set_ylabel('USD')
        ax.set_title('Ticker: ' + ticker)

        print(ax.set_xlim(datetime.date(2021, 1, 4), datetime.date(2021, 3, 1)))

        ax.plot(dtf.t, dtf.o, label='Valor de apertura')
        ax.plot(dtf.t, dtf.c, label='Valor de cierre')
        ax.plot(dtf.t, dtf.l, label='Valor mínimo')
        ax.plot(dtf.t, dtf.h, label='Valor máximo')
        plt.minorticks_on()
        plt.legend()
        plt.show()




