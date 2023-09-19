""" 
GPSVisualizerFileReader Class
This class manages all the needed functions to read the
Track info saved in the data files.

This data files are TXT in the form indicated by the
GPS Visualizer (https://www.gpsvisualizer.com/)

Info about the format is available under:
https://www.gpsvisualizer.com/tutorials/tracks.html
"""

from track_model.GPSPoint import GPSPoint
from track_model.Segment import DrawableSegment
from track_model.Track import Track


class GPSVisualizerFileReader:

    def __init__ (self):
        self.__segment = DrawableSegment()
        self.__track = Track()

    # Reads a text File by analizing and saving all the segments in the file    
    def read_file(self, fileName):
        """ Reads a TXT File with Segments and stores them """
        f = open(fileName, "r")
        lines = f.readlines()
        for line in lines:
            self.analyze_line(line)
        f.close()
        
        return self.__track

    # Analyzes a line in order to extract a gps point or a "start of segment"
    def analyze_line(self, line):
        first_element = line.split(",")[0]

        if first_element == 'T':
            point, name, color = self.get_values_from_line(line)
            self.__segment.add_point(point)
            self.__segment.set_color(color)
            self.__segment.set_name(name)

        elif first_element == 'type' :
            self.__segment = DrawableSegment()
            self.__track.add_segment(self.__segment)           
        
    # Read the lines and obtain the values
    def get_values_from_line(self, line):
        values = line.split(",")
        p = GPSPoint(values[1],values[2],values[3])
        name = values[4]
        color = values[5][:-1]
        return (p, name, color)

    # Returns all the segments in the file.
    def get_track(self):
        """ Returns the Track readed fro mthe file """
        return self.__track


