from track_model.Segment import DrawableSegment
from track_viewer.NoTrackException import NoTrackException

class TrackPlotInfo:

    COLORS = ["blue", "green", "red", "blueviolet", "navy", "fuchsia", "orange"]

    def __init__(self, track = None, name = None):
        self.__track = track
        self.__resetValues()
        self.__name = name
        self.DataAlredyExtracted = False

    def __resetValues(self):
        self.__x_segs = []
        self.__y_segs = []
        self.__c_segs = []
        self.__all_x_data = []
        self.__all_y_data = []
        self.__intersections = []
        self.__lat_segs = []
        self.__lon_segs = []
        self.__curves = []

    def SetTrack(self, track):
        self.__track = track

    def GetName(self):
        return self.__name

    def DataAlreadyExtracted(self):
        return self.DataAlredyExtracted

    def GetSegmentsData(self):
        """ Returns a tuple with segment's array containing X[], Y[] and color for each segment """
        return (self.__x_segs, self.__y_segs, self.__c_segs)
    
    def GetAllPoints(self):
        return (self.__all_x_data, self.__all_y_data)

    def GetIntersectionsList(self):
        return self.__intersections

    def GetLatLonSegments(self):
        """ Returns a tuple with segment's array containing Lons[], Lats[] for each segment"""
        return (self.__lon_segs, self.__lat_segs)

    def GetCurves(self):
        return self.__curves

    def ExtractTrackData(self, automatic_colors = True):
        """ Given a Track, examine and extract all the needed information for plotting.
        If automatic_color = True it will assign automatic colors for each segment if they
        are not of the type DrawableSegments """

        if not self.__track:
            raise NoTrackException("Track is null", "There is no track assigned to the instance. Maybe you forgot to call the constructor with a track or to call SetTrack Method")

        self.__resetValues()

        segments = self.__track.GetSegments()       
            
        inters_x = []   # indexes indicating where each segmentatios is
        all_x = []      # all X data from first point to last one
        all_y = []
        x_segments = []     # Array with X values of each segment
        y_segments = []
        c_segments = []     # Array of color segments
        lat_segments = []   # Array of segment's latitudes
        lon_segments = []

        dist_acc = 0    #Accumulated distance over all segments

        next_color = 0  # To assign colors automatically, if it isn't a DrawableSegment

        for segment in segments:

            lats=[]     # segment latitude's points
            lons=[]     
            x = []      # segment distances (must be calculated from gps points)
            y = []      # segment elevations
           
            # Assign colors to each segemnt (default is blue)
            color = "blue"
            if segment is DrawableSegment:
                color = segment.GetColor()
            elif automatic_colors == True:
                color = TrackPlotInfo.COLORS[next_color]
                next_color += 1
                if next_color >= len(TrackPlotInfo.COLORS): next_color = 0

            curves = segment.GetCurves(min_degree = 90)[2]

            points = segment.GetPoints()
            cant_points = len(points)

            # calculate distance for points (0-->1), (1-->2) ... (N-1-->N)
            for i in range(cant_points-1):
                lats.append(points[i].Latitude)
                lons.append(points[i].Longitude)
                y.append(points[i].Elevation)                
                x.append(dist_acc)
                all_y.append(points[i].Elevation)
                all_x.append(dist_acc)
                dist_acc += points[i].DistanceTo(points[i+1])

                # Extract Curves with degree >= 90
                if i in curves:
                    self.__curves.append( ( all_x[-1], all_y[-1]))
            

            # last points are not contempled in first "for loop" we add them here        
            y.append(points[i+1].Elevation)
            x.append(dist_acc)
            all_y.append(points[i+1].Elevation)
            all_x.append(dist_acc)
            inters_x.append(len(all_x)-1)
            lats.append(points[i+1].Latitude)
            lons.append(points[i+1].Longitude)

            x_segments.append(x)
            y_segments.append(y)
            c_segments.append(color)
            lat_segments.append(lats)
            lon_segments.append(lons)
            

        # NOTE: In the whole method I worked with standalone variables instead of 
        # # instance-attributes because in this way it wouldbe easier to extract the 
        # method (e.g. to another class) without having to remove the "self." that would
        # be needed if I were using instance attributes.
        # I should now assign the variable's values to the instances attributes, of course:
        self.__x_segs = x_segments
        self.__y_segs = y_segments
        self.__c_segs = c_segments
        self.__all_x_data = all_x
        self.__all_y_data = all_y
        self.__intersections = inters_x
        self.__lat_segs = lat_segments
        self.__lon_segs = lon_segments
        self.DataAlredyExtracted = True
        
