"""

This software reads a list of TXT files generated by XXXX software
and plot the Elevation Maps and Intersections of the segments in
the respective PNG file.

"""

from track_model.Track import Track
from track_reader.GPSVisualizerFileReader import GPSVisualizerFileReader
from track_viewer.TrackViewer import TrackViewer, TrackPlotInfo
from pathlib import Path


class PlotTrack:

    def set_track_from_gpsvisualizer_file(self, file_name):
        """
        Read GPS data from a file and set the track for this object
        """
        reader = GPSVisualizerFileReader()

        reader.read_file(file_name)
        self.set_track(reader.get_track())
        
        index = len(file_name)-file_name.rfind(".")-1
        self.image_file_name = file_name[:-index] + "png"
    

    def set_track(self, track: Track):
        """
        Set the track data for this object
        """
        self.track = track


    def plot_track(self, file_name=None):
        """
        Plot the track data and save as an image file
        """

        if not self.track:
            raise Exception("There is no track no plot.")
        
        if not file_name:
            file_name = self.image_file_name

        title = Path(file_name).stem

        pInfo = TrackPlotInfo(self.track, title)
        pInfo.ExtractTrackData()

        viewer = TrackViewer()    
        plot1 = viewer.BuildPlot(pInfo, intersection_window=20)
        viewer.SavePlotAs(plot1, file_name)

        plot1.close()



def main(fileToParse):
    nuevaLista = CheckArgs(fileToParse)
    print("\n".join(nuevaLista))

    finalList = CheckFileList(nuevaLista)
    
    print ('\nFiles to plot:')
    print("\n".join(finalList))

    plotter = PlotTrack()

    for f in finalList:
        print ("Plotting file '", f, "' ...........", end= " ")
        plotter.set_track_from_gpsvisualizer_file(f)
        plotter.plot_track()
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