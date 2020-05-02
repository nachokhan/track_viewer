from TrackAnalyzer import *
from Pruebas.prob_curvas import puntos_1 as pts1
from TrackReader import GPSVisualizerFileReader
from TrackReader import GPXFileReader


from TrackViewer import TrackPlotInfo, TrackViewer


from matplotlib import pyplot as plt

def Prueba_GetSlopeChanges():
    read = GPSVisualizerFileReader()
    track = read.ReadFile("./data/txt/rincon1.txt")
    
    segments = track.GetSegments()


    fig = plt.figure(figsize=(55, 25))
    fig.suptitle("slopes", size="xx-large")
    grid = plt.GridSpec(1, 1, wspace=0.5, hspace=0.5)
    ax1 = fig.add_subplot(grid[0, 0])


    pos = []
    ejesx = []
    ejesy = []


    points = []
    nuevSeg = Segment()
    for s in segments:
        points = s.GetPoints()

        for p in points:
            nuevSeg.AddPoint(p)


    pos = GetSlopeSignChangesPosition(nuevSeg)
        
    points = nuevSeg.GetPoints()

    dist=[0]
    eles=[points[0].Elevation]

    for i in range (1, len(points)):
        dist.append(dist[i-1] + points[i].DistanceTo(points[i-1]))
        eles.append(points[i].Elevation)

    print (len(points))
    print (len(dist))
    print (len(pos))

    l1 = 0
    l2 = l1 + 2300

    colors = ["red", "blue", "green", "black"]

    prev = 0
    c = 0
    for i in range(len(pos)):
        p = pos[i]
        x = dist[p]
        if p >=l1 and p <=l2:
            xx = dist[prev:pos[i+1]]
            yy = eles[prev:pos[i+1]]
            ax1.plot( xx , yy,  color = colors[c])
            ax1.axvline( x, 0, str(x), color = "blue")
            #ax1.scatter(xx, yy, color = "black")
            if c == 3 : c = -1
            c=c+1            
        prev = p        
                 
    plt.show()

    plt.close()

def Prueba_ExtractSegments():   

    read2 = GPXFileReader("./data/gpx/rocas_deu.gpx")

    track = read2.Read()

    newTrack = ExtractSegments_1(track)

    plotInfo = TrackPlotInfo(newTrack)
    plotInfo.ExtractTrackData(automatic_colors=True)

    vie = TrackViewer()
    plot = vie.BuildPlot(plotInfo, max_cols=3)

    vie.ShowPlot(plot)
    vie.ClearPlot(plot)
    

def make_all_Segments():
    import glob

    files = [f for f in glob.glob("./data/gpx/*.gpx", recursive=False)]

    for f in files:
        print ("Processing ", f, "...", end =" ")
        read2 = GPXFileReader(f)
        track = read2.Read()
        newTrack = ExtractSegments_1(track)
        plotInfo = TrackPlotInfo(newTrack)
        plotInfo.ExtractTrackData()
        vie = TrackViewer()
        print (" Ploting....  ", end =" ")
        plot = vie.BuildPlot(plotInfo)
        vie.SavePlotAs(plot, f+".png")
        vie.ClearPlot(plot)
        print (" Finished! Ok  ")

    print ("READY! :)")

def main():
    #Prueba_GetSlopeChanges()

    Prueba_ExtractSegments()


  
    
  