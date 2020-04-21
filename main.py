import matplotlib.pyplot as plt
import numpy as np
import math

from TrackViewer import TrackFile

def PT(track):

    max_cols = 4
    intersections = len (track.GetSegments()) - 1
    max_rows = math.ceil (intersections / max_cols) + 1
    intersection_window = 50


    dist_acc = 0    #Accumulated distance over all segments

    x_min = 0.0
    x_max = 112100.0
    y_min = 9000
    y_max = 0

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
            if(dist_acc >= x_min and dist_acc <= x_max):
                y.append(points[i].Elevation)                
                x.append(dist_acc)
                all_y.append(points[i].Elevation)
                all_x.append(dist_acc)

            dist_acc += points[i].DistanceTo(points[i+1])
        
        # last points are not contempled in first "for loop" we add them here
        if(dist_acc >= x_min and dist_acc <= x_max):
            y.append(points[i+1].Elevation)
            x.append(dist_acc)
            all_y.append(points[i+1].Elevation)
            all_x.append(dist_acc)
            scat_x.append(dist_acc)
            scat_y.append(points[i+1].Elevation)
            inters_x.append(len(all_x)-1)

        if y:
            if max(y) > y_max : y_max = max(y)    
            if min(y) < y_min : y_min = min(y)

        main_ax.fill_between(x, y, color = color)
 
   
    ax = []

    for i in range(0, intersections):        
        row = math.floor(i/max_cols) + 1
        col = i % max_cols
        m_l = inters_x[i]-intersection_window     # middle to left
        m_r = inters_x[i]+intersection_window     # middle to right
        x_values = all_x[m_l:m_r]
        y_values = all_y[m_l:m_r]

        ax_ = fig.add_subplot(grid[row, col], ylim = 1000)
        ax_.plot(x_values, y_values)        
        ax_.set_ylim( min(y_values), max(y_values))
        ax_.set_xlim( min(x_values), max(x_values))
        ax_.axvline(all_x[inters_x[i]], color = "red")
        ax.append(ax_)
        

    main_ax.set_ylim(y_min-10, y_max+20)
    main_ax.scatter(scat_x, scat_y, color = "black", edgecolor="white", marker = '^')

    plt.show()


def Hacer(fileName):
    t = TrackFile()
    t.ReadFile(fileName)
    track = t.GetTrack()
    PT(track)


Hacer("./data/VIEW_04_05_400.txt")
