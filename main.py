from TrackReader import TrackFileReader, Track
from TrackViewer import TrackViewer, TrackPlotInfo

def Hacer(fileName):
    
    reader = TrackFileReader()
    reader.ReadFile(fileName)
    track = reader.GetTrack()

    imageName = fileName[:-3] + "png"

    pInfo = TrackPlotInfo(track)
    pInfo.ExtractTrackData()

    viewer = TrackViewer()    
    plot1 = viewer.BuildPlot(pInfo)
    viewer.ShowPlot(plot1)



        

Hacer("./data/rincon1.txt")
