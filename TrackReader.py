""" 
TrackReader Module
This module manages all the needed functions to read the
Track info saved in the data files.

This data files are TXT in the form indicated by the
GPS Visualizer (https://www.gpsvisualizer.com/)

Info about the format is available under:
https://www.gpsvisualizer.com/tutorials/tracks.html
"""

from trackdatamodel.GPSPoint import GPSPoint
from trackdatamodel.Segment import Segment
from trackdatamodel.Segment import DrawableSegment
from trackdatamodel.Track import Track

from xml.dom import minidom
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys



class GPXFileReader:

    def __init__(self, filename):
        self.__file = filename

    def SetFileName (self, filename):
        self.__filen = filename

    def Read(self):
        
        # Nodes hierarchy in GPXFiles fro each content
        GPX_STR_TRACK_NAME = "gpx,metadata,name".split(",")
        GPX_STR_AUTHOR_NAME = "gpx,metadata,author,name".split(",")
        GPX_STR_TRACK_POINTS = "gpx,trk,trkseg,trkpt".split(",")

        newTrack = Track()

        with open(self.__file) as fp:
            root = BeautifulSoup(fp)

        try:            
            trackName = getXMLNodeText(root, GPX_STR_TRACK_NAME)
            authorName = getXMLNodeText(root, GPX_STR_AUTHOR_NAME)
            trackPoints =  getXMLNodes(root, GPX_STR_TRACK_POINTS)

            newTrack = Track()
            newTrack.SetName(trackName)
            newTrack.SetAuthor(authorName)

            segment = Segment()

            for pts in trackPoints:
                lat = float(pts["lat"])
                lon = float(pts["lon"]) 
                elev = float(getXMLNodeText(pts, ["ele"]))
                gpsPoint = GPSPoint(lat, lon, elev)

                segment.AddPoint(gpsPoint)

            newTrack.AddSegment(segment)
        
        except TypeError as err:
            print("Error parsing GPX File: {0}".format(self.__file))

        return newTrack

def getXMLNodes(xml, lista, i = 0):
    node = None
    new_xml = xml.find(lista[i])
    if new_xml:
        if i < len(lista) - 2:
            node = getXMLNodes(new_xml, lista, i+1)
        else:
            ulitmo = lista[-1]
            node = new_xml.findAll(ulitmo)

    return node
    
def getXMLNodeText(xml, lista, i = 0):
    texto = None
    new_xml = xml.find(lista[i])
    if new_xml:
        if i < len(lista) - 1:
            texto = getXMLNodeText(new_xml, lista, i+1)
        else:
            texto = new_xml.text
    
    return texto


#########
# TrackFileReader Class represents an object that reads a text file 
# with gps segments and saves this data as a List Of Segments.
#########
class GPSVisualizerFileReader:

    def __init__ (self):
        self.__segment = DrawableSegment()
        self.__track = Track()

    # Reads a text File by analizing and saving all the segments in the file    
    def ReadFile(self, fileName):
        """ Reads a TXT File with Segments and stores them """
        f = open(fileName, "r")
        lines = f.readlines()
        for line in lines:
            self.analyzeLine(line)
        f.close()

    # Analyzes a line in order to extract a gps point or a "start of segment"
    def analyzeLine(self, line):
        first_element = line.split(",")[0]

        if first_element == 'T':
            point, name, color = self.GetValuesFromLine(line)
            self.__segment.AddPoint(point)
            self.__segment.SetColor(color)
            self.__segment.SetName(name)

        elif first_element == 'type' :
            self.__segment = DrawableSegment()
            self.__track.AddSegment(self.__segment)           
        
    # Read the lines and obtain the values
    def GetValuesFromLine(self, line):
        values = line.split(",")
        p = GPSPoint(values[1],values[2],values[3])
        name = values[4]
        color = values[5][:-1]
        return (p, name, color)

    # Returns all the segments in the file.
    def GetTrack(self):
        """ Returns the Track readed fro mthe file """
        return self.__track


