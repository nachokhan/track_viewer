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



import plottxt

if __name__ == "__main__":
    sys.argv.append("../track_analyzer/other/output/rincon2___/10/VIEW_05_03_250.txt")

    lista = sys.argv[1:]

    print ("\nCHUPALA:\t")
    print("\n".join(lista))

    plottxt.main(lista)