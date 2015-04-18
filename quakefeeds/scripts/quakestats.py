"""
quakestats

Computes some basic statistics for earthquakes in a USGS data feed.
The desired feed is specified using severity level and period.
Severity level can be "significant", "4.5", "2.5", "1.0", "all".
Period can be "hour", "day", "week", "month".

Usage: quakestats [options] <level> <period>

Options:

  -h --help   Show this help
"""

import statistics
from docopt import docopt
from quakefeeds import QuakeFeed

def main():
    args = docopt(__doc__)

    level = args["<level>"]
    period = args["<period>"]

    feed = QuakeFeed(level, period)

    mean_magnitude = statistics.mean(feed.magnitudes)
    median_magnitude = statistics.median(feed.magnitudes)
    mean_depth = statistics.mean(feed.depths)
    median_depth = statistics.median(feed.depths)

    print(len(feed), "events processed.")
    print("Mean magnitude   = {:.1f}".format(mean_magnitude))
    print("Median magnitude = {:.1f}".format(median_magnitude))
    print("Mean depth       = {:.1f} km".format(mean_depth))
    print("Median depth     = {:.1f} km".format(median_depth))
