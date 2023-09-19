from track_model.Track import Track
from track_model.Segment import Segment
from track_model.GPSPoint import GPSPoint
from bs4 import BeautifulSoup


class GPXFileReader:

    def __init__(self, filename):
        self.__file = filename

    def set_file_name (self, filename):
        self.__filen = filename

    def read(self):
        
        # Nodes hierarchy in GPXFiles fro each content
        GPX_STR_TRACK_NAME = "gpx,metadata,name".split(",")
        GPX_STR_AUTHOR_NAME = "gpx,metadata,author,name".split(",")
        GPX_STR_TRACK_POINTS = "gpx,trk,trkseg,trkpt".split(",")

        newTrack = Track()

        with open(self.__file) as fp:
            root = BeautifulSoup(fp, features="lxml")

        try:            
            trackName = self.get_XML_node_text(root, GPX_STR_TRACK_NAME) or 'noname'
            authorName = self.get_XML_node_text(root, GPX_STR_AUTHOR_NAME) or 'noname'
            trackPoints =  self.get_XML_nodes(root, GPX_STR_TRACK_POINTS)

            newTrack = Track()
            newTrack.set_name(trackName)
            newTrack.set_author(authorName)

            segment = Segment()

            for pts in trackPoints:
                lat = float(pts["lat"])
                lon = float(pts["lon"]) 
                elev = float(self.get_XML_node_text(pts, ["ele"]))
                gpsPoint = GPSPoint(lat, lon, elev)

                segment.add_point(gpsPoint)

            newTrack.add_segment(segment)
        
        except TypeError as err:
            print(f"Error parsing GPX File: {self.__file} . Error {err}")

        return newTrack


    def get_XML_nodes(self, xml, lista, i = 0):
        node = None
        new_xml = xml.find(lista[i])
        if new_xml:
            if i < len(lista) - 2:
                node = self.get_XML_nodes(new_xml, lista, i+1)
            else:
                ulitmo = lista[-1]
                node = new_xml.findAll(ulitmo)
        return node


    def get_XML_node_text(self, xml, lista, i = 0):
        texto = None
        new_xml = xml.find(lista[i])
        if new_xml:
            if i < len(lista) - 1:
                texto = self.get_XML_node_text(new_xml, lista, i+1)
            else:
                texto = new_xml.text
        return texto
