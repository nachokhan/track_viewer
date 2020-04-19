#import matplotlib.pyplot as plt
#import numpy as np
import timeit
from datetime import datetime

from TrackViewer import TrackFile

#x = np.linspace(0, 20, 100)  # Create a list of evenly-spaced numbers over the range
#plt.plot(x, np.sin(x))       # Plot the sine of each x point
#plt.show()                   # Display the plot

def Hacer(lista, metodo):   
    distancia = 0
    t1 = datetime.now()

    for segment in lista:
        distancia += segment.GetDistance(metodo, False)

    t2 = datetime.now()
    time = abs(t2-t1)

    return (time, distancia)


t = TrackFile()
t.ReadFile("./data/rincon1.txt")

time, distancia = Hacer(t.ListOfSegments, "own")
print ("OWN\tFinal = " + str(distancia/1000) + " km\tTIME: " + str(time.microseconds) + " us")

time, distancia = Hacer(t.ListOfSegments, "geodesic")
print ("GEODE\tFinal = " + str(distancia/1000) + " km\tTIME: " + str(time.microseconds) + " us")

time, distancia = Hacer(t.ListOfSegments, "great_circle")
print ("GREAT\tFinal = " + str(distancia/1000) + " km\tTIME: " + str(time.microseconds) + " us")

time, distancia = Hacer(t.ListOfSegments, "geopy")
print ("GEOPY\tFinal = " + str(distancia/1000) + " km\tTIME: " + str(time.microseconds) + " us")
