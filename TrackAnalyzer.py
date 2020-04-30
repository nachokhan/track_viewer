""" 
Analyzer Module
This module manages all the needed functions to
make an analysis of teh Track
"""

from trackdatamodel.Track import Track
from trackdatamodel.Segment import Segment

def sign(x) :
    """ Returns the sign of X. Zero is considered negative because
    ir being used for detect Up & Downhills. And no slope means for
    us a downhill """
    if x > 0 : return 1
    if x < 0 : return -1
    if x == 0: return -1


def ExtractSegments_1(track):
    """Make a new track with one or more segments. Segments are
    being divided according different algoritmhs. At the time 
    of writing, the best algorithm is still not determined.

    Arguments:
        track {Track} -- The GPX/TCX/KML/etc track

    Returns:
        Track {Track} -- A new tracl with the new segments
    """

    newTrack = Track()          # New track to be returned
    segments = []               # List with the new segments
    changePositions = []        # Positions where the changes UP/DOWN take place

    uniqueSegment = track.GetSegments()[0]

    changePositions = GetSlopeSignChangesPosition(uniqueSegment)

    # TO CONTINUE

    return newTrack


def GetSlopeSignChangesPosition(segment):
    """Returns a list of points indicating the indexes of the points
    where there is a slope sign change (up- or downhill's chage)   
    """
    positions = []       # Positions of slope sign change

    points = segment.GetPoints()
    q_points = len(points)

    for i in range(q_points - 2):
        p1 = points[i]
        p2 = points[i+1]
        p3 = points[i+2]

        sl_1 = sign(p1.SlopeWith(p2))
        sl_2 = sign(p2.SlopeWith(p3))

        if sl_1 != sl_2:
            positions.append(i+1)
    
    return positions


        



