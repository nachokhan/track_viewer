""" 
TrackViewer Class
This class manages all the needed functions to plot the
Track info saved in the data files readen by TrackReader
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math


class TrackViewer:   

    def BuildPlot(self, plotInfo, max_cols = 0, intersection_window = 50, show_curves=True):
        """Given a TrackPlotInfo object, build the XXXXX Information Page."""

        if not plotInfo.DataAlreadyExtracted():
            raise Exception("You must first call plotInfo.ExtractData() !!!")

        x_segments,  y_segments, c_segments = plotInfo.GetSegmentsData()
        inters_x = plotInfo.GetIntersectionsList()
        all_x , all_y = plotInfo.GetAllPoints()
        title = plotInfo.GetName()
        curves = plotInfo.GetCurves()

        intersections = len(inters_x) - 1

        if max_cols == 0:
            if intersections == 0:
                max_cols = 1
            elif intersections <= 5:
                max_cols = intersections
            else:
                max_cols = 4

        # How many rows do we need to show N intersections
        max_rows = math.ceil (intersections / max_cols) + 1

        y_max = max(all_y)
        y_min = min(all_y)

        # Initiliaze graphics
        fig = plt.figure(figsize=(25, 15))
        fig.suptitle(title, size="xx-large")
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


        # SCATTER CURVES        
        for c in curves:
            int_x = c[0]
            int_y = c[1]
            main_ax.scatter(int_x, int_y, color = "red", edgecolor="white", marker = 'd')


        # DRAW EACH INTERSECTION
        ax = []
        for i in range(0, intersections):        
            row = math.floor(i/max_cols) + 1
            col = i % max_cols

            # Select the intervals & values around the segment's intersection
            inters_p = inters_x[i]                  # current distance of intersection
            if inters_p < intersection_window:
                m_l = 0                                 # zero to middle
            else:
                m_l = inters_p-intersection_window      # middle to left 
            m_r = inters_p+intersection_window          # middle to right

            x_values_1 = all_x[m_l:inters_p+1]
            y_values_1 = all_y[m_l:inters_p+1]
            x_values_2 = all_x[inters_p:m_r]
            y_values_2 = all_y[inters_p:m_r]
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
            ax_.axvline(all_x[inters_p], color = "red")
            txt_x = str(round(all_x[inters_p]/1000, 2))      # X coord (for the title) rounded in Km
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

    def ClearPlot(self, plot):
        plot.close()
        del plot
