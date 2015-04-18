quakefeeds
==========

Python 3 tools for handling USGS earthquake data feeds.

The ``quakefeeds`` package provides a class ``QuakeFeed`` that captures data
from a GeoJSON feed, given a valid severity level and time period.
The class provides some shortcuts for accessing data of interest within
the feed and provides other useful methods - e.g. one to generate a simple
Google map plotting quake locations and magnitudes.

The data feeds and a description of their GeoJSON format are available at
http://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php.


Examples of Use
---------------

.. code-block:: python

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
   >>> feed.event_title(0)
   'M 6.1 - 47km SW of Karpathos, Greece'
   >>> feed.depth(0)
   20.86
   >>> feed.depths
   <generator object depths at 0x7fef054b5fc0>
   >>> list(feed.depths)
   [20.86, 46.35, 76.54, 48.69, 10, 28.64]
   >>> map1 = feed.create_google_map()
   >>> map2 = feed.create_google_map(style="titled")
   >>> feed.write_google_map("map.html", style="titled")


Scripts
-------

The installation process will install some scripts in addition to the
``quakefeeds`` package:

* ``quakemap``, which plots earthquakes on a Google map
* ``quakestats``, which computes basic statistics for a feed


Dependencies
------------

* Python 3
* `Requests <http://python-requests.org>`_
* `Jinja2 <http://jinja.pocoo.org>`_ template engine (for map generation)
* `docopt <http://docopt.org>`_ (for the scripts)


Installation
------------

Use `pip <http://pip-installer.org>`_ to install the package, its scripts
and their dependencies::

  pip install quakefeeds

Alternatively, you can install from within the unpacked source distribution::

  python setup.py install

(Note that this requires prior installation of
`setuptools <http://pythonhosted.org/setuptools/>`_.)

If you don't want the scripts, copying the ``quakefeeds`` directory from
the source distribution to somewhere in your PYTHONPATH will suffice.
