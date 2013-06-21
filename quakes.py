"""
Tools for handling USGS earthquake data feeds.

This module provides a simple way of retrieving earthquake data
for a given minimum severity level and time period from a web
service run by the USGS Earthquake Hazards Program.  It also
provides the means to generate a Google map showing earthquake
locations and other details.

Feeds and a description of their format are available at
http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
"""

from string import Template
import urllib.request
import json


URL = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{}_{}.geojson"

ALLOWED_LEVELS = ("significant", "4.5", "2.5", "1.0", "all")
ALLOWED_PERIODS = ("hour", "day", "week", "month")

MAP_TEMPLATE = Template("""\
<!DOCTYPE html>
<html>
<head>
<script type="text/javascript" src="http://www.google.com/jsapi"></script>
<script type="text/javascript">
google.load("visualization", "1", {packages:["map"]});
google.setOnLoadCallback(drawMap);
function drawMap() {
var data = new google.visualization.arrayToDataTable([
['Lat', 'Lon', 'Details'],
$data
]);
var map = new google.visualization.Map(document.getElementById('map'));
map.draw(data, {showTip: true});
}
</script>
<title>Earthquake Map</title>
</head>
<body>
<div id="map" style="width:800px; height:500px"></div>
</body>
</html>""")


def get_data(level, period):
    """Retrieves earthquake data for the given severity level and period.

       ValueError is raised if either severity level or period are not
       supported by the USGS data feeds.  Data follow the GeoJSON format
       (see http://www.geojson.org) and are returned as a dictionary.
    """
    if level not in ALLOWED_LEVELS:
        raise ValueError("invalid severity level")
    if period not in ALLOWED_PERIODS:
        raise ValueError("invalid period")

    feed_url = URL.format(level, period)
    feed = urllib.request.urlopen(feed_url)

    response = feed.read().decode("utf-8")
    data = json.loads(response)

    return data


def generate_map(data, filename=None):
    """Plots earthquakes from the given GeoJSON dataset on a Google map.

       The location of each earthquake will be marked.  Clicking on a
       marker will display an info bubble containing the magnitude of the
       quake and a description of its location.

       The HTML for the map is returned as a string.  If a filename is
       specified, the HTML will also be written to a file with that name.
    """

    map_data = []
    for feature in data["features"]:
        mag = feature["properties"]["mag"]
        place = feature["properties"]["place"]
        lon, lat, _ = feature["geometry"]["coordinates"]
        map_data.append("[{}, {}, 'M{}: {}'],".format(lat, lon, mag, place))

    html = MAP_TEMPLATE.substitute(data="\n".join(map_data))

    if filename:
        with open(filename, "wt") as outfile:
            print(html, file=outfile)

    return html


if __name__ == '__main__':
    import sys

    try:
        level = sys.argv[1]
        period = sys.argv[2]
        filename = sys.argv[3]
    except:
        sys.exit("Usage: python quakes.py <level> <period> <filename>")

    data = get_data(level, period)
    generate_map(data, filename)
