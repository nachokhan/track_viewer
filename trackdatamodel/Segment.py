"""

Segment
A segment is a collection of consecutive points in the map.
It represents a logic part of a whole Track. It means a track
consists of one or more consecutive segments.
The logic of where a segment starts and end depends on specific
algoritms that do this.

    - Longitude (equivalent to X coord)
    - Latitude  (equivalent to Y coord)
    - Elevation (equivalent to Z coord)

Main Public methods are:

    - GetSlope()                (average slope)
    - GetLength()               (total length from p[0] to p[N])
    - GetElevationExtremes()    (min and max elevation)
    - GetAccElevation()         (total amount of uphill's meters)
    

"""

from trackdatamodel.GPSPoint import GPSPoint

class Segment:
    def __init__(self):
        self.__points = []
        self.__color = "red"
        self.__name = "noname"
   
    def AddPoint(self, point):
        """ Adds a new GPS point to the segment """
        self.__points.append(point)

    def SetColor(self, color):
        """ Sets the color to plot the segment """
        self.__color = color
    
    def GetColor(self):
        """ Returns the color to plot the segment """
        return self.__color

    def GetSlope(self):
        """ Returns the slope of the whole segment """
        return 0 # todo

    def SetName(self, name):
        """ Sets the name of the segment """
        self.__name = name

    def GetName(self):
        """ Returns the name of the segment """
        return self.__name

    def GetPoints(self):
        """ Return a list of points """
        return self.__points

    def GetLength(self):
        """ Returns the lenght of the whole segment in meters """      
        d = 0
        points_range = len(self.__points)-1
        for i in range (points_range):
            d += self.__points[i].DistanceTo(self.__points[i+1])
            self.__distance__ = d
        return self.__distance__

    def GetElevationExtremes(self):
        """ Returns the maximum and the minimum elevations of the segment"""
        max = min = self.__points[0].Elevation
        for p in self.__points:
            if p.Elevation > max: max = p.Elevation
            if p.Elevation < min: min = p.Elevation

        return (min, max)