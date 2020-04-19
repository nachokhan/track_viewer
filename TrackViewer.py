from math import sin, cos, sqrt, atan2, radians

#########
# TrackFile Class represents an object that reads a text file with gps
# segments and saves this data as a List Of Segments.
#########
class TrackFile:

    def __init__ (self):
        self.Segment = Segment()
        self.ListOfSegments = []

    # Reads a text File by analizing and saving all the segments in the file    
    def ReadFile(self, fileName):

        f = open(fileName, "r")
        lines = f.readlines()
        for line in lines:
            self.AnalyzeLine(line)

        f.close()

    # Analyzes a line in order to extract a gps point or a "start of segment"
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
        
    
    # Gets the color part of the text line
    def GetColor(self, line):
        values = line.split(',')
        return values[-1][:-1]
    
    # Gets the GPS point of the text line.
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

    def GetDistance(self, method):        
        d = 0
        points_range = len(self.Points)-1
        for i in range (points_range):
            d += self.Points[i].DistanceTo(self.Points[i+1])
            self.__distance__ = d
        return self.__distance__
