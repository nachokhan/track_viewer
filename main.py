from TrackReader import TrackFileReader
from pathlib import Path
import matplotlib.pyplot as plt
import sys


import plottxt
import TrackJudge

def f_plottxt():
    sys.argv.append("../track_analyzer/other/output/rincon2___/10/VIEW_05_03_250.txt")

    lista = sys.argv[1:]

    print ("\nCHUPALA:\t")
    print("\n".join(lista))

    plottxt.main(lista)

def f_index_generico():
    fig = plt.figure(figsize=(55, 25))
    fig.suptitle("HOLA", size="xx-large")
    grid = plt.GridSpec(2, 2, wspace=0.5, hspace=0.5)
    ax1 = fig.add_subplot(grid[0, 0])
    ax2 = fig.add_subplot(grid[0, 1])
    ax3 = fig.add_subplot(grid[1, 0])
    ax4 = fig.add_subplot(grid[1, 1])

  
    const = 1000
    x = range(100, 3000)
    meth = TrackJudge.FIETS_Index
    index1 = [( meth(const, i, 500)  ) for i in x]
    ax1.plot(x, index1)
    ax1.set_title("FIETS -> Acc Elevacion = 1000 m")
    ax1.set_xlabel("Distance (m)")    

    const = 2000
    x = range(50, 1500)
    meth = TrackJudge.FIETS_Index
    index2 = [( meth(i, const, 500)  ) for i in x]
    ax2.plot(x, index2)
    ax2.set_title("FIETS -> Distancia = 2000 m")
    ax2.set_xlabel("Acc Elevacion (m)")

    const = 1000
    x = range(100, 3000)
    meth = TrackJudge.ClimByBike_Index
    index3 = [( meth(const, i, 500)  ) for i in x]
    ax3.plot(x, index3)
    ax3.set_title("ClimByBike -> Acc Elevacion = 1000 m")
    ax3.set_xlabel("Distancia (m)")

    const = 2000
    x = range(50, 1500)
    meth = TrackJudge.ClimByBike_Index
    index4 = [( meth(i, const, 500)  ) for i in x]
    ax4.plot(x, index4)
    ax4.set_title("ClimByBike -> Distancia = 2000 m")
    ax4.set_xlabel("Acc Elevacion (m)")
    
    title = "Difficulty"
    ax1.set_ylabel(title)
    ax1.grid(True)
    ax2.set_ylabel(title)
    ax2.grid(True)
    ax3.set_ylabel(title)
    ax3.grid(True)
    ax4.set_ylabel(title)
    ax4.grid(True)

    plt.show()

def indexes():
    reader = TrackFileReader()
    reader.ReadFile("./data/arco_up.txt")

    track = reader.GetTrack()    

    segments = track.GetSegments()

    for seg in segments:
        points = seg.GetPoints()



    print ("HOLA")



if __name__ == "__main__":
    indexes()
    