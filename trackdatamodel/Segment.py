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
from math import radians, degrees



class Segment:
    def __init__(self):
        self.__points = []
   
    def AddPoint(self, point):
        """ Adds a new GPS point to the segment """
        self.__points.append(point)

    def AddPoints(self, points):
        """ Adds a list of points to the segment """
        self.__points += points

    def GetRawSlope(self):
        """ Returns the raw slope of the whole segment (p0 -> pn) """
        dh = self.GetAccElevation()+self.GetAccDescent()
        dx = self.GetLength()
        if dx == 0: return 0
        return dh/dx * 100

    def GetAvSlope(self):
        """ Returns the slope average of the whole segment """
        l = len(self.__points)
        av = 0
        for i in range (1, l):
            av += self.__points[i].SlopeWith(self.__points[i-1])
        
        return -av/l # slope is inverted here because comparing p2 with p1

    def GetPoints(self):
        """ Return a list of points """
        return self.__points

    def GetLength(self):
        """ Returns the lenght of the whole segment in meters """      
        d = 0
        points_range = len(self.__points)-1
        for i in range (points_range):
            d += self.__points[i].DistanceTo(self.__points[i+1])
        return d

    def GetLengthUphills(self):
        l = len(self.__points)
        sum = 0
        for i in range (1, l):
            slope = self.__points[i].SlopeWith(self.__points[i-1])            
            if slope < 0: # slope is inverted here because comparing p2 with p1
                sum += self.__points[i].DistanceTo(self.__points[i-1])            
        
        return sum

    def GetLengthDownhills(self):
        l = len(self.__points)
        sum = 0
        for i in range (1, l):
            slope = self.__points[i].SlopeWith(self.__points[i-1])            
            if slope > 0: # slope is inverted here because comparing p2 with p1
                sum += self.__points[i].DistanceTo(self.__points[i-1])            
        
        return sum
        return 0

    def GetLengthNoSlope(self):
        l = len(self.__points)
        sum = 0
        for i in range (1, l):
            slope = self.__points[i].SlopeWith(self.__points[i-1])            
            if slope == 0:
                sum += self.__points[i].DistanceTo(self.__points[i-1])            
        
        return sum

    def GetElevationExtremes(self):
        """ Returns the maximum and the minimum elevations of the segment"""
        max = min = self.__points[0].Elevation
        for p in self.__points:
            if p.Elevation > max: max = p.Elevation
            if p.Elevation < min: min = p.Elevation

        return (min, max)

    def GetAccElevation(self):
        """ Returns the accumulated ascending elevation of the segment """
        acc = 0
        q_points = len(self.__points)-1
        for i in range (0, q_points):
            p1 = self.__points[i]
            p2 = self.__points[i+1]
            diff = p2.Elevation - p1.Elevation

            if diff > 0:
                acc += diff
        return  acc

    def GetAccDescent(self):
        """ Returns the accumulated descending elevation ('-' sign) of the segment """
        acc = 0
        q_points = len(self.__points)-1
        for i in range (0, q_points):
            p1 = self.__points[i]
            p2 = self.__points[i+1]
            diff = p2.Elevation - p1.Elevation

            if diff < 0:
                acc += diff
        return  acc

    def GetCurves(self, min_degree = 80, min_p_sep=5):
        """Return quatity of curves in the segment that have at least X dgrees

        Keyword Arguments:
            min_degree {int} -- Min angle to be considered "curve" (default: {80})
            min_p_sep {int} -- Mini separation between points(default: {5})

        Returns:
            curves_count {int} -- Quantity of curves detected
            degrees {list} -- Degree of each curve
            mid_points_curves {list} -- Each index with the "middle point" of the curve
            curves {list(tuples)} -- list of tuples with the "curves" itself.
        """
        curves_count = 0        # Of cours, curves counter
        mid_points = []         # Points of the middle point of each curve
        curves = []             # tuples (3 points each) with each curve
        degrees = []            # STRONGNESS of each curve (how "eng" is)        
        q_points = len(self.__points)-2
        for i in range (0, q_points):
            p1 = self.__points[i]
            p2 = self.__points[i+1]
            p3 = self.__points[i+2]

            p2, i2 = self._getNextPoint(p1, i+1)
            p3, i3 = self._getNextPoint(p2, i2+1)

            d1 = p1.DistanceTo(p2)
            d2 = p2.DistanceTo(p3)

            b1 = p1.BearingWith(p2)
            b2 = p2.BearingWith(p3)

            diff = abs(b2-b1)

            if diff >= min_degree:#  and d1 >= min_p_sep and d2 >= min_p_sep:
                curves_count += 1
                mid_points.append(i2)
                curves.append( (i, i2, i3) )
                degrees.append( round(diff, 2) ) 
                

        return curves_count, degrees, mid_points, curves

    def _getNextPoint(self, prev_p, index):
        """ Returns the next point closer (min MIN_DISTANCE meters) to work with """
        MIN_DISTANCE = 10

        if index >= len(self.__points):
            return self.__points[index-1], index-1
        
        p = self.__points[index]

        dist = p.DistanceTo(prev_p)

        if  dist < MIN_DISTANCE:
            p, index = self._getNextPoint(prev_p, index+1)
        
        return p, index

    

""" 
Its a Segment designed to be ploted.
It adds a color and maybe a name.
"""
class DrawableSegment(Segment):
    def __init__(self):
        Segment.__init__(self)
        #super().__init__()
        self.__color = "red"
        self.__name = "noname"

    def SetColor(self, color):
        """ Sets the color to plot the segment """
        self.__color = color
    
    def GetColor(self):
        """ Returns the color to plot the segment """
        return self.__color
    
    def SetName(self, name):
        """ Sets the name of the segment """
        self.__name = name

    def GetName(self):
        """ Returns the name of the segment """
        return self.__name