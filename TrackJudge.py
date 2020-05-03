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


def CalcSegmentDifficulty(segment, method):

    dh = segment.GetAccElevation() #+ segment.GetAccDescent()
    dx = segment.GetLength()
    alt = segment.GetElevationExtremes()[1]

    a = method(dh, dx, alt)

    print (str(round(a,2)) +", ", end = " ")

    return a


def CalcTrackDifficulty(track, method = FIETS_Index):

    dif = 0
    for seg in track.GetSegments():
        dif += CalcSegmentDifficulty(seg, method)

    return dif

