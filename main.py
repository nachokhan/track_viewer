from TrackReader import TrackFileReader, Track
from TrackViewer import TrackViewer

def Hacer(fileName):
    t = TrackFileReader()
    t.ReadFile(fileName)
    track = t.GetTrack()

    g = TrackViewer()
    g.BulidPlot(track)
        

Hacer("./data/rincon1.txt")
