from track_reader.GPXFileReader import GPXFileReader


def main():

    fileName = "./data/gpx/larry.gpx"

    reader = GPXFileReader(fileName)

    track = reader.read()

    print (track.get_length())
    print (track.get_boundaries())

