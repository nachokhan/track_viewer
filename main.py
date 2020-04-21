import matplotlib.pyplot as plt
import numpy as np
import math
import random

from TrackViewer import TrackFile

def PT(track, max_cols = 0, intersection_window = 50):

    segments = track.GetSegments()

    intersections = len(segments) - 1

    if max_cols == 0:
        if intersections <= 5:
            max_cols = intersections
        else:
            max_cols = 4

    # How many rows do we need to show N intersections
    max_rows = math.ceil (intersections / max_cols) + 1

    dist_acc = 0    #Accumulated distance over all segments
        
    inters_x = []   # indexes where the segmentatios are
    all_x = []      # all X data from first point to last one
    all_y = []   

    x_segments = []     # Array with X values of each segment
    y_segments = []
    c_segments = []     # Array of color segments

    for segment in segments:

        x = []  # x must be calculated from gps points
        y = []
        color = segment.GetColor()
        points = segment.GetPoints()
        cant_points = len(points)-1

        # calculate distance for points (0-->1), (1-->2) ... (N-1-->N)
        for i in range(cant_points):         
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

        x_segments.append(x)
        y_segments.append(y)
        c_segments.append(color)
    
    y_max = max(all_y)
    y_min = min(all_y)


    #########################################################################################################################
    # GRAPHICATION PART

    # Initiliaze graphics
    fig = plt.figure(figsize=(25, 15))
    fig.suptitle("Elevation Map Analysis")
    grid = plt.GridSpec(max_rows, max_cols, wspace=0.2, hspace=0.3)    

    # DRAW MAIN ELEVATION MAP
    main_ax = fig.add_subplot(grid[0, 0:])    # first row reserved for total elevation
    for i in range (0, len(x_segments)):        
        main_ax.fill_between(x_segments[i], y_segments[i], color = c_segments[i], alpha = 0.5)  # Should Move this to GRAPH PART

    main_ax.set_title("Elevation Map")
    main_ax.set_xlabel("Distance (m)")
    main_ax.set_ylabel("Elevation(m)")
    main_ax.set_ylim(y_min-10, y_max+20)

    # SCATTER PART
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
        ax_.fill_between(x_values_1, y_values_1, color = segments[i].GetColor(), alpha=0.2)
        ax_.fill_between(x_values_2, y_values_2, color = segments[i+1].GetColor(), alpha=0.2)
        ax_.set_ylim( min_y, max_y)
        ax_.set_xlim( min_x, max_x)
        ax_.axvline(all_x[inters_x[i]], color = "red")
        ax_.set_title("Intersection #" + str(i+1))
        ax.append(ax_)
    
    plt.show()


def Hacer(fileName):
    t = TrackFile()
    t.ReadFile(fileName)
    track = t.GetTrack()
    PT(track)


Hacer("./data/rincon1.txt")
