from TrackAnalyzer import *
from track_reader.GPSVisualizerFileReader import GPSVisualizerFileReader
from track_reader.GPXFileReader import GPXFileReader


from TrackViewer import TrackPlotInfo, TrackViewer

from TrackJudge import CalcSegmentDifficulty, CalcTrackDifficulty, FIETS_Index, ClimByBike_Index

from matplotlib import pyplot as plt

def Prueba_GetSlopeChanges():
    read = GPSVisualizerFileReader()
    track = read.read_file("./data/txt/rincon1.txt")
    
    segments = track.get_segments()


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
            nuevSeg.add_point(p)


    pos = get_slope_sign_change_position(nuevSeg)
        
    points = nuevSeg.get_points()

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

def Prueba_ExtractSegments(must_plot = True):   

    read2 = GPXFileReader("./data/gpx/pampa.gpx")

    track = read2.read()

    newTrack = extract_segment_1(track)

    dif = CalcTrackDifficulty(newTrack, method=FIETS_Index, curves=False )
    print ("\n FIETS: ", dif, "\n")
    dif = CalcTrackDifficulty(newTrack, method=ClimByBike_Index, curves=False )
    print ("\n CLIMB: ", dif, "\n")

    if must_plot == True:
        plotInfo = TrackPlotInfo(newTrack)
        plotInfo.ExtractTrackData(automatic_colors=True)
        vie = TrackViewer()
        plot = vie.BuildPlot(plotInfo, max_cols=3)
        vie.ShowPlot(plot)
        vie.ClearPlot(plot)
        

def make_all_Segments(must_plot = False):
    import glob

    files = [f for f in glob.glob("./data/gpx/sub/*.gpx", recursive=False)]
    #files = [f for f in glob.glob("./data/gpx/*.gpx", recursive=False)]

    files.sort()

    text = "Ruta, FIETS, CLIMB, FIETS(C), CLIMB(C)\n"

    for f in files:

        l1 = f.rfind("/")+1

        print ("Processing ", f[l1:-4], "...\t", end =" ")
        read2 = GPXFileReader(f)
        track = read2.read()
        newTrack = extract_segment_1(track)
        dif1 = round(CalcTrackDifficulty(newTrack, method=FIETS_Index, curves=False ), 1)
        
        text += "{0},{1}\n".format(f[l1:-4], dif1)
        
        if must_plot == True:
            plotInfo = TrackPlotInfo(newTrack)
            plotInfo.ExtractTrackData()
            vie = TrackViewer()
            print ("\tPloting....  ", end =" ")
            plot = vie.BuildPlot(plotInfo)
            vie.SavePlotAs(plot, f+".png")
            vie.ClearPlot(plot)
        print ("Ok  .", end = " ")
        print (" - DIFF: ", str(round(dif1,2)))

    f = open("comp.txt", "w")    
    f.write(text)
    f.close()

    print ("READY! :)")

def main():
    #Prueba_GetSlopeChanges()
    #Prueba_ExtractSegments( )
    make_all_Segments(True)


  
    
  