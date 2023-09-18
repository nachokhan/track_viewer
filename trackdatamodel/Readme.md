# Python GPS Tracking Library Documentation

## Table of Contents

- [Summary](#summary)
- [GPSPoint](#gpspoint)
- [Segment](#segment)
- [Track](#track)

## Summary

The Track Data Model contains the classes needed to define a Track with its segments, its points, and whatever else we may need now and in the future. This module has almost no calculations and contains only real data.

But what does "real data" mean? When we measure elevation with a GPS device, we obtain a number. The same occurs with latitude, longitude, time, or even with effort if we have a specialized device that allows us to do so. We could even calculate the distance between two points, and it would still be considered "real data" because established methods determine how this can be done, without any inferences on our part.

So this data is "real" in the sense that we're not allowed to say "this is right" or "this is wrong." It's simply data that comes to us from the outside. Note: when I say "us," I mean, of course, that "we" are this software. Have you ever wondered what it's like to be software? Here's your opportunity ;)

Other types of values (or "data"), like difficulty (which WE assign), would not be included in this module. This is because it would introduce "pollution" into the "fresh" model with data of questionable accuracy. This follows the "I'm wrong; they're right" principle. I will assume that every piece of information that comes to me from the outside world, or any information that I can calculate using methods also originating from the outside world, is accurate. Why would I do this? Because it's not my fault who created it or how it was made. All I can do is accept it, not modify it. If I alter, for example, the conventional method for calculating the distance between two GPS points, I might be introducing an error due to potential flaws in my understanding. But if I use a standard method, then it's not my fault if it turns out to be incorrect. The correction would come from outside, and all I would need to do is replace it with the corrected version.


---

## GPSPoint

The `GPSPoint` class represents a point in a GPS coordinate system with latitude, longitude, and elevation.

### Methods:

1. **`__init__`**: Initializes a new `GPSPoint` object with latitude, longitude, and elevation.
2. **`distance_to`**: Computes the 3D Euclidean distance between the current point (`self`) and another point (`point`) passed as a parameter.
3. **`bearing_with`**: Calculates the bearing between the current point and another point. This method considers whether the longitude and latitude are increasing or decreasing between the two points to determine the bearing.
4. **`slope_with`**: Calculates the slope between the current point and another point. The slope is expressed in percentage.
5. **`_h_distance_to`**: Is a private auxiliary method that calculates the horizontal distance in meters between the current point and another point as if they were at the same elevation.

---

## Segment

The `Segment` class represents a segment composed of multiple GPS points (`GPSPoint` class).

### Methods:

1. **`__init__`**: Initializes the `Segment` object with an empty list of GPS points.
2. **`add_point` and `add_points`**: Add a point or a list of GPS points to the segment.
3. **`get_raw_slope` and `get_avg_slope`**: Calculate the total and average slope of the segment, respectively.
4. **`get_points`**: Returns the list of GPS points of the segment.
5. **`get_length`**: Calculates the total length of the segment in meters.
6. **`get_length_uphills`, `get_length_downhills`, `get_length_flats`**: Calculate the length of the segment that is uphill, downhill, and flat, respectively.
7. **`get_elevation_extremes`**: Returns the maximum and minimum elevations of the segment.
8. **`get_acc_elevation` and `get_acc_descent`**: Return the accumulated uphill and downhill elevation of the segment, respectively.
9. **`get_curves`**: Identifies and counts curves in the segment that have at least a minimum angle and point separation defined.
10. **`_getNextPoint`**: Auxiliary method to get the next nearby point to work with, used in `get_curves`.

---

## Track

The `Track` class represents a set of segments. Each segment is a sequence of GPS points with methods for calculating distances, slopes, and other metrics.

### Attributes:
1. **`__segments`**: List of `Segment` objects that make up the track.
2. **`__author`**: Author of the track.
3. **`__name`**: Name of the track.
4. **`__northest_point`, `__southest_point`, `__westest_point`, `__eastest_point`**: Extreme points in various directions.

### Methods:

1. **`add_segment`**: Adds a new segment to the list of segments.
2. **`add_segments`**: Adds a list of segments.
3. **`get_segments`**: Returns all the segments of the track.
4. **`get_length`**: Returns the total length of the track by summing the lengths of all segments.
5. **`set_name`**: Sets the name of the track.
6. **`get_name`**: Returns the name of the track.
7. **`set_author`**: Sets the author of the track.
8. **`get_author`**: Returns the author of the track.
9. **`get_boundaries`**: Returns a bounding box as a tuple (MinLon, MaxLon, MinLat, MaxLat).
10. **`get_extreme_point`**: Returns the extreme point in a given direction ('n', 's', 'w' or 'e').
11. **`__calc_extreme_points`**: Private method to calculate the extreme points of the track.
12. **`get_elevation_extremes`**: Returns the maximum and minimum elevations of the entire track.

The `Track` class allows for the management and calculation of various metrics and properties derived from the segments that make it up.