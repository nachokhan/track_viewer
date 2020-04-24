from TrackReader import TrackFileReader, Track
from TrackViewer import TrackViewer, TrackPlotInfo
from matplotlib import pylab as plt
import math
from pathlib import Path

def Hacer(fileName):
    
    reader = TrackFileReader()
    reader.ReadFile(fileName)
    track = reader.GetTrack()

    imageName = fileName[:-3] + "png"

    title = Path(fileName).stem

    pInfo = TrackPlotInfo(track, title)
    pInfo.ExtractTrackData()

    viewer = TrackViewer()    
    plot1 = viewer.BuildPlot(pInfo)
    viewer.ShowPlot(plot1)


Hacer("./data/rincon1.txt")
