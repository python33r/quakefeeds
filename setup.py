from setuptools import setup, find_packages

setup(
  name="quakefeeds",
  version="0.2",
  description="Python 3 tools for handling USGS earthquake data feeds",
  long_description=open("README.rst").read(),
  url="https://github.com/python33r/quakefeeds",
  author="Nick Efford",
  author_email="nick.efford@gmail.com",
  packages=find_packages(),
  package_data = {
    "": ["templates/*.html"],
  },
  scripts=[
    "scripts/quakemap.py",
  ],
  install_requires=[
    "Requests",
    "Jinja2",
  ],
  platforms="any",
  license="MIT",
  keywords="data json science seismology usgs",
  classifiers=[
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering",
  ]
)
