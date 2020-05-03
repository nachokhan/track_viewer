from TrackReader import GPSVisualizerFileReader, GPXFileReader
import matplotlib.pyplot as plt

def main(filename, min_degree = 45, scatter_all = False, scatter_curves = True, plot_curves = True):
    f_showAcc(filename, min_degree, scatter_all, scatter_curves, plot_curves)

def f_showAcc(filename, degree, scatter_all, scatter_curves, plot_curves):
    reader = GPXFileReader(filename)
    track = reader.Read()

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

        c_count, intens, mid_p_curve, all_p_curve = seg.GetCurves(min_degree = degree, min_p_sep = 5)

        puntos = seg.GetPoints()

        # Show the whole route
        eje_x = [( i.Longitude  ) for i in seg.GetPoints()]
        eje_y = [( i.Latitude  ) for i in seg.GetPoints()]
        ax1.plot(eje_x, eje_y, color = "blue")

        # Build axes with the middle point of each curve
        eje_x2 = []
        eje_y2 = []
        for i in mid_p_curve:
            eje_x2.append( puntos[i].Longitude)
            eje_y2.append( puntos[i].Latitude)
        

        # PAINT SMALL LINES SHOWING EACH CURVES
        if plot_curves:
            eje_x3 = []
            eje_y3 = []
            t=0
            for i in range(0, len(all_p_curve)-2, 3):
                i1,i2,i3 = all_p_curve[i][0], all_p_curve[i][1], all_p_curve[i][2]
                eje_x3.append( (puntos[i1].Longitude, puntos[i2].Longitude,  puntos[i3].Longitude) )
                eje_y3.append( (puntos[i1].Latitude, puntos[i2].Latitude,  puntos[i3].Latitude) )
                ax1.plot(eje_x3[t], eje_y3[t], color = "red")
                t=t+1

        # Show some Segment info on the console
        print("SEGMENTO")
        print ("\tDist ->: ", round(seg.GetLength(),2), "m")
        print ("\tAcc+ ->: ", round(seg.GetAccElevation(),2), "m")
        print ("\tAcc- ->: ", round(seg.GetAccDescent(),2), "m")
        print ("\tCurv ->: ", c_count, " curves")
        dis += seg.GetLength()
        acc += seg.GetAccElevation()
        acc2 += seg.GetAccDescent()
        curv += c_count
        
        # Scatter ALL points
        if scatter_all:
            ax1.scatter(eje_x, eje_y, color = "green")     
        
        # Scatter ONLY Middle POINTS of curves
        if scatter_curves:
            ax1.scatter(eje_x2, eje_y2, color = "red")     

        plt.show()
        
        
    plt.close()       


    print ("\nTOTAL:")
    print ("\tDist ->: ", round(dis,2), "m")
    print ("\tAcc+ ->: ", round(acc,2), "m")
    print ("\tAcc- ->: ", round(acc2,2), "m")
    print ("\tCurv ->: ", curv, " curves")

    print ("HOLA")