"""
quakemap

Generates a Google map of the earthquakes in a USGS data feed.

Usage: quakemap [options] <level> <period>

Options:

  -h --help   Show this help
  -o <file>   Specify an output file instead of stdout
  -s <style>  Specify map style [default: plain]
"""

from docopt import docopt
from quakefeeds import QuakeFeed

def main():
    args = docopt(__doc__)

    level = args["<level>"]
    period = args["<period>"]
    filename = args["-o"]
    style = args["-s"]

    feed = QuakeFeed(level, period)
    feed.write_google_map(filename, style=style)
