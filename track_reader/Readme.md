# Track Reader Module Documentation

## Index

1. [Summary](#summary)
2. [GPSVisualizerFileReader](#gpsvisualizerfilereader)
    - [Attributes](#attributes)
    - [Methods](#methods)
3. [GPXFileReader](#gpxfilereader)
    - [Attributes](#attributes-1)
    - [Methods](#methods-1)

## Summary

This document provides a detailed explanation of two classes: `GPSVisualizerFileReader` and `GPXFileReader`. Both classes are designed for reading GPS data from different file formats and storing them in a structured form. The `GPSVisualizerFileReader` class reads from text files, while `GPXFileReader` reads GPX files (an XML-based format). These classes facilitate the manipulation and visualization of GPS data by converting it into `Track` and `Segment` objects.

## GPSVisualizerFileReader

The `GPSVisualizerFileReader` class is responsible for reading and parsing text files that contain information about GPS tracks and segments. It uses other classes like `GPSPoint`, `DrawableSegment`, and `Track` to model the data.
Info about his format under: https://www.gpsvisualizer.com/tutorials/tracks.html

### Attributes

- `self.__segment`: A `DrawableSegment` object to store the current segment being read.
- `self.__track`: A `Track` object to store all the segments read from the file.

### Methods

#### `__init__`
Initializes the object with a new `DrawableSegment` and `Track` instance.

#### `read_file(fileName)`
Reads a text file line by line and processes each line to build the `Track` object. 

#### `analyze_line(line)`
Processes each line to either add a point to the current segment or start a new segment.

#### `get_values_from_line(line)`
Parses a line to get the GPS point, name, and color.

#### `get_track()`
Returns the `Track` object containing all the segments.

## GPXFileReader

The `GPXFileReader` class reads GPX (GPS Exchange Format) files and extracts information to create a `Track` object. It utilizes the `BeautifulSoup` library for XML parsing.

### Attributes

- `self.__file`: The filename of the GPX file to read.

### Methods

#### `__init__(self, filename)`
Initializes the object with the given filename.

#### `set_file_name(self, filename)`
Sets the filename for the GPX file.

#### `read()`
Reads the GPX file and constructs a `Track` object containing all the parsed information.

#### `get_XML_nodes(self, xml, lista, i = 0)`
Navigates through the XML hierarchy to find and return a list of nodes.

#### `get_XML_node_text(self, xml, lista, i = 0)`
Navigates through the XML hierarchy to find and return the text content of a node.