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
    reader.ReadFile("./data/rocas1.txt")

    track = reader.GetTrack()    

    segments = track.GetSegments()

    dis = 0
    acc = 0
    acc2 = 0
    curv=0   

    for seg in segments:

        fig = plt.figure(figsize=(55, 25))
        fig.suptitle("CURVES", size="xx-large")
        grid = plt.GridSpec(1, 1, wspace=0.5, hspace=0.5)
        ax1 = fig.add_subplot(grid[0, 0])
       
        curvis, intensidad, puntis = seg.GetCurves(min_degree = 40, min_p_sep = 4)

        puntos = seg.GetPoints()

        # Show the whole route
        eje_x = [( i.Longitude  ) for i in seg.GetPoints()]
        eje_y = [( i.Latitude  ) for i in seg.GetPoints()]
        ax1.plot(eje_x, eje_y, color = "blue")        
        eje_x2 = []
        eje_y2 = []
        for i in puntis:
            eje_x2.append( puntos[i].Longitude)
            eje_y2.append( puntos[i].Latitude)
        

        # PAINT SMALL LINES SHOWING EACH CURVES
        # For this must be enabled de three "appends" in method Segment.GetCurves()
        #eje_x3 = []
        #eje_y3 = []
        #t=0
        #for i in range(0, len(puntis)-2, 3):
        #    i1,i2,i3 = puntis[i], puntis[i+1], puntis[i+2]
        #    eje_x3.append( (puntos[i1].Longitude, puntos[i2].Longitude,  puntos[i3].Longitude) )
        #    eje_y3.append( (puntos[i1].Latitude, puntos[i2].Latitude,  puntos[i3].Latitude) )
        #    ax1.plot(eje_x3[t], eje_y3[t], color = "red")
        #    t=t+1

        # Show some Segment info on the console
        print("SEGMENTO")
        print ("\tDist ->: ", round(seg.GetLength(),2), "m")
        print ("\tAcc+ ->: ", round(seg.GetAccElevation(),2), "m")
        print ("\tAcc- ->: ", round(seg.GetAccDescent(),2), "m")
        print ("\tCurv ->: ", curvis, " curves")
        dis += seg.GetLength()
        acc += seg.GetAccElevation()
        acc2 += seg.GetAccDescent()
        curv += curvis
        
        ax1.scatter(eje_x, eje_y, color = "green")     # Paint ALL points
        ax1.scatter(eje_x2, eje_y2, color = "red")      # Paint ONLY CURVE POINTS
        plt.show()

        plt.close()
        


    print ("\nTOTAL:")
    print ("\tDist ->: ", round(dis,2), "m")
    print ("\tAcc+ ->: ", round(acc,2), "m")
    print ("\tAcc- ->: ", round(acc2,2), "m")
    print ("\tCurv ->: ", curv, " curves")

    print ("HOLA")


from naquever.prob_curvas import puntos_1 as pts1
from naquever.prob_curvas import puntos_2 as pts2
from naquever.prob_curvas import puntos_3 as pts3
from naquever.prob_curvas import puntos_4 as pts4
from naquever.prob_curvas import contar_curvas as contar


def RevisarCurvas(pts):
    a,b,c = contar(pts, 45)

    print("Curvas: ", a)

    #for i in range (0, a):
    #    print ("\nIntens: ", b[i])
    #    print ("Pto: (",c[i], ") = ", pts[c[i]])

    return c

def chiqui():

    fig = plt.figure(figsize=(55, 25))
    fig.suptitle("CURVES", size="xx-large")
    grid = plt.GridSpec(2, 2, wspace=0.5, hspace=0.5)
    ax1 = fig.add_subplot(grid[0, 1])
    ax2 = fig.add_subplot(grid[1, 1])
    ax3 = fig.add_subplot(grid[1, 0])
    ax4 = fig.add_subplot(grid[0, 0])
    
    a1 = RevisarCurvas(pts1)
    a2 = RevisarCurvas(pts2)
    a3 = RevisarCurvas(pts3)
    a4 = RevisarCurvas(pts4)

    ejex1 = [(p[0]) for p in pts1]
    ejey1 = [(p[1]) for p in pts1]
    ejex2 = [(p[0]) for p in pts2]
    ejey2 = [(p[1]) for p in pts2]
    ejex3 = [(p[0]) for p in pts3]
    ejey3 = [(p[1]) for p in pts3]
    ejex4 = [(p[0]) for p in pts4]
    ejey4 = [(p[1]) for p in pts4]

    ax1.plot(ejex1, ejey1, color = "blue")
    ax2.plot(ejex2, ejey2, color = "blue")
    ax3.plot(ejex3, ejey3, color = "blue")
    ax4.plot(ejex4, ejey4, color = "blue")

    scat1x = [(pts1[p][0]) for p in a1]
    scat1y = [(pts1[p][1]) for p in a1]
    scat2x = [(pts2[p][0]) for p in a2]
    scat2y = [(pts2[p][1]) for p in a2]
    scat3x = [(pts3[p][0]) for p in a3]
    scat3y = [(pts3[p][1]) for p in a3]
    scat4x = [(pts4[p][0]) for p in a4]
    scat4y = [(pts4[p][1]) for p in a4]

    ax1.scatter(scat1x, scat1y, color = "green")
    ax2.scatter(scat2x, scat2y, color = "green")
    ax3.scatter(scat3x, scat3y, color = "green")
    ax4.scatter(scat4x, scat4y, color = "green")



    plt.show()



if __name__ == "__main__":
    
    f_showAcc()
    #chiqui()
   
    

   


    