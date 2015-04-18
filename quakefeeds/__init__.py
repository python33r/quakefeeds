"""
Python 3 tools for handling USGS earthquake data feeds.

The main tool is the class QuakeFeed, which represents a GeoJSON
data feed and provides easy ways of interacting with the data.

Feeds and a description of their format are available at
http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
"""

import io
import requests
from datetime import datetime, timezone


URL = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{}_{}.geojson"

ALLOWED_LEVELS  = { "significant", "4.5", "2.5", "1.0", "all" }
ALLOWED_PERIODS = { "hour", "day", "week", "month" }


class QuakeFeed:
    """
    Represents a USGS Earthquake Hazards Program GeoJSON data feed.

    The class provides a thin object-oriented wrapper around the
    deserialized JSON data, simplifying the extraction of interesting
    items such as quake magnitudes, quake locations, etc.  The raw
    data remain accessible as a standard Python dictionary, via
    the 'data' attribute.
    """

    MAP_STYLES = ("plain", "titled")

    def __init__(self, level, period):
        """
        Captures the feed with the given severity level and period.

        ValueError is raised if either severity level or period are not
        supported by the USGS data feeds.  IOError is raised if the
        response status following the request for data is not 200 OK.
        """
        if level.lower() not in ALLOWED_LEVELS:
            raise ValueError("invalid severity level")
        if period.lower() not in ALLOWED_PERIODS:
            raise ValueError("invalid period")

        feed_url = URL.format(level.lower(), period.lower())
        response = requests.get(feed_url)

        if response.status_code != 200:
            message = "HTTP status code {:d}".format(response.status_code)
            raise IOError(message)

        self.data = response.json()

    # Special methods

    def __len__(self):
        """
        Returns the number of events captured from the data feed.
        """
        return self.data["metadata"]["count"]

    def __getitem__(self, index):
        """
        Returns the JSON data for a specific event, given its index.
        """
        return self.event(index)

    # Properties associated with the feed

    @property
    def url(self):
        """
        The URL of this feed.
        """
        return self.data["metadata"]["url"]

    @property
    def title(self):
        """
        The title of this feed.

        Example: "USGS Magnitude 4.5+ Earthquakes, Past Week"
        """
        return self.data["metadata"]["title"]

    @property
    def time(self):
        """
        Time of feed acquisition.

        This is a standard datetime object, using UTC as timezone.
        """
        t = self.data["metadata"]["generated"] / 1000.0

        return datetime.fromtimestamp(t, tz=timezone.utc)

    @property
    def bbox(self):
        """
        Bounding box of the events represented by this feed.

        Elements of this list are min longitude, min latiude, min
        depth, max longitude, max latitude, max depth. 

        See http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
        and http://geojson.org/geojson-spec.html#bounding-boxes
        """
        return self.data["bbox"]

    # Iterators for specific event data

    @property
    def events(self):
        """
        A generator that allows iteration over all events in the feed.
        """
        for event in self.data["features"]:
            yield event

    @property
    def event_times(self):
        """
        A generator that allows iteration over all event times.
        """
        for event in self.data["features"]:
            t = event["properties"]["time"] / 1000.0
            yield datetime.fromtimestamp(t, tz=timezone.utc)

    @property
    def locations(self):
        """
        A generator that allows iteration over event locations.
        """
        for event in self.data["features"]:
            yield event["geometry"]["coordinates"][:2]

    @property
    def places(self):
        """
        A generator that allows iteration over place descriptions.
        """
        for event in self.data["features"]:
            yield event["properties"]["place"]

    @property
    def magnitudes(self):
        """
        A generator that allows iteration over event magnitudes.
        """
        for event in self.data["features"]:
            yield event["properties"]["mag"]

    @property
    def depths(self):
        """
        A generator that allows iteration over event depths.
        """
        for feature in self.data["features"]:
            yield feature["geometry"]["coordinates"][2]

    # Methods to access data for an individual event

    def event(self, index):
        """
        Returns full JSON data for a specific event, given its index.
        """
        return self.data["features"][index]

    def event_time(self, index):
        """
        Returns the time at which an event took place, given its index.
        """
        t = self[index]["properties"]["time"] / 1000.0

        return datetime.fromtimestamp(t, tz=timezone.utc)

    def event_title(self, index):
        """
        Returns the title of an event, given its index.
        """
        return self[index]["properties"]["title"]

    def location(self, index):
        """
        Returns a 2-element list containing the longitude and latitude
        of a specific event, given its index.
        """
        return self[index]["geometry"]["coordinates"][:2]

    def place(self, index):
        """
        Returns the text description of a named geographic region near
        a specific event, given its index.
        """
        return self[index]["properties"]["place"]

    def magnitude(self, index):
        """
        Returns the magnitude of an event, given its index.
        """
        return self[index]["properties"]["mag"]

    def depth(self, index):
        """
        Returns the depth of an event in km, given its index.
        """
        return self[index]["geometry"]["coordinates"][2]

    # Other methods

    def refresh(self):
        """
        Updates this feed with new data.

        IOError is raised if data acquisition fails.
        """
        response = requests.get(self.url)

        if response.status_code != 200:
            message = "HTTP status code {:d}".format(response.status_code)
            raise IOError(message)

        self.data = response.json()

    def create_google_map(self, **kwargs):
        """
        Plots events from this feed on a Google map, returning the HTML
        for the map as a string.

        The location of each event will be marked.  Clicking on a marker
        will display an info bubble containing the magnitude of the event
        and a description of its location.

        The Jinja2 template engine (http://jinja.pocoo.org) is used to
        generate the HTML.  This can be used either with built-in templates
        or with your own.  A built-in template is selected using the
        'style' keyword argument; the default is 'plain'.

        If you wish to provide your own template, you will need to supply
        a Jinja2 Environment object using the 'env' keyword argument *and*
        a template filename using the 'tpfile' keyboard argument.
        """

        from jinja2 import Environment, PackageLoader

        # Set up Jinja2 environment and template

        env = kwargs.get("env")

        if env is None:
            env = Environment(loader=PackageLoader("quakefeeds"))
            style = kwargs.get("style", "plain")
            if style not in self.MAP_STYLES:
                raise ValueError("invalid map style")
            tpfile = style + ".html"
        else:
            if not isinstance(env, Environment):
                raise ValueError("env must be a Jinja2 Environment")
            tpfile = kwargs.get("tpfile")
            if tpfile is None:
                raise ValueError("tpfile argument not supplied")

        # Extract plottable data

        max_points = 300   # Google API limit

        map_data = []
        for event in self.data["features"][:max_points]:
            mag = event["properties"]["mag"]
            place = event["properties"]["place"]
            lon, lat, _ = event["geometry"]["coordinates"]
            map_data.append((lat, lon, mag, place))

        # Render template using extracted event data

        template = env.get_template(tpfile)
        html = template.render(data=map_data, feed=self)

        return html

    def write_google_map(self, output=None, **kwargs):
        """
        Calls create_google_map to generate a map in HTML form, then
        writes this map to the given destination.

        Destinations can be specified either as a filename or as a
        file-like object that has already been opened for text output.
        If no destination is specified, the map is written to stdout.
        """

        html = self.create_google_map(**kwargs)

        if output is None:
            print(html)
        elif isinstance(output, str):
            with open(output, "wt") as outfile:
                print(html, file=outfile)
        elif isinstance(output, io.TextIOBase):
            if not output.writable():
                raise IOError("destination not writable")
            print(html, file=output)
        else:
            raise ValueError("unsuitable output")
