#import matplotlib.pyplot as plt
#import numpy as np
import timeit
from datetime import datetime

from TrackViewer import TrackFile

#x = np.linspace(0, 20, 100)  # Create a list of evenly-spaced numbers over the range
#plt.plot(x, np.sin(x))       # Plot the sine of each x point
#plt.show()                   # Display the plot

def Hacer(lista):   
    distancia = 0
    t1 = datetime.now()

    for segment in lista:
        distancia += segment.GetDistance()

    t2 = datetime.now()
    time = abs(t2-t1)

    return (time, distancia)


t = TrackFile()
t.ReadFile("./data/rincon1.txt")

time, distancia = Hacer(t.__listOfSegments)
print ("OWN\tFinal = " + str(distancia/1000) + " km\tTIME: " + str(time.microseconds) + " us")