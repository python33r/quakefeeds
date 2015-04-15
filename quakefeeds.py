"""
Tools for handling USGS earthquake data feeds.

This module provides a simple way of retrieving earthquake data
for a given minimum severity level and time period from a web
service run by the USGS Earthquake Hazards Program.  It also
provides the means to generate a Google map showing earthquake
locations and other details such as magnitude.

Feeds and a description of their format are available at
http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
"""

import urllib.request, json, io
from jinja2 import Environment, FileSystemLoader


URL = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{}_{}.geojson"

ALLOWED_LEVELS = ("significant", "4.5", "2.5", "1.0", "all")
ALLOWED_PERIODS = ("hour", "day", "week", "month")

TEMPLATE_PATH = "."
TEMPLATE_FILE = "map-template.html"


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


def generate_map(data, output=None):
    """Plots earthquakes from the given GeoJSON dataset on a Google map.

       The location of each earthquake will be marked.  Clicking on a
       marker will display an info bubble containing the magnitude of the
       quake and a description of its location.

       The HTML for the map is returned as a string.  If a filename or a
       file-like object that supports text output is specified as a second
       argument, the HTML will also be written to that destination.
    """

    quakes = []
    for feature in data["features"]:
        mag = feature["properties"]["mag"]
        place = feature["properties"]["place"]
        lon, lat, _ = feature["geometry"]["coordinates"]
        quakes.append((lat, lon, mag, place))

    env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
    template = env.get_template(TEMPLATE_FILE)
    html = template.render(quakes=quakes)

    if isinstance(output, str):
        with open(output, "wt") as outfile:
            print(html, file=outfile)
    elif isinstance(output, io.TextIOBase):
        if not output.writable():
            raise ValueError("destination not writable")
        print(html, file=output)

    return html
