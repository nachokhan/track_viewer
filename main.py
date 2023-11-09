import sys

from track_model.Segment import Segment
import plottxt
from tests import Curvas_01, Curvas_02
from tests import GPXRead_01
from tests import Analyzer_01
from tests import ConStrava

def f_plottxt():
    sys.argv.append("../track_analyzer/other/output/rincon2___/10/VIEW_05_03_250.txt")
    lista = sys.argv[1:]
    plottxt.main(lista)

if __name__ == "__main__":
    
    Curvas_02.main("data/gpx/strava_perilago.gpx", 10, scatter_all=False, scatter_curves=True, plot_curves=True)
    # Curvas_01.main()

    #GPXRead_01.main()

    #Analyzer_01.main()

    # ConStrava.main()
   
    