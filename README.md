quakefeeds
==========

Python 3 tools for handling USGS earthquake data feeds.

The ```quakefeeds``` module provides a simple way of retrieving earthquake
data for a given minimum severity level and time period from a web service
run by the USGS Earthquake Hazards Program (http://earthquake.usgs.gov).
It also provides the means to generate a simple Google map showing quake
locations and other details such as magnitude.

The data feeds and a description of their GeoJSON format are available at
http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php.
