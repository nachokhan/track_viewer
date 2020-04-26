""" 
TrackReader Module
This module manages all the needed functions to read the
Track info saved in the data files.

This data files are TXT in the form indicated by the
GPS Visualizer (https://www.gpsvisualizer.com/)

Info about the format is available under:
https://www.gpsvisualizer.com/tutorials/tracks.html
"""

from trackdatamodel.GPSPoint import GPSPoint
from trackdatamodel.Segment import Segment
from trackdatamodel.Track import Track

#########
# TrackFileReader Class represents an object that reads a text file 
# with gps segments and saves this data as a List Of Segments.
#########
class TrackFileReader:

    def __init__ (self):
        self.__segment = Segment()
        self.__track = Track()

    # Reads a text File by analizing and saving all the segments in the file    
    def ReadFile(self, fileName):
        """ Reads a TXT File with Segments and stores them """
        f = open(fileName, "r")
        lines = f.readlines()
        for line in lines:
            self.analyzeLine(line)
        f.close()

    # Analyzes a line in order to extract a gps point or a "start of segment"
    def analyzeLine(self, line):
        first_element = line.split(",")[0]

        if first_element == 'T':
            point, name, color = self.GetValuesFromLine(line)
            self.__segment.AddPoint(point)
            self.__segment.SetColor(color)
            self.__segment.SetName(name)

        elif first_element == 'type' :
            self.__segment = Segment()          
            self.__track.AddSegment(self.__segment)           
        
    # Read the lines and obtain the values
    def GetValuesFromLine(self, line):
        values = line.split(",")
        p = GPSPoint(values[1],values[2],values[3])
        name = values[4]
        color = values[5][:-1]
        return (p, name, color)


    # Returns all the segments in the file.
    def GetTrack(self):
        """ Returns the Track readed fro mthe file """
        return self.__track


