from TrackReader import TrackFileReader, Track
from TrackViewer import TrackViewer, TrackPlotInfo

def Hacer(fileName):
    t = TrackFileReader()
    t.ReadFile(fileName)
    track = t.GetTrack()

    g = TrackViewer()
    plotInfo = g.GetPlotInfo(track)

    ploti = g.BuildPlot(plotInfo)

    g.SavePlotAs(ploti, fileName[:-3] + "png")

        

Hacer("./data/rincon1.txt")
