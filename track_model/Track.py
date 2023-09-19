#########
# Track represents a collection of Segments (ideally correlatives segments)
#########

from track_model.Segment import Segment
from track_model.GPSPoint import GPSPoint

class Track:
    def __init__(self):
        #Reality
        self.__segments = []
        self.__author = None
        self.__name = None

        #Truth
        self.__northest_point = None
        self.__southest_point = None
        self.__westest_point = None
        self.__eastest_point = None

    
    def add_segment(self, segment):
        """ Add a new segment to the track """
        self.__segments.append(segment)

    def add_segments(self, segments):
        """ Add a list of segments to the track """
        self.__segments += segments
        
    def get_segments(self):
        """ Returns all the segments in the track """
        return self.__segments
    
    def get_length(self):
        """ Returns the length of the whole Track """
        d = 0
        for segment in self.__segments:
            d += segment.GetLength()
        return d

    def set_name(self, name):
        self.__name = name
    
    def set_name(self):
        return self.__name

    def set_author(self, author):
        self.__author = author
    
    def get_author(self):
        return self.__author
    

    def get_boundaries(self):
        """ Returns Boundary Box as tuple (MinLon, MaxLon, MinLat, MaxLat) """
        if not self.__northest_point:
            self.__calc_extreme_points()

        minLon = self.__westest_point[0]
        maxLon = self.__eastest_point[0]
        minLat = self.__southest_point[1]
        maxLat = self.__northest_point[1]
        return (minLon, maxLon, minLat, maxLat)

    def get_extreme_point(self, direction):
        """ Returns the 'direction' extrem point. direcction is ('n','s','w' or 'e') """
        if not self.__northest_point:
            self.__calc_extreme_points()
        
        if direction.lower() == "n": return self.__northest_point
        elif direction.lower() == "s": return self.__southest_point
        elif direction.lower() == "w": return self.__westest_point
        elif direction.lower() == "e": return self.__eastest_point

    def __calc_extreme_points(self):
        """ Calculate Extrem points thourgh all points """
        points=[]
        for s in self.__segments:
            for p in s.GetPoints():
                points.append( (p.Latitude, p.Longitude ))

        self.__northest_point = max(points,key=lambda item:item[1])
        self.__southest_point = min(points,key=lambda item:item[1])
        self.__westest_point = max(points,key=lambda item:item[0])
        self.__eastest_point = min(points,key=lambda item:item[0])


    def get_elevation_extremes(self):
        """ Returns the maximum and the minimum elevations of the track"""
        min, max = self.__segments[0].GetElevationExtremes()
        for s in self.__segments:
            m, M = s.GetElevationExtremes()
            if M > max: max = M
            if m < min: min = m

        return (min, max)