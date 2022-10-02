import matplotlib.pyplot as plt
import datetime


class ShowData:
    def graph(self, dtf, ticker, rangos):
        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.21)

        ax.set_xlabel('Fecha')
        ax.tick_params(axis='x', labelrotation=-45, width=2, which='major')
        ax.tick_params(axis='y', grid_alpha=0.8, width=2, which='major')
        ax.tick_params(axis='both', grid_alpha=0.8, which='minor')
        ax.grid(color='gray', linestyle='-', alpha=0.8, linewidth=1, which='major')
        ax.grid(color='gray', linestyle='-', alpha=0.5, linewidth=0.5, which='minor')
        ax.set_ylabel('USD')
        ax.set_title('Ticker: ' + ticker)

        ax.set_xlim(datetime.datetime.strptime(rangos[1], '%Y-%m-%d'),
                    datetime.datetime.strptime(rangos[2], '%Y-%m-%d'))
        ax.plot(dtf.t, dtf.o, label='Valor de apertura')
        ax.plot(dtf.t, dtf.c, label='Valor de cierre')
        ax.plot(dtf.t, dtf.l, label='Valor mínimo')
        ax.plot(dtf.t, dtf.h, label='Valor máximo')

        plt.minorticks_on()
        plt.legend()
        plt.show()
