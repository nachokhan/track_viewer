"""

GPSPoint
This class defines a unique point in the map with:

    - Longitude (equivalent to X coord)
    - Latitude  (equivalent to Y coord)
    - Elevation (equivalent to Z coord)

Main Public methods are:

    - DistanceTo (point p)  (the distance between p and itself)
    

"""
from math import sin, cos, sqrt, atan2, radians

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