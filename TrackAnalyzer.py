""" 
Analyzer Module
This module manages all the needed functions to
make an analysis of teh Track
"""

from trackdatamodel.Track import Track
from trackdatamodel.Segment import Segment

def ExtractSegments_1(track):
    """[summary]

    Arguments:
        track {Track} -- The GPX/TCX/KML/etc track

    Returns:
        Track {Track} -- A new tracl with the new segments
    """

    track = Track()
    segments = []



    return track