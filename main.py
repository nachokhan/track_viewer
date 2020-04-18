import matplotlib.pyplot as plt
import numpy as np

from TrackViewer import TrackFile

#x = np.linspace(0, 20, 100)  # Create a list of evenly-spaced numbers over the range
#plt.plot(x, np.sin(x))       # Plot the sine of each x point
#plt.show()                   # Display the plot

t = TrackFile()

t.ReadFile("./data/rincon1.txt")

print ("SEGMENTOS: " + str(len(t.ListOfSegments)))

distancia1 = 0
for segment in t.ListOfSegments:
    distancia1 += segment.GetDistance(False)

print ("NO ELEV Final = " + str(distancia1/1000) + " km")

distancia2 = 0
for segment in t.ListOfSegments:
    distancia2 += segment.GetDistance(True)

print ("SI ELEV Final = " + str(distancia2/1000) + " km")

print ("Diferencia es: " + str(abs(distancia1-distancia2)) + " metros")