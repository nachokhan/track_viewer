""" 
Analyzer Module
This module manages all the needed functions to
make an analysis of teh Track
"""

from track_model.Track import Track
from track_model.Segment import Segment
from track_model.GPSPoint import GPSPoint

def sign(x) :
    """ Returns the sign of X. Zero is considered negative because
    ir being used for detect Up & Downhills. And no slope means for
    us a downhill """
    if x > 0 : return 1
    if x < 0 : return -1
    if x == 0: return -1


def segment_from_change_position(segment, segmentations):

    points = segment.GetPoints()   
    segments = []    

    #segmentations.insert(0, 0)
    segmentations.append(len(points))

    prev = 0
    for actual in segmentations:
        pts = points[prev:actual]        
        seg = Segment()
        seg.add_points (pts)
        segments.append(seg)
        prev = actual    


    return segments

def extract_segment_1(track, method = 0):
    """
    Make a new track with one or more segments. Segments are
    being divided according different algoritmhs. At the time 
    of writing, the best algorithm is still not determined.

    Arguments:
        track {Track} -- The GPX/TCX/KML/etc track

    Returns:
        Track {Track} -- A new tracl with the new segments
    """

    newTrack = Track()          # New track to be returned
    newSegments = []            # List with the new segments
    changePositions = []        # Positions where the changes UP/DOWN take place

    uniqueSegment = track.GetSegments()[0]   

    remove_short_distances(uniqueSegment, 4)
    uniqueSegment2 =  normalize_elevation(uniqueSegment)

    #graficar_dos_x(uniqueSegment, uniqueSegment2)

    changePositions = get_slope_sign_change_position(uniqueSegment2)
    changePositions = segment_by_height(uniqueSegment2, changePositions)

    newSegments = segment_from_change_position(uniqueSegment2, changePositions)
    newTrack.add_segments(newSegments)
    return newTrack

def normalize_elevation(segment):

    import copy
    points = segment.GetPoints()
    newPoints = copy.deepcopy(points)

    win = 9
    offset = int((win-1)/2)
    q_points = len(newPoints)

    for i in range (offset, q_points - offset):
        aver = 0
        for j in range(-offset, offset+1):
            aver += points[i+j].Elevation
        newPoints[i].Elevation = aver / win
    
    for i in range(0, offset+2):
        aver = 0
        for j in range(0, win):
            aver += points[i+j].Elevation
        newPoints[i].Elevation = aver / win

    for i in range(q_points-offset-2, q_points):
        aver = 0
        for j in range(0, win):
            aver += points[i-j].Elevation
        newPoints[i].Elevation = aver / win        


    newSegment = Segment()
    newSegment.add_points(newPoints)

    return newSegment

def remove_short_distances(segment, min_distance = 4):
    """ 
    Exactly that 
    """

    points = segment.GetPoints().copy()
    pointsToDelete = []

    for i in range(len(points)-1):
        
        p1 = points[i]
        p2 = points[i+1]
        dist = p1.DistanceTo(p2)

        if dist <= min_distance:
            pointsToDelete.append(i)

    pointsToDelete.reverse()

    for i in pointsToDelete:
        del points[i]

    newSegment = Segment()
    newSegment.add_points(points)

    return newSegment
    
def segment_by_height(segment, segmentations):
    """ 
    Makes a new segmentation based on the heights difference 
    """
    
    mh,Mh = segment.GetElevationExtremes()

    dht = Mh-mh
    min_h = dht * 0.015
    if min_h < 15:
        min_h = 15
    
    points = segment.GetPoints()
    newSegmentations = []
    l0 = 0
    
    for i in range(1, len(segmentations)):
        l1 = segmentations[i-1]
        l2 = segmentations[i]

        p_seg = Segment()
        p_seg.add_points (points[l0:l1])
        p_delta_h = p_seg.get_acc_elevation() + p_seg.get_acc_descent()
        p_delta_h_p = max (p_seg.get_acc_elevation(), abs(p_seg.get_acc_descent()))
        p_delta_h = p_delta_h_p * sign(p_delta_h)

        seg = Segment()
        seg.add_points (points[l1:l2])
        delta_h = seg.get_acc_elevation() + seg.get_acc_descent()
       
        factor = abs(p_delta_h * ((-5.9459*10**(-6))+0.19891))

        if sign(delta_h) != sign(p_delta_h):
            #if abs(delta_h) > 0.1 * abs(p_delta_h) and abs(delta_h) > min_h:
            if abs(delta_h) > min_h:
                newSegmentations.append(l1)
                l0 = l1
        
    return newSegmentations


def get_slope_sign_change_position(segment):
    """
    Returns a list of points indicating the indexes of the points
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


def graficar_dos_x(s1, s2):
    from matplotlib import pyplot as plt
    fig = plt.figure(figsize=(55, 25))
    fig.suptitle("slopes", size="xx-large")
    grid = plt.GridSpec(1, 1, wspace=0.5, hspace=0.5)
    ax1 = fig.add_subplot(grid[0, 0])

    if s1 is Segment and s2 is Segment:
        p1 = s1.GetPoints()
        p2 = s2.GetPoints()
    else:
        p1 = s1
        p2 = s2
    
    x = []
    y1 = []
    y2 = []

    if p1[0] is GPSPoint:
        for i in range( len(p1)):
            x.append(i)
            y1.append(p1[i].Elevation)
            y2.append(p2[i].Elevation)
    else:
        x = range(0, len(p1))
        y1 = p1
        y2 = p2

    l1 = 0
    l2 = len(p1)
    ax1.plot(x[l1:l2], y1[l1:l2], color = "blue")
    ax1.plot(x[l1:l2], y2[l1:l2], color = "red")
    plt.show()
    del plt