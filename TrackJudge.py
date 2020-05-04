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
    
    dif = 2 * delta_h**2 / (distance * 10) + T

    return dif / 10 * 4


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



def Fisico_Index(segment):


    dif = 0
    ps = segment.GetPoints()

    for i in range (len(ps)-1):
        s = ps[i+1].Elevation - ps[i].Elevation
        sl = ps[i].SlopeWith(ps[i+1])

        if s > 0:
            fact = getSF(sl)
            dif += fact*s
        else:
            dif += -s/5

    return dif / 70


def getSF(sl):
    sl = abs(sl)
    if sl >= 0 and sl <  5: return 1.5
    if sl >  6 and sl <  7: return 2.5
    if sl >  8 and sl < 10: return 3
    if sl > 11 and sl < 13: return 3.5
    if sl > 14 and sl < 18: return 4
    if sl > 19 and sl < 25: return 5
    else: return 10

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
        #dif += CalcSegmentDifficulty(seg, method, curves)
        dif += Fisico_Index(seg)

    return dif

