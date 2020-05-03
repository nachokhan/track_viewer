"""
TrackJudge is the module thah gives an opinion of a track.
This means, based on different variables, the Jugde will 
emit a value of difficulty for a segment or a track.

Different variables to consider are:
    - Distance
    - Elevation
    - Accumulated Elevation
    - Slope
    - Altitude (masl)
    - Curves

Other variable to consider, but difficult to mess are:
    - Type of grund (asphalt, gravel road, rocks)
    - Lose ground
    - Obstacles 
    - Etc.
"""

def FIETS_Index(delta_h, distance, altitude):
    T = 0
    if altitude >= 1000:
        T = (altitude-1000) / 1000
    
    return delta_h**2 / (distance * 10)


def ClimByBike_Index(delta_h, distance, altitude):
    T = 0
    if altitude >= 1000:
        T = (altitude-1000) / 100

    T1 = (200 * delta_h / distance)
    T2 = (delta_h ** 2) / distance
    T3 = distance / 1000
        
    return T1 + T2 + T3 + T

def Curves_Difficulty (degrees, slopes, distance):
    sum = 0

    for i in range (0, len(degrees)):
        degree = degrees[i]
        pts = slopes[i]

        if degree >= 90:
            if len(pts) == 3:
                slope = (pts[0].SlopeWith(pts[2])+pts[1].SlopeWith(pts[2])) / 2
            else:
                slope = 0
            
            dif = GetCurveDifficulty(degree, slope)
            sum += dif

    return sum**2 / distance


def GetCurveDifficulty(degree, slope):

    a = -0.0044
    b = 0.99
    c = 1
        
    angle_factor = 1/16
    slope_factor = a * slope**2 + b * slope + c

    dif = degree * angle_factor * slope_factor

    return dif



def Nacho_Index(curves_intensity, distance):
    sum = 0

    
    

def CalcSegmentDifficulty(segment, method, take_curves):

    dh = segment.GetAccElevation() #+ segment.GetAccDescent()
    dx = segment.GetLength()
    alt = segment.GetElevationExtremes()[1]

    curves = segment.GetCurves()

    points = []
    for point in curves[3]:
        points.append(segment.GetPoints()[point[0]:point[2]])


    a = method(dh, dx, alt)
    curves_dif = Curves_Difficulty(curves[1], points, dx)

    if take_curves == True:
        a += curves_dif

    #print (str(round(a,2)) +", ", end = " ")

    return a


def CalcTrackDifficulty(track, method = FIETS_Index, curves = True):

    dif = 0
    for seg in track.GetSegments():
        dif += CalcSegmentDifficulty(seg, method, curves)

    return dif

