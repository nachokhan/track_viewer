"""

This software reads a list of TXT files generated by XXXX software
and plot the Elevation Maps and Intersections of the segments in
the respective PNG file.

"""

from TrackReader import GPSVisualizerFileReader
from trackdatamodel import Track
from TrackViewer import TrackViewer, TrackPlotInfo
from pathlib import Path
import sys


def Plotear(fileName):
    
    reader = GPSVisualizerFileReader()
    reader.ReadFile(fileName)
    track = reader.GetTrack()

    index = len(fileName)-fileName.rfind(".")-1
    imageName = fileName[:-index] + "png"

    title = Path(fileName).stem

    pInfo = TrackPlotInfo(track, title)
    pInfo.ExtractTrackData()

    viewer = TrackViewer()    
    plot1 = viewer.BuildPlot(pInfo, intersection_window=20)
    viewer.SavePlotAs(plot1, imageName)

    plot1.close()


def main(fileToParse):
    nuevaLista = CheckArgs(fileToParse)
    print("\n".join(nuevaLista))

    finalList = CheckFileList(nuevaLista)
    
    print ('\nFiles to plot:')
    print("\n".join(finalList))

    for f in finalList:
        print ("Plotting file '", f, "' ...........", end= " ")
        Plotear(f)
        print ("Done!")



def  CheckArgs(fileToParse):
    """ Check the Argv list to perfmorm different actions """
    nuevaLista = []

    # If no parameter is used: show error + example
    if len(fileToParse) == 0:
        print("Use with list of txt file to parse:\nI.e. 1: python plottxt.py file1.txt file2.txt file3.txt\nI.e. 2: python plottxt.py *")

    # If given an "*": examine all files in the folder
    elif len(fileToParse) == 1 and fileToParse[0].endswith("*"):
        direct = Path(fileToParse[0][:-1])
        nuevaLista = []
        for elem in direct.iterdir():
            file = Path(elem)
            if file.is_file():
                nuevaLista.append(str (file.absolute()))
    
    else:
        nuevaLista = fileToParse
     
    return nuevaLista

def CheckFileList(fileToParse):
    """ Removes those files that don't exists in the list """
    finalList = list(fileToParse)

    for f in fileToParse:
        file = Path(f)
        if not file.exists() or not file.is_file():
            print ("File ", f, "not found or is not a file. Removed from list")
            finalList.remove(f)    
    return finalList

if __name__ == "__main__":
    main()