"""

GPSPoint
This class defines a unique point in the map with:

    - Longitude (equivalent to X coord)
    - Latitude  (equivalent to Y coord)
    - Elevation (equivalent to Z coord)

Main Public methods are:

    - DistanceTo (point p)  (the distance between p and itself)
    

"""
from math import sin, cos, sqrt, atan2, radians, degrees, atan

from geographiclib.geodesic import Geodesic

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

    def BearingWith(self, point):
        """ Return bearing between self and another point """
        lat1 = self.Latitude
        lat2 = point.Latitude
        lon1 = self.Longitude
        lon2 = point.Longitude

        dx = lon2-lon1
        dy = lat2-lat1

        if dx == 0:
            if dy < 0:
                return 180
            else:
                return 0

        tan = dy/dx
        
        ang = degrees(atan(tan))

        if dx < 0:
            pepe = -90
        else:
            pepe = 90

        return round (pepe-ang, 2)

    def SlopeWith(self, p2):
        """ Get the slope (in %) between a point a itself """
        delta_y = p2.Elevation - self.Elevation
        delta_x = self.h_distance_to(p2)

        return (delta_y / delta_x * 1000)
        
    
    def h_distance_to(self, p2):
        """ Returns the horizontal distance between a point itself,
        as there were at same elevation """
        R = 6373.0
        lat1, lon1 = radians(self.Latitude), radians(self.Longitude)
        lat2, lon2 = radians(p2.Latitude), radians(p2.Longitude)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c * 1000
        return distance

    