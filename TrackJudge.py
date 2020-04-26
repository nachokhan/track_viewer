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



def CalcSegmentDifficulty(segment):
    return None




def CalcTrackDifficulty(track):
    return None

