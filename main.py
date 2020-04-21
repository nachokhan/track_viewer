import matplotlib.pyplot as plt
import numpy as np
import math

from TrackViewer import TrackFile

def PT(track, max_cols = 4, intersection_window = 50):

    intersections = len (track.GetSegments()) - 1
    max_rows = math.ceil (intersections / max_cols) + 1

    dist_acc = 0    #Accumulated distance over all segments

    segments = track.GetSegments()

    scat_x = [0]
    scat_y = [segments[0].GetPoints()[0].Elevation]
    inters_x = []

    all_x = []
    all_y = []

    # Initiliaze graphics
    fig = plt.figure(figsize=(25, 15))
    grid = plt.GridSpec(max_rows, max_cols, wspace=0.2, hspace=0.2)
    main_ax = fig.add_subplot(grid[0, 0:])    # first row reserved for total elevation


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
        scat_x.append(dist_acc)
        scat_y.append(points[i+1].Elevation)
        inters_x.append(len(all_x)-1)            

        main_ax.fill_between(x, y, color = color, alpha = 0.5)
 
   
    ax = []

    for i in range(0, intersections):        
        row = math.floor(i/max_cols) + 1
        col = i % max_cols

        #Select the intervals & values around the segment's intersection
        m_l = inters_x[i]-intersection_window     # middle to left
        m_r = inters_x[i]+intersection_window     # middle to right
        x_values_1 = all_x[m_l:inters_x[i]+1]
        y_values_1 = all_y[m_l:inters_x[i]+1]
        x_values_2 = all_x[inters_x[i]:m_r]
        y_values_2 = all_y[inters_x[i]:m_r]
        #Calculate min and max
        min_x = min ( min(x_values_1), min (x_values_2))
        min_y = min ( min(y_values_1), min (y_values_2))
        max_x = max ( max(x_values_1), max (x_values_2))
        max_y = max ( max(y_values_1), max (y_values_2))

        ax_ = fig.add_subplot(grid[row, col], ylim = 1000)
        ax_.fill_between(x_values_1, y_values_1, color = segments[i].GetColor(), alpha=0.2)
        ax_.fill_between(x_values_2, y_values_2, color = segments[i+1].GetColor(), alpha=0.2)
        ax_.set_ylim( min_y, max_y)
        ax_.set_xlim( min_x, max_x)
        ax_.axvline(all_x[inters_x[i]], color = "red")
        ax.append(ax_)
        

        y_max = max(all_y)
        y_min = min(all_y)

    main_ax.set_ylim(y_min-10, y_max+20)
    main_ax.scatter(scat_x, scat_y, color = "black", edgecolor="white", marker = '^')

    plt.show()


def Hacer(fileName):
    t = TrackFile()
    t.ReadFile(fileName)
    track = t.GetTrack()
    PT(track, max_cols=5)


Hacer("./data/VIEW_04_05_400.txt")
