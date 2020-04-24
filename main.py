from TrackReader import TrackFileReader, Track
from TrackViewer import TrackViewer, TrackPlotInfo
from pathlib import Path
import sys


def Hacer(fileName):
    
    reader = TrackFileReader()
    reader.ReadFile(fileName)
    track = reader.GetTrack()

    index = len(fileName)-fileName.find(".")-1
    imageName = fileName[:-index] + "png"

    title = Path(fileName).stem

    pInfo = TrackPlotInfo(track, title)
    pInfo.ExtractTrackData()

    viewer = TrackViewer()    
    plot1 = viewer.BuildPlot(pInfo, intersection_window=40)
    viewer.ShowPlot(plot1)


#Hacer("./data/rincon1.txt")
