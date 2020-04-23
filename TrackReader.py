""" 
TrackReader Module
This module manages all the needed functions to read the
Track info saved in the data files.

This data files are TXT in the form indicated by the
GPS Visualizer (https://www.gpsvisualizer.com/)

Info about the format is available under:
https://www.gpsvisualizer.com/tutorials/tracks.html
"""

from math import sin, cos, sqrt, atan2, radians

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


#########
# GPS Point represents a GPS point data.
#########
class GPSPoint:
    def __init__(self, lat, lon, elev):
        self.Latitude = float(lat)
        self.Longitude = float(lon)
        self.Elevation = float(elev)

    def DistanceTo(self, point):
        delta_x = self.h_distance_to(point)
        delta_y = abs(self.Elevation - point.Elevation)        
        d = sqrt( delta_x**2 + delta_y**2)        
        return d
    
    def h_distance_to(self, p2):
        R = 6373.0
        lat1, lon1 = radians(self.Latitude), radians(self.Longitude)
        lat2, lon2 = radians(p2.Latitude), radians(p2.Longitude)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c * 1000
        return distance


#########
# Segments represents a collection of GPS Points that were defined
# as a Segment, that means, a part of whole route.
#########
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


#########
# Track represents a collection of Segments (ideally correlatives segments)
#########
class Track:
    def __init__(self):
        self.__segments = []
        self.__northest_point = None
        self.__southest_point = None
        self.__westest_point = None
        self.__eastest_point = None
    
    def AddSegment(self, segment):
        """ Add a new segment to the track """
        self.__segments.append(segment)
    
    def GetLength(self):
        """ Returns the length of the whole Track """
        d = 0
        for segment in self.__segments:
            d += segment.GetLength()
        return d

    def GetSegments(self):
        """ Returns all the segments in the track """
        return self.__segments

    def GetBoundaries(self):
        """ Return Boundary Box as tuple (MinLon, MaxLon, MinLat, MaxLat) """
        minLon = self.__westest_point[0]
        maxLon = self.__eastest_point[0]
        minLat = self.__southest_point[1]
        maxLat = self.__northest_point[1]
        return (minLon, maxLon, minLat, maxLat)

    def GetExtremPoint(self, direction):

        if not self.__northest_point:
            self.__calcExtremPoints()
        
        if direction.lower() == "n": return self.__northest_point
        elif direction.lower() == "s": return self.__southest_point
        elif direction.lower() == "w": return self.__westest_point
        elif direction.lower() == "e": return self.__eastest_point

    def __calcExtremPoints(self):
        """ Calculate Extrem points thourgh all points """
        points=[]
        for s in self.__segments:
            for p in s.GetPoints():
                points.append( (p.Latitude, p.Longitude ))

        self.__northest_point = max(points,key=lambda item:item[1])
        self.__southest_point = min(points,key=lambda item:item[1])
        self.__westest_point = max(points,key=lambda item:item[0])
        self.__eastest_point = min(points,key=lambda item:item[0])


    def GetElevationExtremes(self):
        """ Returns the maximum and the minimum elevations of the track"""
        min, max = self.__segments[0].GetElevationExtremes()
        for s in self.__segments:
            m, M = s.GetElevationExtremes()
            if M > max: max = M
            if m < min: min = m

        return (min, max)