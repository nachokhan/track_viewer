from TrackReader import TrackFileReader
from pathlib import Path
import matplotlib.pyplot as plt
import sys

from trackdatamodel.Segment import Segment
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

def f_showAcc():
    reader = TrackFileReader()
    reader.ReadFile("./data/rincon1.txt")

    track = reader.GetTrack()    

    segments = track.GetSegments()

    dis = 0
    acc = 0
    acc2 = 0
    curv=0

    fig = plt.figure(figsize=(55, 25))
    fig.suptitle("CURVES", size="xx-large")
    grid = plt.GridSpec(1, 1, wspace=0.5, hspace=0.5)
    ax1 = fig.add_subplot(grid[0, 0])

    for seg in segments:
       
        curvis, puntis = seg.GetCurves(min_degree=40)

        puntos = seg.GetPoints()

        eje_x = [( i.Longitude  ) for i in seg.GetPoints()]
        eje_y = [( i.Latitude  ) for i in seg.GetPoints()]
        ax1.plot(eje_x, eje_y, color = "blue")
        eje_x2 = []
        eje_y2 = []

        for i in puntis:
            eje_x2.append( puntos[i].Longitude)
            eje_y2.append( puntos[i].Latitude)
        
        eje_x3 = []
        eje_y3 = []
        t=0
        for i in range(0, len(puntis)-2, 3):
            i1,i2,i3 = puntis[i], puntis[i+1], puntis[i+2]
            eje_x3.append( (puntos[i1].Longitude, puntos[i2].Longitude,  puntos[i3].Longitude) )
            eje_y3.append( (puntos[i1].Latitude, puntos[i2].Latitude,  puntos[i3].Latitude) )
            ax1.plot(eje_x3[t], eje_y3[t], color = "red")
            t=t+1


        print("SEGMENTO")
        print ("\tDist ->: ", round(seg.GetLength(),2), "m")
        print ("\tAcc+ ->: ", round(seg.GetAccElevation(),2), "m")
        print ("\tAcc- ->: ", round(seg.GetAccDescent(),2), "m")
        print ("\tCurv ->: ", curvis, " curves")
        dis += seg.GetLength()
        acc += seg.GetAccElevation()
        acc2 += seg.GetAccDescent()
        curv += curvis
        
        ax1.scatter(eje_x, eje_y, color = "green")
        ax1.scatter(eje_x2, eje_y2, color = "red")
        plt.show()
        


    print ("\nTOTAL:")
    print ("\tDist ->: ", round(dis,2), "m")
    print ("\tAcc+ ->: ", round(acc,2), "m")
    print ("\tAcc- ->: ", round(acc2,2), "m")
    print ("\tCurv ->: ", curv, " curves")

    print ("HOLA")


if __name__ == "__main__":
    f_showAcc()
    