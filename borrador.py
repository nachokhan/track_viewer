from TrackReader import GPSVisualizerFileReader, Track
from TrackViewer import TrackViewer, TrackPlotInfo
from matplotlib import pylab as plt
import math

"""
A little information
https://docs.microsoft.com/en-us/azure/azure-maps/zoom-levels-and-tile-grid?tabs=csharp

"""

def OpenStreetMap():
    reader = GPSVisualizerFileReader()
    reader.ReadFile("./data/rocas2.txt")
    track = reader.GetTrack()

    maxlon = track.get_extreme_point("n")[1]
    minlon = track.get_extreme_point("s")[1]
    maxlat = track.get_extreme_point("w")[0]
    minlat = track.get_extreme_point("e")[0]
    formato = "png"

    osmmmmm2 = f'http://render.openstreetmap.org/cgi-bin/export?bbox={minlon},{minlat},{maxlon},{maxlat}&scale=29033&format=png'

    import webbrowser
    # http://render.openstreetmap.org/cgi-bin/export?bbox=-69.297326,-33.00407,-69.233426,-32.967264&scale=29033&format=png
    webbrowser.get('firefox').open_new_tab(osmmmmm2)


def getCenter(minlon, maxlon, minlat, maxlat, zoom):
    deltalat = abs (max(minlat, maxlat) - min(minlat, maxlat))
    deltalon = abs (max(minlon, maxlon) - min(minlon, maxlon))
    
    a = 0
    m = 6000

    width = deltalon * m
    height = deltalat * m

    return (width, height)

def Thunder():
    reader = GPSVisualizerFileReader()
    reader.ReadFile("./data/rincon1.txt")
    track = reader.GetTrack()
    tracki = TrackPlotInfo(track)
    tracki.ExtractTrackData()

    maxlon = track.get_extreme_point("n")[1]
    minlon = track.get_extreme_point("s")[1]
    maxlat = track.get_extreme_point("w")[0]
    minlat = track.get_extreme_point("e")[0]

    prop = (abs(maxlon-minlon)) / (abs(maxlat-minlat))
    
    zoom = 13
    w, h = getCenter(minlon, maxlon, minlat, maxlat, zoom)
    width = math.ceil( w )
    height = math.ceil ( h )
 
    lat = (maxlat+minlat)/2
    lon = (maxlon+minlon)/2  

    webUrl = f'https://tile.thunderforest.com/static/outdoors/{lon},{lat},{zoom}/{width}x{height}.png?apikey=aa0fb18001ef464bb82b04581e8baac6'

    im = plt.imread(webUrl)
    fig, ax = plt.subplots(figsize = (15,15))


    segments = track.get_segments()

    xs = []
    ys = []
    cs = []

    for s in segments:
        c = s.GetColor()
        x=[]
        y=[]
        for p in s.GetPoints():
            x.append(p.Longitude)
            y.append(p.Latitude)

        ax.plot(x, y, color = c, zorder=1)

    ax.scatter(lon, lat, color = "red", marker = '^')

    border = 0.0025

    ax.set_ylim(minlat-border, maxlat+border)
    ax.set_xlim(minlon-border, maxlon+border)

    plt.imshow(im, zorder=0, extent= (minlon, maxlon, minlat, maxlat), aspect='equal')
    plt.show()
