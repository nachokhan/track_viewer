""" 
TrackViewer Module
This module manages all the needed functions to plot the
Track info saved in the data files readen by TrackReader

"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import TrackReader

class TrackPlotInfo:

    def __init__(self, track = None):
        self.__track = track
        self.__x_segs = []
        self.__y_segs = []
        self.__c_segs = []
        self.__all_x_data = []
        self.__all_y_data = []
        self.__intersections = []
        self.__lat_segs = []
        self.__lon_segs = []

    def SetTrack(self, track):
        self.__track = track

    def GetSegmentsData(self):
        return (self.__x_segs, self.__y_segs, self.__c_segs)
    
    def GetAllPoints(self):
        return (self.__all_x_data, self.__all_y_data)

    def GetIntersectionsList(self):
        return self.__intersections

    def GetLatLonSegments(self):
        """ Returns a tuple with segment's array containing Lons[], Lats[] for each segment"""
        return (self.__lon_segs, self.__lat_segs)

    def ExtractTrackData(self):
        """ Given a Track, examine and extract all the needed information for plotting """

        if not self.__track:
            raise NoTrackException("Track is null", "There is no track assigned to the instance. Maybe you forgot to call the constructor with a track or to call SetTrack Method")

        segments = self.__track.GetSegments()

        dist_acc = 0    #Accumulated distance over all segments
            
        inters_x = []   # indexes indicating where each segmentatios is
        all_x = []      # all X data from first point to last one
        all_y = []   

        x_segments = []     # Array with X values of each segment
        y_segments = []
        c_segments = []     # Array of color segments

        lat_segments = []   # Array of segment's latitudes
        lon_segments = []

        for segment in segments:

            lats=[]     # segment latitude's points
            lons=[]     
            x = []      # segment distances (must be calculated from gps points)
            y = []      # segment elevations
            color = segment.GetColor()
            points = segment.GetPoints()
            cant_points = len(points)-1

            # calculate distance for points (0-->1), (1-->2) ... (N-1-->N)
            for i in range(cant_points):
                lats.append(points[i].Latitude)
                lons.append(points[i].Longitude)
                y.append(points[i].Elevation)                
                x.append(dist_acc)
                all_y.append(points[i].Elevation)
                all_x.append(dist_acc)
                dist_acc += points[i].DistanceTo(points[i+1])
            
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
        


class TrackViewer:


    def BuildPlot(self, plotInfo, max_cols = 0, intersection_window = 50):
        """Given a TrackPlotInfo object, build the XXXXX Information Page."""
        x_segments,  y_segments, c_segments = plotInfo.GetSegmentsData()
        inters_x = plotInfo.GetIntersectionsList()
        all_x , all_y = plotInfo.GetAllPoints()

        intersections = len(inters_x) - 1

        if max_cols == 0:
            if intersections <= 5:
                max_cols = intersections
            else:
                max_cols = 4

        # How many rows do we need to show N intersections
        max_rows = math.ceil (intersections / max_cols) + 1

        y_max = max(all_y)
        y_min = min(all_y)

        # Initiliaze graphics
        fig = plt.figure(figsize=(25, 15))
        fig.suptitle("Elevation Map Analysis")
        grid = plt.GridSpec(max_rows, max_cols, wspace=0.2, hspace=0.8)    

        # DRAW MAIN ELEVATION MAP
        main_ax = fig.add_subplot(grid[0, 0:])    # first row reserved for total elevation

        for i in range (0, len(x_segments)):        
            main_ax.fill_between(x_segments[i], y_segments[i], color = c_segments[i], alpha = 0.5)  # Should Move this to GRAPH PART

        main_ax.set_title("Elevation Map")
        main_ax.set_xlabel("Distance (Km)")
        main_ax.set_ylabel("Elevation(m)")
        main_ax.set_ylim(y_min-10, y_max+60)
        # Scale m into Km and add the last X value as a text (to avoid possible overlapping)
        x_scale = 1/1000
        ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*x_scale))
        main_ax.xaxis.set_major_formatter(ticks_x)
        main_ax.annotate(str( round(all_x[-1]*x_scale,2)), (all_x[-1], all_y[-1]))
        
        
        # SCATTER POINTS        
        for i in inters_x:
            int_x = all_x[i]
            int_y = all_y[i]
            main_ax.scatter(int_x, int_y, color = "black", edgecolor="white", marker = '^')            


        # DRAW EACH INTERSECTION
        ax = []
        for i in range(0, intersections):        
            row = math.floor(i/max_cols) + 1
            col = i % max_cols

            # Select the intervals & values around the segment's intersection
            m_l = inters_x[i]-intersection_window       # middle to left
            m_r = inters_x[i]+intersection_window       # middle to right
            x_values_1 = all_x[m_l:inters_x[i]+1]
            y_values_1 = all_y[m_l:inters_x[i]+1]
            x_values_2 = all_x[inters_x[i]:m_r]
            y_values_2 = all_y[inters_x[i]:m_r]
            # Calculate min and max
            min_x = min ( min(x_values_1), min (x_values_2))
            min_y = min ( min(y_values_1), min (y_values_2))
            max_x = max ( max(x_values_1), max (x_values_2))
            max_y = max ( max(y_values_1), max (y_values_2))
            # Plot everything
            ax_ = fig.add_subplot(grid[row, col], ylim = 1000)
            ax_.fill_between(x_values_1, y_values_1, color = c_segments[i], alpha=0.2)
            ax_.fill_between(x_values_2, y_values_2, color = c_segments[i+1], alpha=0.2)
            ax_.set_ylim( min_y, max_y)
            ax_.set_xlim( min_x, max_x)
            ax_.axvline(all_x[inters_x[i]], color = "red")
            txt_x = str(round(all_x[inters_x[i]]/1000, 2))      # X coord (for the title) rounded in Km
            txt = "[#" + str(i+1) + "] (" + txt_x + " km)"      # ALL the text
            ax_.set_title(txt)
            ax.append(ax_)
        
        return plt


    def ShowPlot(self, plot):
        """ Shows the Plot in the Screen """
        plot.show()

    def SavePlotAs(self, plot, fileName, transparent = True):
        """Saves a plot into a PNG file """
        plot.savefig(fileName)


class NoTrackException(Exception):
    """ Exceptio raised when trying to work with a null track """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
