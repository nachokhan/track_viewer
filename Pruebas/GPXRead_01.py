from TrackReader import GPXFileReader

def main():

    fileName = "./data/gpx/larry.gpx"

    reader = GPXFileReader(fileName)

    track = reader.Read()

    print (track.GetLength())
    print (track.GetBoundaries())

