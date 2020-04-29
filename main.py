import sys

from trackdatamodel.Segment import Segment
import plottxt
from Pruebas import Curvas_01, Curvas_02
from Pruebas import GPXRead_01

def f_plottxt():
    sys.argv.append("../track_analyzer/other/output/rincon2___/10/VIEW_05_03_250.txt")
    lista = sys.argv[1:]
    plottxt.main(lista)

if __name__ == "__main__":
    
    #Curvas_02.main("./data/txt/rincon1.txt", 50, scatter_all=False, scatter_curves=True, plot_curves=True)
    #Curvas_01.main()

    GPXRead_01.main()


   
    