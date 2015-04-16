quakefeeds
==========

Python 3 tools for handling USGS earthquake data feeds.

The `quakefeeds` package provides a class `QuakeFeed` that captures data
from a GeoJSON feed, given a valid severity level and time period.
The class provides some shortcuts for accessing data of interest within
the feed and provides other useful methods - e.g. one to generate a simple
Google map showing quake locations and other details.

The data feeds and a description of their GeoJSON format are available at
http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php.

Examples of Use
---------------

```python
>>> from quakefeeds import QuakeFeed
>>> feed = QuakeFeed("4.5", "day")
>>> feed.title
'USGS Magnitude 4.5+ Earthquakes, Past Day'
>>> feed.time
datetime.datetime(2015, 4, 16, 19, 18, 39, tzinfo=datetime.timezone.utc)
>>> len(feed)
6
>>> feed[0]
{'properties': {'cdi': 1, 'tsunami': 0, 'alert': None, ...}
# full JSON data for first event in feed
>>> feed.location(0)
[26.8608, 35.135]
>>> feed.magnitude(0)
6.1
>>> feed.title(0)
'M 6.1 - 47km SW of Karpathos, Greece'
>>> feed.depth(0)
20.86
>>> feed.depths
<generator object depths at 0x7fef054b5fc0>
>>> list(feed.depths)
[20.86, 46.35, 76.54, 48.69, 10, 28.64]
>>> feed.create_google_map("quakemap.html")
>>> feed.create_google_map("quakemap2.html", style="titled")
```

Dependencies
------------

* Python 3 is required.

* [Requests](http://python-requests.org) is used to acquire feed data.

* The [Jinja2](http://jinja.pocoo.org) template engine is needed if you wish
  to produce maps from a feed using the ``create_google_map`` method, but
  otherwise does not need to be installed.
