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
        """ Returns the accumulated descending elevation of the segment """
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
            min_degree {int} -- Minimun angle to be considered "curve" (default: {80})
            min_p_sep {int} -- Minimun separation between points to avoid noise (default: {5})

        Returns:
            curves {int} -- Quantity of curves detected
            intensities {list} -- Degree of each curve
            curve_points {list} -- Each index with a detected curve
        """
        curves = 0                      # Of cours, curves counter
        points_with_curve = []          # Points of the middle point of each curve
        curves_intenstities = []        # STRONGNESS of each curve (how "eng" is)
        q_points = len(self.__points)-2
        for i in range (0, q_points):
            p1 = self.__points[i]
            p2 = self.__points[i+1]
            p3 = self.__points[i+2]

            d1 = p1.DistanceTo(p2)
            d2 = p2.DistanceTo(p3)

            b1 = p1.BearingWith(p2)
            b2 = p2.BearingWith(p3)

            diff = abs(b2-b1)

            if diff >= min_degree  and d1 >= min_p_sep and d2 >= min_p_sep:
                curves += 1
                #points_with_curve.append(i)
                points_with_curve.append(i+1)
                #points_with_curve.append(i+2)
                curves_intenstities.append( round(diff, 2) ) 
                

        return curves, curves_intenstities, points_with_curve