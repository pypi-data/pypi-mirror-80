# pythumbnailer

Create static HTML galleries with thumbnails.

Supports:
- Many types of images
- Many types of videos (using `ffpmeg`)
- GPS Tracks in GPX format

The architecture should it make it relatively simple to add more types.

## Installation

This is available on PyPI: https://pypi.org/project/pythumbnailer/

```sh
$ pip install pythumbnailer
```

It's also available on AUR: https://aur.archlinux.org/packages/pythumbnailer/

## Dependencies

This is only tested on Linux, but it should work on Windows.

The Python dependencies are shown on `requirements.txt`.

This also requires a non-Python dependency.

### FFMPEG

Both `ffmpeg` and `ffprobe` should be available. Install the version that comes
without your operating system.

### HTML

The generated HTML should be mostly self-contained and standards-compliant. For
advanced features it is needed to use Javascript libraries, bundled on the
repository itself (see the `pythumbnailer/static/lib/` folder.

Here is the list of all dependencies:

#### Leaflet

The library that supports slippy maps:

- https://leafletjs.com/
- http://github.com/Leaflet/Leaflet

This uses some plugins, installed as other dependencies.

#### Leaflet Elevation

Leaflet plugin. Show the elevation graph.

- https://github.com/Raruto/leaflet-elevation

#### Leaflet GPX

Leaflet plugin. Support GPX files in-browser.

- https://github.com/mpetazzoni/leaflet-gpx

#### D3.js

Dependency for `leaflet-elevation`.

- https://d3js.org/
- https://github.com/d3/d3
