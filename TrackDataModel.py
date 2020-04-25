"""
The Track Data Model contains the classes needed to define a Track 
with its segments, its points, and whatever we may need now and in 
the future.

It is a module with almost no calculations, and it contains only 
real data.

But what does "real data" means? Well, when we mess elevation with
a GPS device, we obtain a number. The same happens with the latitude, 
longitude, time, or even with the effort (if we have a special device 
that allow us to do it). We could even calculate the disnatce between
two points and it will be still "real data" because its already 
stablished how we can do it and we hace no inference on it.

So this is "real" data in the sense that we are not allowed to say 
"this is right" or "this is wrong". It just data that came to us 
from the outside. Note: when I say "us" I mean of course that "we" 
are this software. Have you ever wonder to be a software? Here is 
your opportunity ;)

Other type of values (or "data") like difficulty (that WE assign) would 
not be considered in this module. Because it is like "pollution" in the 
"fresh" model with data we dont't know if it is ok or not. This is the 
"I'm wrong, they're right" principle. I will consider that every 
information that comes to me from the outside world (or or every 
information that I can calculate with methods that come to me also from 
the outside world) is right. Why would I do this? Because it is not my 
fault who and how was it made. All I can do is take it, but no modify it. 
If I modify, e.g. the way distance between two GPS points are normally 
calculated, I may be adding an error because of my brain's potential 
defects. But if I use an standard method, then it is not my fault I it 
was wrong. The correction comes from the outside and all I have to do 
is replace it with the corrected version.
"""

from math import sin, cos, sqrt, atan2, radians

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