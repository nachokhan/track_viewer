from geopy import distance
import math

#########
# TrackFile Class represents an object that reads a text file with gps
# segments and saves this data as a List Of Segments.
#########
class TrackFile:

    def __init__ (self):
        self.Segment = Segment()
        self.ListOfSegments = []

    ###
    # Reads a text File by analizing and saving all the segments in the file
    ###
    def ReadFile(self, fileName):

        f = open(fileName, "r")
        lines = f.readlines()
        for line in lines:
            self.AnalyzeLine(line)

        f.close()

    ###
    # Analyzes a line in order to extract a gps point or a "start of segment"
    ###
    def AnalyzeLine(self, line):
        first_element = line.split(",")[0]

        if first_element == 'T':
            point = self.GetPoint(line)
            color = self.GetColor(line)
            self.Segment.AddPoint(point)
            self.Segment.SetColor(color)

        elif first_element == 'type' :
            self.Segment = Segment()          
            self.ListOfSegments.append(self.Segment)           
        
    
    ###
    # Gets the color part of the text line
    ###
    def GetColor(self, line):
        values = line.split(',')
        return values[-1][:-1]
    
    ###
    # Gets the GPS point of the text line.
    ###
    def GetPoint (self, line):
        values = line.split(',')
        return GPSPoint(values[1],values[2],values[3])


#########
# GPS Point represents a GPS point data.
#########
class GPSPoint:
    def __init__(self, lat, lon, elev):
        self.Latitude = float(lat)
        self.Longitude = float(lon)
        self.Elevation = float(elev)

    def DistanceTo(self, point, consider_elevation=True):
        this_point = (self.Latitude, self.Longitude)
        other_point = (point.Latitude, point.Longitude)

        delta_x = distance.distance(this_point, other_point).meters
        delta_y = abs(self.Elevation - point.Elevation)
        
        if consider_elevation:
            d = math.sqrt( delta_x*delta_x + delta_y*delta_y)
        else:
            d = delta_x
        
        return d


#########
# Segments represent a collection of GPS Points that were defined
# as a Segment, that means, a part of whole route.
#########
class Segment:
    def __init__(self):
        self.Points = []
        self.Color = "red"
    
    def AddPoint(self, point):
        self.Points.append(point)

    def SetColor(self, color):
        self.Color = color
    
    def GetColor(self):
        return self.Color

    def GetSlope(self):
        return 0 # todo

    def GetDistance(self, consider_elevation=True):
        d = 0
        for i in range (len(self.Points)-1):
            d += self.Points[i].DistanceTo(self.Points[i+1], consider_elevation)        
        return d
