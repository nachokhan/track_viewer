from TrackReader import GPXFileReader

def main(fileName):

    reader = GPXFileReader(fileName)

    reader.Read()

