#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time   : 2020/9/7 10:41 AM
# @Author : Dutt
# @Email  : dutengteng1@163.com
# @File   : raster2tiles.py



# ******************************************************************************
# Purpose : Support tianditu (EPSG 4490) Latitude and longitude projection.
#           Support convert to lerc tile.
#           Support upload tile file to cloud storage (s3,oss)
# Author : dutengteng, GAGO
# ******************************************************************************
#  $Id: gdal2tiles.py 39836 2017-08-16 12:51:57Z rouault $
#
# Project:  Google Summer of Code 2007, 2008 (http://code.google.com/soc/)
# Support:  BRGM (http://www.brgm.fr)
# Purpose:  Convert a raster into TMS (Tile Map Service) tiles in a directory.
#           - generate Google Earth metadata (KML SuperOverlay)
#           - generate simple HTML viewer based on Google Maps and OpenLayers
#           - support of global tiles (Spherical Mercator) for compatibility
#               with interactive web maps a la Google Maps
# Author:   Klokan Petr Pridal, klokan at klokan dot cz
# Web:      http://www.klokan.cz/projects/gdal2tiles/
# GUI:      http://www.maptiler.org/
#
###############################################################################
# Copyright (c) 2008, Klokan Petr Pridal
# Copyright (c) 2010-2013, Even Rouault <even dot rouault at mines-paris dot org>
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
# ******************************************************************************

import platform
import os
import sys
import shutil
import math
import json
from uuid import uuid4
from osgeo import gdal
from osgeo import osr


try:
    from PIL import Image
    import numpy
    import osgeo.gdal_array as gdalarray
except Exception:
    # 'antialias' resampling is not available
    pass

from gagoos.storage import StorageService
from gagoos.storage import create_service_from_config

__version__ = "$Id: raster2tiles.py 39836 2020-09-16 12:51:57Z rouault $"

resampling_list = ('average', 'near', 'bilinear', 'cubic', 'cubicspline', 'lanczos',  'antialias')
profile_list = ('mercator', 'geodetic', 'tianditu','raster')
format_list = ('PNG', 'GTiff', 'Lerc')
access_list = ('private', 'public-read', 'public-read-write', 'authenticated-read')
webviewer_list = ('all', 'google', 'openlayers', 'leaflet', 'none')
overwrite_list = ('skip', 'overwrite', 'merge')

# =============================================================================
# =============================================================================
# =============================================================================

__doc__globalmaptiles = """
globalmaptiles.py

Global Map Tiles as defined in Tile Map Service (TMS) Profiles
==============================================================

Functions necessary for generation of global tiles used on the web.
It contains classes implementing coordinate conversions for:

  - GlobalMercator (based on EPSG:3857)
       for Google Maps, Yahoo Maps, Bing Maps compatible tiles
  - GlobalGeodetic (based on EPSG:4326)
       for OpenLayers Base Map and Google Earth compatible tiles

More info at:

http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification
http://wiki.osgeo.org/wiki/WMS_Tiling_Client_Recommendation
http://msdn.microsoft.com/en-us/library/bb259689.aspx
http://code.google.com/apis/maps/documentation/overlays.html#Google_Maps_Coordinates

Created by Klokan Petr Pridal on 2008-07-03.
Google Summer of Code 2008, project GDAL2Tiles for OSGEO.

In case you use this class in your product, translate it to another language
or find it useful for your project please let me know.
My email: klokan at klokan dot cz.
I would like to know where it was used.

Class is available under the open-source GDAL license (www.gdal.org).
"""

MAXZOOMLEVEL = 32


class GlobalMercator(object):
    r"""
    TMS Global Mercator Profile
    ---------------------------

    Functions necessary for generation of tiles in Spherical Mercator projection,
    EPSG:3857.

    Such tiles are compatible with Google Maps, Bing Maps, Yahoo Maps,
    UK Ordnance Survey OpenSpace API, ...
    and you can overlay them on top of base maps of those web mapping applications.

    Pixel and tile coordinates are in TMS notation (origin [0,0] in bottom-left).

    What coordinate conversions do we need for TMS Global Mercator tiles::

         LatLon      <->       Meters      <->     Pixels    <->       Tile

     WGS84 coordinates   Spherical Mercator  Pixels in pyramid  Tiles in pyramid
         lat/lon            XY in meters     XY pixels Z zoom      XYZ from TMS
        EPSG:4326           EPSG:387
         .----.              ---------               --                TMS
        /      \     <->     |       |     <->     /----/    <->      Google
        \      /             |       |           /--------/          QuadTree
         -----               ---------         /------------/
       KML, public         WebMapService         Web Clients      TileMapService

    What is the coordinate extent of Earth in EPSG:3857?

      [-20037508.342789244, -20037508.342789244, 20037508.342789244, 20037508.342789244]
      Constant 20037508.342789244 comes from the circumference of the Earth in meters,
      which is 40 thousand kilometers, the coordinate origin is in the middle of extent.
      In fact you can calculate the constant as: 2 * math.pi * 6378137 / 2.0
      $ echo 180 85 | gdaltransform -s_srs EPSG:4326 -t_srs EPSG:3857
      Polar areas with abs(latitude) bigger then 85.05112878 are clipped off.

    What are zoom level constants (pixels/meter) for pyramid with EPSG:3857?

      whole region is on top of pyramid (zoom=0) covered by 256x256 pixels tile,
      every lower zoom level resolution is always divided by two
      initialResolution = 20037508.342789244 * 2 / 256 = 156543.03392804062

    What is the difference between TMS and Google Maps/QuadTree tile name convention?

      The tile raster itself is the same (equal extent, projection, pixel size),
      there is just different identification of the same raster tile.
      Tiles in TMS are counted from [0,0] in the bottom-left corner, id is XYZ.
      Google placed the origin [0,0] to the top-left corner, reference is XYZ.
      Microsoft is referencing tiles by a QuadTree name, defined on the website:
      http://msdn2.microsoft.com/en-us/library/bb259689.aspx

    The lat/lon coordinates are using WGS84 datum, yes?

      Yes, all lat/lon we are mentioning should use WGS84 Geodetic Datum.
      Well, the web clients like Google Maps are projecting those coordinates by
      Spherical Mercator, so in fact lat/lon coordinates on sphere are treated as if
      the were on the WGS84 ellipsoid.

      From MSDN documentation:
      To simplify the calculations, we use the spherical form of projection, not
      the ellipsoidal form. Since the projection is used only for map display,
      and not for displaying numeric coordinates, we don't need the extra precision
      of an ellipsoidal projection. The spherical projection causes approximately
      0.33 percent scale distortion in the Y direction, which is not visually
      noticeable.

    How do I create a raster in EPSG:3857 and convert coordinates with PROJ.4?

      You can use standard GIS tools like gdalwarp, cs2cs or gdaltransform.
      All of the tools supports -t_srs 'epsg:3857'.

      For other GIS programs check the exact definition of the projection:
      More info at http://spatialreference.org/ref/user/google-projection/
      The same projection is designated as EPSG:3857. WKT definition is in the
      official EPSG database.

      Proj4 Text:
        +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0
        +k=1.0 +units=m +nadgrids=@null +no_defs

      Human readable WKT format of EPSG:3857:
         PROJCS["Google Maps Global Mercator",
             GEOGCS["WGS 84",
                 DATUM["WGS_1984",
                     SPHEROID["WGS 84",6378137,298.257223563,
                         AUTHORITY["EPSG","7030"]],
                     AUTHORITY["EPSG","6326"]],
                 PRIMEM["Greenwich",0],
                 UNIT["degree",0.0174532925199433],
                 AUTHORITY["EPSG","4326"]],
             PROJECTION["Mercator_1SP"],
             PARAMETER["central_meridian",0],
             PARAMETER["scale_factor",1],
             PARAMETER["false_easting",0],
             PARAMETER["false_northing",0],
             UNIT["metre",1,
                 AUTHORITY["EPSG","9001"]]]
    """

    def __init__(self, tileSize=256):
        "Initialize the TMS Global Mercator pyramid"
        self.tileSize = tileSize
        self.initialResolution = 2 * math.pi * 6378137 / self.tileSize
        # 156543.03392804062 for tileSize 256 pixels
        self.originShift = 2 * math.pi * 6378137 / 2.0
        # 20037508.342789244

    def LatLonToMeters(self, lat, lon):
        "Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:3857"

        mx = lon * self.originShift / 180.0
        my = math.log(math.tan((90 + lat) * math.pi / 360.0)) / (math.pi / 180.0)

        my = my * self.originShift / 180.0
        return mx, my

    def MetersToLatLon(self, mx, my):
        "Converts XY point from Spherical Mercator EPSG:3857 to lat/lon in WGS84 Datum"

        lon = (mx / self.originShift) * 180.0
        lat = (my / self.originShift) * 180.0

        lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
        return lat, lon

    def PixelsToMeters(self, px, py, zoom):
        "Converts pixel coordinates in given zoom level of pyramid to EPSG:3857"

        res = self.Resolution(zoom)
        mx = px * res - self.originShift
        my = py * res - self.originShift
        return mx, my

    def MetersToPixels(self, mx, my, zoom):
        "Converts EPSG:3857 to pyramid pixel coordinates in given zoom level"

        res = self.Resolution(zoom)
        px = (mx + self.originShift) / res
        py = (my + self.originShift) / res
        return px, py

    def PixelsToTile(self, px, py):
        "Returns a tile covering region in given pixel coordinates"

        tx = int(math.ceil(px / float(self.tileSize)) - 1)
        ty = int(math.ceil(py / float(self.tileSize)) - 1)
        return tx, ty

    def PixelsToRaster(self, px, py, zoom):
        "Move the origin of pixel coordinates to top-left corner"

        mapSize = self.tileSize << zoom
        return px, mapSize - py

    def MetersToTile(self, mx, my, zoom):
        "Returns tile for given mercator coordinates"

        px, py = self.MetersToPixels(mx, my, zoom)
        return self.PixelsToTile(px, py)

    def TileBounds(self, tx, ty, zoom):
        "Returns bounds of the given tile in EPSG:3857 coordinates"

        minx, miny = self.PixelsToMeters(tx*self.tileSize, ty*self.tileSize, zoom)
        maxx, maxy = self.PixelsToMeters((tx+1)*self.tileSize, (ty+1)*self.tileSize, zoom)
        return (minx, miny, maxx, maxy)

    def TileLatLonBounds(self, tx, ty, zoom):
        "Returns bounds of the given tile in latitude/longitude using WGS84 datum"

        bounds = self.TileBounds(tx, ty, zoom)
        minLat, minLon = self.MetersToLatLon(bounds[0], bounds[1])
        maxLat, maxLon = self.MetersToLatLon(bounds[2], bounds[3])

        return (minLat, minLon, maxLat, maxLon)

    def Resolution(self, zoom):
        "Resolution (meters/pixel) for given zoom level (measured at Equator)"

        # return (2 * math.pi * 6378137) / (self.tileSize * 2**zoom)
        return self.initialResolution / (2**zoom)

    def ZoomForPixelSize(self, pixelSize):
        "Maximal scaledown zoom of the pyramid closest to the pixelSize."

        for i in range(MAXZOOMLEVEL):
            if pixelSize > self.Resolution(i):
                if i != -1:
                    return i-1
                else:
                    return 0    # We don't want to scale up

    def GoogleTile(self, tx, ty, zoom):
        "Converts TMS tile coordinates to Google Tile coordinates"

        # coordinate origin is moved from bottom-left to top-left corner of the extent
        return tx, (2**zoom - 1) - ty

    def QuadTree(self, tx, ty, zoom):
        "Converts TMS tile coordinates to Microsoft QuadTree"

        quadKey = ""
        ty = (2**zoom - 1) - ty
        for i in range(zoom, 0, -1):
            digit = 0
            mask = 1 << (i-1)
            if (tx & mask) != 0:
                digit += 1
            if (ty & mask) != 0:
                digit += 2
            quadKey += str(digit)

        return quadKey


class GlobalGeodetic(object):
    r"""
    TMS Global Geodetic Profile
    ---------------------------

    Functions necessary for generation of global tiles in Plate Carre projection,
    EPSG:4326, "unprojected profile".

    Such tiles are compatible with Google Earth (as any other EPSG:4326 rasters)
    and you can overlay the tiles on top of OpenLayers base map.

    Pixel and tile coordinates are in TMS notation (origin [0,0] in bottom-left).

    What coordinate conversions do we need for TMS Global Geodetic tiles?

      Global Geodetic tiles are using geodetic coordinates (latitude,longitude)
      directly as planar coordinates XY (it is also called Unprojected or Plate
      Carre). We need only scaling to pixel pyramid and cutting to tiles.
      Pyramid has on top level two tiles, so it is not square but rectangle.
      Area [-180,-90,180,90] is scaled to 512x256 pixels.
      TMS has coordinate origin (for pixels and tiles) in bottom-left corner.
      Rasters are in EPSG:4326 and therefore are compatible with Google Earth.

         LatLon      <->      Pixels      <->     Tiles

     WGS84 coordinates   Pixels in pyramid  Tiles in pyramid
         lat/lon         XY pixels Z zoom      XYZ from TMS
        EPSG:4326
         .----.                ----
        /      \     <->    /--------/    <->      TMS
        \      /         /--------------/
         -----        /--------------------/
       WMS, KML    Web Clients, Google Earth  TileMapService
    """

    def __init__(self, tmscompatible, tileSize=256):
        self.tileSize = tileSize
        if tmscompatible is not None:
            # Defaults the resolution factor to 0.703125 (2 tiles @ level 0)
            # Adhers to OSGeo TMS spec
            # http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification#global-geodetic
            self.resFact = 180.0 / self.tileSize
        else:
            # Defaults the resolution factor to 1.40625 (1 tile @ level 0)
            # Adheres OpenLayers, MapProxy, etc default resolution for WMTS
            self.resFact = 360.0 / self.tileSize

    def LonLatToPixels(self, lon, lat, zoom):
        "Converts lon/lat to pixel coordinates in given zoom of the EPSG:4326 pyramid"

        res = self.resFact / 2**zoom
        px = (180 + lon) / res
        py = (90 + lat) / res
        return px, py

    def PixelsToTile(self, px, py):
        "Returns coordinates of the tile covering region in pixel coordinates"

        tx = int(math.ceil(px / float(self.tileSize)) - 1)
        ty = int(math.ceil(py / float(self.tileSize)) - 1)
        return tx, ty

    def LonLatToTile(self, lon, lat, zoom):
        "Returns the tile for zoom which covers given lon/lat coordinates"

        px, py = self.LonLatToPixels(lon, lat, zoom)
        return self.PixelsToTile(px, py)

    def Resolution(self, zoom):
        "Resolution (arc/pixel) for given zoom level (measured at Equator)"

        return self.resFact / 2**zoom

    def ZoomForPixelSize(self, pixelSize):
        "Maximal scaledown zoom of the pyramid closest to the pixelSize."

        for i in range(MAXZOOMLEVEL):
            if pixelSize > self.Resolution(i):
                if i != 0:
                    return i-1
                else:
                    return 0    # We don't want to scale up

    def TileBounds(self, tx, ty, zoom):
        "Returns bounds of the given tile"
        res = self.resFact / 2**zoom
        return (
            tx*self.tileSize*res - 180,
            ty*self.tileSize*res - 90,
            (tx+1)*self.tileSize*res - 180,
            (ty+1)*self.tileSize*res - 90
        )

    def TileLatLonBounds(self, tx, ty, zoom):
        "Returns bounds of the given tile in the SWNE form"
        b = self.TileBounds(tx, ty, zoom)
        return (b[1], b[0], b[3], b[2])


class Zoomify(object):
    """
    Tiles compatible with the Zoomify viewer
    ----------------------------------------
    """

    def __init__(self, width, height, tilesize=256, tileformat='jpg'):
        """Initialization of the Zoomify tile tree"""

        self.tilesize = tilesize
        self.tileformat = tileformat
        imagesize = (width, height)
        tiles = (math.ceil(width / tilesize), math.ceil(height / tilesize))

        # Size (in tiles) for each tier of pyramid.
        self.tierSizeInTiles = []
        self.tierSizeInTiles.append(tiles)

        # Image size in pixels for each pyramid tierself
        self.tierImageSize = []
        self.tierImageSize.append(imagesize)

        while (imagesize[0] > tilesize or imagesize[1] > tilesize):
            imagesize = (math.floor(imagesize[0] / 2), math.floor(imagesize[1] / 2))
            tiles = (math.ceil(imagesize[0] / tilesize), math.ceil(imagesize[1] / tilesize))
            self.tierSizeInTiles.append(tiles)
            self.tierImageSize.append(imagesize)

        self.tierSizeInTiles.reverse()
        self.tierImageSize.reverse()

        # Depth of the Zoomify pyramid, number of tiers (zoom levels)
        self.numberOfTiers = len(self.tierSizeInTiles)

        # Number of tiles up to the given tier of pyramid.
        self.tileCountUpToTier = []
        self.tileCountUpToTier[0] = 0
        for i in range(1, self.numberOfTiers+1):
            self.tileCountUpToTier.append(
                self.tierSizeInTiles[i-1][0] * self.tierSizeInTiles[i-1][1] +
                self.tileCountUpToTier[i-1]
            )

    def tilefilename(self, x, y, z):
        """Returns filename for tile with given coordinates"""

        tileIndex = x + y * self.tierSizeInTiles[z][0] + self.tileCountUpToTier[z]
        return os.path.join("TileGroup%.0f" % math.floor(tileIndex / 256),
                            "%s-%s-%s.%s" % (z, x, y, self.tileformat))


class Gdal2TilesError(Exception):
    pass


class Raster2Tiles(object):

    def process(self):
        """The main processing function, runs all the main steps of processing"""
        try:
            # Opening and preprocessing of the input file
            self.open_input()

            # Generation of main metadata files and HTML viewers
            # self.generate_metadata()

            # Generation of the lowest tiles
            self.generate_base_tiles()

            # Generation of the overview tiles (higher in the pyramid)
            self.generate_overview_tiles()

            if self.lerc:
                if os.path.exists(self.tempdir):
                    shutil.rmtree(self.tempdir)
                tifdir = os.path.join(self.output, "tif")
                lercdir = os.path.join(self.output, "lerc")

                self.tiff2lerc(tifdir, lercdir)

                if self.storage_service is not None:
                    if self.onlylerc:
                        lercprefix = self.options.prefix
                    else:
                        lercprefix = os.path.join(self.options.prefix, "lerc")
                        tifprefix = os.path.join(self.options.prefix, "tif")
                        print(
                            'Uploading tif tile files to cloud storage.'
                        )
                        self.uploadtile2cloudstorage(tifdir, tifprefix, ".tif")

                    print(
                        'Uploading lerc tile files to cloud storage.'
                    )
                    self.uploadtile2cloudstorage(lercdir, lercprefix, ".lerc")

        except Exception as e:
            print(e)
        finally:
            if self.options is not None:
                if self.storage_service is not None and os.path.exists(self.output):
                    shutil.rmtree(self.options.output)
                if self.storage_service is None and os.path.exists(self.tempdir):
                    shutil.rmtree(self.tempdir)
                pass

    def uploadtile2cloudstorage(self, tiledir, csprefix, tilepostfix):

        print(
            'Uploading tile tile files to cloud storage.'
        )
        for root, dirs, files in os.walk(tiledir):
            for file in files:
                if os.path.splitext(file)[1] == tilepostfix:
                    tilefile = os.path.join(root, file)
                    tilebasename = os.path.basename(tilefile)
                    l_z = tilefile.split("/")[-3]
                    l_x = tilefile.split("/")[-2]
                    cs_tilefilename = os.path.join(
                        csprefix,
                        l_z,
                        l_x,
                        tilebasename
                    )
                    try:
                        if self.options.verbose:
                            print(
                                'Uploading %s tile tile %s to cloud storage.' %
                                (cs_tilefilename, tilepostfix)
                            )
                        self.storage_service.upload_file(
                            self.options.bucket,
                            cs_tilefilename,
                            tilefile,
                            self.options.access
                        )
                    except Exception as e:
                        self.error(e)
                    finally:
                        if os.path.exists(tilefile):
                            os.remove(tilefile)


    # def uploadtif2cloudstorage(self, tifdir, csprefix, tilepostfix):
    #
    #     print(
    #         'Uploading tif tile files to cloud storage.'
    #     )
    #     for root, dirs, files in os.walk(tifdir):
    #         for file in files:
    #             if os.path.splitext(file)[1] == tilepostfix:
    #                 tiffile = os.path.join(root, file)
    #                 tifbasename = os.path.basename(tiffile)
    #                 l_z = tiffile.split("/")[-3]
    #                 l_x = tiffile.split("/")[-2]
    #                 cs_tiftilefilename = os.path.join(
    #                     csprefix,
    #                     l_z,
    #                     l_x,
    #                     tifbasename
    #                 )
    #
    #                 try:
    #                     if self.options.verbose:
    #                         print(
    #                             'Uploading tif tile tile %s to cloud storage.' %
    #                             cs_tiftilefilename
    #                         )
    #                     self.storage_service.upload_file(
    #                         self.options.bucket,
    #                         cs_tiftilefilename,
    #                         tiffile,
    #                         self.options.access
    #                     )
    #                 except Exception as e:
    #                     self.error(e)
    #                 finally:
    #                     if os.path.exists(tiffile):
    #                         os.remove(tiffile)


    def error(self, msg, details=""):
        """Print an error message and stop the processing"""
        if details:
            self.parser.error(msg + "\n\n" + details)
        else:
            self.parser.error(msg)

    def progressbar(self, complete=0.0):
        """Print progressbar for float value 0..1"""
        gdal.TermProgress_nocb(complete)

    def gettempfilename(self, suffix):
        """Returns a temporary filename"""
        if '_' in os.environ:
            # tempfile.mktemp() crashes on some Wine versions (the one of Ubuntu 12.04 particularly)
            if os.environ['_'].find('wine') >= 0:
                tmpdir = '.'
                if 'TMP' in os.environ:
                    tmpdir = os.environ['TMP']
                import time
                import random
                random.seed(time.time())
                random_part = 'file%d' % random.randint(0, 1000000000)
                return os.path.join(tmpdir, random_part + suffix)

        import tempfile
        return tempfile.mktemp(suffix)

    def stop(self):
        """Stop the rendering immediately"""
        self.stopped = True

    def __init__(self, arguments):
        """Constructor function - initialization"""
        self.out_drv = None
        self.mem_drv = None
        self.in_ds = None
        self.out_ds = None
        self.out_srs = None
        self.nativezoom = None
        self.tminmax = None
        self.tsize = None
        self.mercator = None
        self.geodetic = None
        self.alphaband = None
        self.dataBandsCount = None
        self.out_gt = None
        self.tileswne = None
        self.swne = None
        self.ominx = None
        self.omaxx = None
        self.omaxy = None
        self.ominy = None
        self.in_datatype = None

        self.stopped = False
        self.input = None
        self.output = None

        # Tile format
        self.tilesize = 256
        self.tiledriver = None
        self.tileext = None
        self.tianditu = True
        self.storage_config = None
        self.lerc = False
        self.tempdir = None
        self.storage_service = None
        self.out_proj = None

        self.overwrite = None
        self.onlylerc = False


        # Should we read bigger window of the input raster and scale it down?
        # Note: Modified later by open_input()
        # Not for 'near' resampling
        # Not for Wavelet based drivers (JPEG2000, ECW, MrSID)
        # Not for 'raster' profile
        self.scaledquery = True
        # How big should be query window be for scaling down
        # Later on reset according the chosen resampling algorightm
        self.querysize = 4 * self.tilesize

        # Should we use Read on the input file for generating overview tiles?
        # Note: Modified later by open_input()
        # Otherwise the overview tiles are generated from existing underlying tiles
        self.overviewquery = False

        # RUN THE ARGUMENT PARSER:

        self.optparse_init()
        self.options, self.args = self.parser.parse_args(args=arguments)
        if not self.args:
            self.error("No input file specified")


        # POSTPROCESSING OF PARSED ARGUMENTS:

        # Workaround for old versions of GDAL
        try:
            if ((self.options.verbose and self.options.resampling == 'near') or
                    gdal.TermProgress_nocb):
                pass
        except Exception:
            self.error("This version of GDAL is not supported. Please upgrade to 1.6+.")

        # Is output directory the last argument?

        # Test output directory, if it doesn't exist
        if (os.path.isdir(self.args[-1]) or
                (len(self.args) > 1 and not os.path.exists(self.args[-1]))):
            self.output = self.args[-1]
            self.args = self.args[:-1]

        # More files on the input not directly supported yet

        if (len(self.args) > 1):
            self.error("Processing of several input files is not supported.",
                       "Please first use a tool like gdal_vrtmerge.py or gdal_merge.py on the "
                       "files: gdal_vrtmerge.py -o merged.vrt %s" % " ".join(self.args))

        self.input = self.args[0]

        # Default values for not given options

        if not self.output:
            # Directory with input filename without extension in actual directory
            self.output = os.path.splitext(os.path.basename(self.input))[0]


        # Supported options

        self.resampling = None

        if self.options.resampling == 'average':
            try:
                if gdal.RegenerateOverview:
                    pass
            except Exception:
                self.error("'average' resampling algorithm is not available.",
                           "Please use -r 'near' argument or upgrade to newer version of GDAL.")

        elif self.options.resampling == 'antialias':
            try:
                if numpy:     # pylint:disable=W0125
                    pass
            except Exception:
                self.error("'antialias' resampling algorithm is not available.",
                           "Install PIL (Python Imaging Library) and numpy.")

        elif self.options.resampling == 'near':
            self.resampling = gdal.GRA_NearestNeighbour
            self.querysize = self.tilesize

        elif self.options.resampling == 'bilinear':
            self.resampling = gdal.GRA_Bilinear
            self.querysize = self.tilesize * 2

        elif self.options.resampling == 'cubic':
            self.resampling = gdal.GRA_Cubic

        elif self.options.resampling == 'cubicspline':
            self.resampling = gdal.GRA_CubicSpline

        elif self.options.resampling == 'lanczos':
            self.resampling = gdal.GRA_Lanczos

        # User specified zoom levels
        self.tminz = None
        self.tmaxz = None
        if self.options.zoom:
            minmax = self.options.zoom.split('-', 1)
            minmax.extend([''])
            zoom_min, zoom_max = minmax[:2]
            self.tminz = int(zoom_min)
            if zoom_max:
                self.tmaxz = int(zoom_max)
            else:
                self.tmaxz = int(zoom_min)

        if self.options.profile == "tianditu":
            self.tianditu = True
            self.epsg = "EPSG:4490"
        else:
            self.tianditu = False

        # tile format
        if self.options.format == "PNG":
            self.tiledriver = "PNG"
            self.tileext = "png"
        elif self.options.format == "GTiff":
            self.tiledriver = "GTiff"
            self.tileext = "tif"
        elif self.options.format == "Lerc":
            self.tiledriver = "GTiff"
            self.tileext = "tif"
            self.lerc = True
        if self.tianditu:
            self.tempdir = os.path.join(self.output, str(uuid4()))
            os.makedirs(self.tempdir, exist_ok=True)


        # Overwrite mode uploading tile file to storage.
        if self.options.overwrite == "skip":
            self.overwrite = 0
        elif self.options.overwrite == "overwrite":
            self.overwrite = 1
        else:
            self.overwrite = 2

        if self.options.onlylerc:
            self.onlylerc = True

        # Check if the input filename is full ascii or not
        try:
            os.path.basename(self.input).encode('ascii')
        except UnicodeEncodeError:
            full_ascii = False
        else:
            full_ascii = True

        # LC_CTYPE check
        if not full_ascii and 'UTF-8' not in os.environ.get("LC_CTYPE", ""):
            if not self.options.quiet:
                print("\nWARNING: "
                      "You are running raster2tiles.py with a LC_CTYPE environment variable that is "
                      "not UTF-8 compatible, and your input file contains non-ascii characters. "
                      "The generated sample googlemaps, openlayers or "
                      "leaflet files might contain some invalid characters as a result\n")

        # Check the availability of cloud storage
        if self.options.cs_config is not None:
            if self.options.bucket is None or self.options.prefix is None:
                raise Exception(
                    "The bucket name or prefix of cloud storage must not be None!")
            else:
                self.bucket = self.options.bucket
                self.tiler_prefix = self.options.prefix

            cs_config = self.options.cs_config
            if not os.path.exists(self.options.cs_config):
                raise Exception(
                    "The '%s' cloud storage connfigure file was not found!",
                    self.options.cs_config)
            with open(cs_config) as cs_f:
                config = json.load(cs_f)
            self.storage_service: StorageService = create_service_from_config(
                config
            )

            if self.storage_service is None:
                raise Exception(
                    "Cloud storage service create failed!")
            if self.storage_service.get_bucket(self.bucket) is None:
                raise Exception(
                    "Get storage bucket: %s failed!" % self.bucket)

        # Output the results
        if self.options.verbose:
            print("Options:", self.options)
            print("Input:", self.input)
            print("Output:", self.output)
            print("Cache: %s MB" % (gdal.GetCacheMax() / 1024 / 1024))
            print('')

    def optparse_from_config(self):
        pass

    def optparse_init(self):
        """Prepare the option parser for input (argv)"""

        from optparse import OptionParser
        from optparse import OptionGroup
        usage = "Usage: %prog [options] input_file(s) [output]"
        p = OptionParser(usage, version="%prog " + __version__)
        p.add_option("-p", "--profile", dest='profile',
                     type='choice', choices=profile_list,
                     help=("Tile cutting profile (%s) - default 'mercator' "
                           "(Google Maps compatible)" % ",".join(profile_list)))
        p.add_option("-r", "--resampling", dest="resampling",
                     type='choice', choices=resampling_list,
                     help="Resampling method (%s) - default 'average'" % ",".join(resampling_list))
        p.add_option('-s', '--s_srs', dest="s_srs", metavar="SRS",
                     help="The spatial reference system used for the source input data")
        p.add_option('-z', '--zoom', dest="zoom",
                     help="Zoom levels to render (format:'2-5' or '10').")
        p.add_option('-e', '--resume', dest="resume", action="store_true",
                     help="Resume mode. Generate only missing files.")
        p.add_option('-a', '--srcnodata', dest="srcnodata", metavar="NODATA",
                     help="NODATA transparency value to assign to the input data")
        p.add_option('-d', '--tmscompatible', dest="tmscompatible", action="store_true",
                     help=("When using the geodetic profile, specifies the base resolution "
                           "as 0.703125 or 2 tiles at zoom level 0."))
        p.add_option("-v", "--verbose",
                     action="store_true", dest="verbose",
                     help="Print status messages to stdout")
        p.add_option("-q", "--quiet",
                     action="store_true", dest="quiet",
                     help="Disable messages and status to stdout")
        p.add_option("-f", "--format", dest="format",
                     type='choice', choices=format_list,
                     help=("Output tile format (%s) -default 'PNG' " % ",".join(format_list)))

        # cloud storage options
        g = OptionGroup(p, "Cloud Storage (s3、oss or obs )options",
                        "Options for upload tile file to cloud storage.")
        g.add_option("-c", "--storage-config", dest='cs_config',
                     help=("Cloud storage configure file! A json file that records "
                           "the cloud storage configuration. "))
        g.add_option("-b", "--bucket", dest='bucket',
                     help="Bucket name of cloud storage.")
        g.add_option("-x", "--prefix", dest='prefix',
                     help="Prefix name of cloud storage.")
        g.add_option("-t", "--access", dest='access', type='choice',
                     choices=access_list,
                     help="Access type of cloud storage (%s) - default 'private'."
                          % ",".join(access_list))
        g.add_option("-o", "--overwrite", dest='overwrite', type='choice',
                     choices=overwrite_list,
                     help="Overwrite mode of tile files (%s) - default 'overwrite'."
                     % ",".join(overwrite_list))
        g.add_option("-l", "--onlylerc", dest="onlylerc", action="store_true",
                     help="Upload lerc tile files only")
        p.add_option_group(g)

        p.set_defaults(verbose=False, profile="mercator",
                       webviewer='all', copyright='',
                       resampling='average', resume=False,
                       format='PNG',
                       access='private',
                       overwrite='overwrite',
                       onlylerc=False,
                       googlekey='INSERT_YOUR_KEY_HERE',
                       bingkey='INSERT_YOUR_KEY_HERE')

        self.parser = p

    # -------------------------------------------------------------------------
    def open_input(self):
        """Initialization of the input raster, reprojection if necessary"""
        gdal.AllRegister()

        self.out_drv = gdal.GetDriverByName(self.tiledriver)
        self.mem_drv = gdal.GetDriverByName('MEM')

        if not self.out_drv:
            raise Exception("The '%s' driver was not found, is it available in this GDAL build?",
                            self.tiledriver)
        if not self.mem_drv:
            raise Exception("The 'MEM' driver was not found, is it available in this GDAL build?")

        # Open the input file

        if self.input:
            self.in_ds = gdal.Open(self.input, gdal.GA_ReadOnly)
        else:
            raise Exception("No input file was specified")

        if self.options.verbose:
            print("Input file:",
                  "( %sP x %sL - %s bands)" % (self.in_ds.RasterXSize, self.in_ds.RasterYSize,
                                               self.in_ds.RasterCount))

        if not self.in_ds:
            # Note: GDAL prints the ERROR message too
            self.error("It is not possible to open the input file '%s'." % self.input)

        # Read metadata from the input file
        if self.in_ds.RasterCount == 0:
            self.error("Input file '%s' has no raster band" % self.input)

        if self.lerc and self.in_ds.RasterCount != 1:
            self.error("Input file '%s' must has 1 band when Lerc format is set." % self.input)

        if self.in_ds.GetRasterBand(1).GetRasterColorTable() and self.options.format == "PNG":
            self.error("Please convert this file to RGB/RGBA and run gdal2tiles on the result.",
                       "From paletted file you can create RGBA file (temp.vrt) by:\n"
                       "gdal_translate -of vrt -expand rgba %s temp.vrt\n"
                       "then run:\n"
                       "gdal2tiles temp.vrt" % self.input)

        self.in_datatype = self.in_ds.GetRasterBand(1).DataType

        # Get NODATA value
        in_nodata = []
        for i in range(1, self.in_ds.RasterCount+1):
            if self.in_ds.GetRasterBand(i).GetNoDataValue() is not None:
                in_nodata.append(self.in_ds.GetRasterBand(i).GetNoDataValue())
        if self.options.srcnodata:
            nds = list(map(float, self.options.srcnodata.split(',')))
            if len(nds) < self.in_ds.RasterCount:
                in_nodata = (nds * self.in_ds.RasterCount)[:self.in_ds.RasterCount]
            else:
                in_nodata = nds
        print(in_nodata)
        self.out_nodata = in_nodata

        if self.options.verbose:
            print("NODATA: %s" % in_nodata)

        if self.options.verbose:
            print("Preprocessed file:",
                  "( %sP x %sL - %s bands)" % (self.in_ds.RasterXSize, self.in_ds.RasterYSize,
                                               self.in_ds.RasterCount))

        in_srs = None

        if self.options.s_srs:
            in_srs = osr.SpatialReference()
            in_srs.SetFromUserInput(self.options.s_srs)
            in_srs_wkt = in_srs.ExportToWkt()
        else:
            in_srs_wkt = self.in_ds.GetProjection()
            if not in_srs_wkt and self.in_ds.GetGCPCount() != 0:
                in_srs_wkt = self.in_ds.GetGCPProjection()
            if in_srs_wkt:
                in_srs = osr.SpatialReference()
                in_srs.ImportFromWkt(in_srs_wkt)

        self.out_srs = osr.SpatialReference()

        if self.options.profile == 'mercator':
            self.out_srs.ImportFromEPSG(3857)
        elif self.options.profile == 'geodetic':
            self.out_srs.ImportFromEPSG(4326)
        elif self.options.profile == 'tianditu':
            self.out_srs.ImportFromEPSG(4490)
        else:
            self.out_srs = in_srs

        # Are the reference systems the same? Reproject if necessary.

        self.out_ds = None

        if self.options.profile in ('mercator', 'geodetic', 'tianditu'):

            if ((self.in_ds.GetGeoTransform() == (0.0, 1.0, 0.0, 0.0, 0.0, 1.0)) and
                    (self.in_ds.GetGCPCount() == 0)):
                self.error("There is no georeference - neither affine transformation (worldfile) "
                           "nor GCPs. You can generate only 'raster' profile tiles.",
                           "Either gdal2tiles with parameter -p 'raster' or use another GIS "
                           "software for georeference e.g. gdal_transform -gcp / -a_ullr / -a_srs")

            if in_srs:
                if ((in_srs.ExportToProj4() != self.out_srs.ExportToProj4()) or
                        (self.in_ds.GetGCPCount() != 0)):
                    # Generation of VRT dataset in tile projection,
                    # default 'nearest neighbour' warping
                    self.out_ds = gdal.AutoCreateWarpedVRT(
                        self.in_ds, in_srs_wkt, self.out_srs.ExportToWkt())

                    if self.options.verbose:
                        print("Warping of the raster by AutoCreateWarpedVRT "
                              "(result saved into 'tiles.vrt')")
                        self.out_ds.GetDriver().CreateCopy("tiles.vrt", self.out_ds)

                    # Correction of AutoCreateWarpedVRT for NODATA values
                    if in_nodata != []:
                        tempfilename = self.gettempfilename('-gdal2tiles.vrt')
                        self.out_ds.GetDriver().CreateCopy(tempfilename, self.out_ds)
                        # open as a text file
                        s = open(tempfilename).read()
                        # Add the warping options
                        s = s.replace(
                            "<GDALWarpOptions>",
                            """
    <GDALWarpOptions>
      <Option name="INIT_DEST">NO_DATA</Option>
      <Option name="UNIFIED_SRC_NODATA">YES</Option>
                            """)
                        # replace BandMapping tag for NODATA bands....
                        for i in range(len(in_nodata)):
                            s = s.replace(
                                '<BandMapping src="%i" dst="%i"/>' % ((i+1), (i+1)),
                                """
        <BandMapping src="%i" dst="%i">
          <SrcNoDataReal>%i</SrcNoDataReal>
          <SrcNoDataImag>0</SrcNoDataImag>
          <DstNoDataReal>%i</DstNoDataReal>
          <DstNoDataImag>0</DstNoDataImag>
        </BandMapping>
                                """ % ((i+1), (i+1), in_nodata[i], in_nodata[i]))
                        # save the corrected VRT
                        open(tempfilename, "w").write(s)
                        # open by GDAL as self.out_ds
                        self.out_ds = gdal.Open(tempfilename)
                        # delete the temporary file
                        os.unlink(tempfilename)

                        # set NODATA_VALUE metadata
                        self.out_ds.SetMetadataItem(
                            'NODATA_VALUES', ' '.join([str(i) for i in in_nodata]))

                        if self.options.verbose:
                            print("Modified warping result saved into 'tiles1.vrt'")
                            open("tiles1.vrt", "w").write(s)

                    # Correction of AutoCreateWarpedVRT for Mono (1 band) and RGB (3 bands) files
                    # without NODATA:
                    # equivalent of gdalwarp -dstalpha
                    if in_nodata == [] and self.out_ds.RasterCount in [1, 3]:
                        tempfilename = self.gettempfilename('-gdal2tiles.vrt')
                        self.out_ds.GetDriver().CreateCopy(tempfilename, self.out_ds)
                        # open as a text file
                        s = open(tempfilename).read()
                        # Add the warping options
                        s = s.replace(
                            "<BlockXSize>",
                            """
  <VRTRasterBand dataType="Byte" band="%i" subClass="VRTWarpedRasterBand">
    <ColorInterp>Alpha</ColorInterp>
  </VRTRasterBand>
  <BlockXSize>
                            """ % (self.out_ds.RasterCount + 1))
                        s = s.replace(
                            "</GDALWarpOptions>",
                            """
    <DstAlphaBand>%i</DstAlphaBand>
  </GDALWarpOptions>
                            """ % (self.out_ds.RasterCount + 1))
                        s = s.replace(
                            "</WorkingDataType>",
                            """
    </WorkingDataType>
    <Option name="INIT_DEST">0</Option>
                            """)
                        # save the corrected VRT
                        open(tempfilename, "w").write(s)
                        # open by GDAL as self.out_ds
                        self.out_ds = gdal.Open(tempfilename)
                        # delete the temporary file
                        os.unlink(tempfilename)

                        if self.options.verbose:
                            print("Modified -dstalpha warping result saved into 'tiles1.vrt'")
                            open("tiles1.vrt", "w").write(s)
                    s = '''
                    '''

            else:
                self.error("Input file has unknown SRS.",
                           "Use --s_srs ESPG:xyz (or similar) to provide source reference system.")

            if self.out_ds and self.options.verbose:
                print("Projected file:", "tiles.vrt", "( %sP x %sL - %s bands)" % (
                    self.out_ds.RasterXSize, self.out_ds.RasterYSize, self.out_ds.RasterCount))

        if not self.out_ds:
            self.out_ds = self.in_ds

        #
        # Here we should have a raster (out_ds) in the correct Spatial Reference system
        #

        if self.options.format in ("PNG", "JPG"):
            # Get alpha band (either directly or from NODATA value)
            self.alphaband = self.out_ds.GetRasterBand(1).GetMaskBand()
            if ((self.alphaband.GetMaskFlags() & gdal.GMF_ALPHA) or
                    self.out_ds.RasterCount == 4 or
                    self.out_ds.RasterCount == 2):
                self.dataBandsCount = self.out_ds.RasterCount - 1
            else:
                self.dataBandsCount = self.out_ds.RasterCount
        else:
            self.dataBandsCount = self.out_ds.RasterCount

        # Read the georeference
        self.out_gt = self.out_ds.GetGeoTransform()

        self.out_proj = self.out_ds.GetProjection()

        # Test the size of the pixel

        # Report error in case rotation/skew is in geotransform (possible only in 'raster' profile)
        if (self.out_gt[2], self.out_gt[4]) != (0, 0):
            self.error("Georeference of the raster contains rotation or skew. "
                       "Such raster is not supported. Please use gdalwarp first.")

        # Here we expect: pixel is square, no rotation on the raster

        # Output Bounds - coordinates in the output SRS
        self.ominx = self.out_gt[0]
        self.omaxx = self.out_gt[0] + self.out_ds.RasterXSize * self.out_gt[1]
        self.omaxy = self.out_gt[3]
        self.ominy = self.out_gt[3] - self.out_ds.RasterYSize * self.out_gt[1]
        # Note: maybe round(x, 14) to avoid the gdal_translate behaviour, when 0 becomes -1e-15

        if self.options.verbose:
            print("Bounds (output srs):", round(self.ominx, 13), self.ominy, self.omaxx, self.omaxy)

        # Calculating ranges for tiles in different zoom levels
        if self.options.profile == 'mercator':

            self.mercator = GlobalMercator()

            # Function which generates SWNE in LatLong for given tile
            self.tileswne = self.mercator.TileLatLonBounds

            # Generate table with min max tile coordinates for all zoomlevels
            self.tminmax = list(range(0, 32))
            for tz in range(0, 32):
                tminx, tminy = self.mercator.MetersToTile(self.ominx, self.ominy, tz)
                tmaxx, tmaxy = self.mercator.MetersToTile(self.omaxx, self.omaxy, tz)
                # crop tiles extending world limits (+-180,+-90)
                tminx, tminy = max(0, tminx), max(0, tminy)
                tmaxx, tmaxy = min(2**tz-1, tmaxx), min(2**tz-1, tmaxy)
                self.tminmax[tz] = (tminx, tminy, tmaxx, tmaxy)

            # TODO: Maps crossing 180E (Alaska?)

            # Get the minimal zoom level (map covers area equivalent to one tile)
            if self.tminz is None:
                self.tminz = self.mercator.ZoomForPixelSize(
                    self.out_gt[1] * max(self.out_ds.RasterXSize,
                                         self.out_ds.RasterYSize) / float(self.tilesize))

            # Get the maximal zoom level
            # (closest possible zoom level up on the resolution of raster)
            if self.tmaxz is None:
                self.tmaxz = self.mercator.ZoomForPixelSize(self.out_gt[1])

            if self.options.verbose:
                print("Bounds (latlong):",
                      self.mercator.MetersToLatLon(self.ominx, self.ominy),
                      self.mercator.MetersToLatLon(self.omaxx, self.omaxy))
                print('MinZoomLevel:', self.tminz)
                print("MaxZoomLevel:",
                      self.tmaxz,
                      "(",
                      self.mercator.Resolution(self.tmaxz),
                      ")")

        if self.options.profile in ('geodetic', 'tianditu'):
            self.geodetic = GlobalGeodetic(self.options.tmscompatible)

            # Function which generates SWNE in LatLong for given tile
            self.tileswne = self.geodetic.TileLatLonBounds

            # Generate table with min max tile coordinates for all zoomlevels
            self.tminmax = list(range(0, 32))
            for tz in range(0, 32):
                tminx, tminy = self.geodetic.LonLatToTile(self.ominx, self.ominy, tz)
                tmaxx, tmaxy = self.geodetic.LonLatToTile(self.omaxx, self.omaxy, tz)

                # crop tiles extending world limits (+-180,+-90)
                tminx, tminy = max(0, tminx), max(0, tminy)
                tmaxx, tmaxy = min(2**(tz+1)-1, tmaxx), min(2**tz-1, tmaxy)
                self.tminmax[tz] = (tminx, tminy, tmaxx, tmaxy)

            # TODO: Maps crossing 180E (Alaska?)

            # Get the maximal zoom level
            # (closest possible zoom level up on the resolution of raster)
            if self.tminz is None:
                self.tminz = self.geodetic.ZoomForPixelSize(
                    self.out_gt[1] * max(self.out_ds.RasterXSize,
                                         self.out_ds.RasterYSize) / float(self.tilesize))

            # Get the maximal zoom level
            # (closest possible zoom level up on the resolution of raster)
            if self.tmaxz is None:
                self.tmaxz = self.geodetic.ZoomForPixelSize(self.out_gt[1])

            if self.options.verbose:
                print("Bounds (latlong):", self.ominx, self.ominy, self.omaxx, self.omaxy)

        if self.options.profile == 'raster':

            def log2(x):
                return math.log10(x) / math.log10(2)

            self.nativezoom = int(
                max(math.ceil(log2(self.out_ds.RasterXSize/float(self.tilesize))),
                    math.ceil(log2(self.out_ds.RasterYSize/float(self.tilesize)))))

            if self.options.verbose:
                print("Native zoom of the raster:", self.nativezoom)

            # Get the minimal zoom level (whole raster in one tile)
            if self.tminz is None:
                self.tminz = 0

            # Get the maximal zoom level (native resolution of the raster)
            if self.tmaxz is None:
                self.tmaxz = self.nativezoom

            # Generate table with min max tile coordinates for all zoomlevels
            self.tminmax = list(range(0, self.tmaxz+1))
            self.tsize = list(range(0, self.tmaxz+1))
            for tz in range(0, self.tmaxz+1):
                tsize = 2.0**(self.nativezoom-tz)*self.tilesize
                tminx, tminy = 0, 0
                tmaxx = int(math.ceil(self.out_ds.RasterXSize / tsize)) - 1
                tmaxy = int(math.ceil(self.out_ds.RasterYSize / tsize)) - 1
                self.tsize[tz] = math.ceil(tsize)
                self.tminmax[tz] = (tminx, tminy, tmaxx, tmaxy)


    def generate_base_tiles(self):
        """
        Generation of the base tiles (the lowest in the pyramid) directly from the input raster
        """

        if not self.options.quiet:
            print("Generating Base Tiles:")

        if self.options.verbose:
            print('')
            print("Tiles generated from the max zoom level:")
            print("----------------------------------------")
            print('')

        # Set the bounds
        tminx, tminy, tmaxx, tmaxy = self.tminmax[self.tmaxz]

        ds = self.out_ds

        if self.options.format in ("PNG", 'JPEG'):
            tilebands = self.dataBandsCount + 1
        else:
            tilebands = self.dataBandsCount

        querysize = self.querysize

        if self.options.verbose:
            print("dataBandsCount: ", self.dataBandsCount)
            print("tilebands: ", tilebands)

        tcount = (1+abs(tmaxx-tminx)) * (1+abs(tmaxy-tminy))
        ti = 0

        tz = self.tmaxz
        if self.options.format in ("PNG", "JPEG"):
            for ty in range(tmaxy, tminy-1, -1):
                for tx in range(tminx, tmaxx+1):

                    if self.stopped:
                        break
                    ti += 1

                    tf_ty = ty
                    if self.tianditu:
                        # convert ty value from TMS to tianditu tile style
                        tf_ty = int(math.pow(2, (tz -1)) - 1 - ty)

                    tilefilename = os.path.join(
                        self.output, str(tz), str(tx), "%s.%s" % (ty, self.tileext))

                    # cloud storage tile file name
                    if self.storage_service is not None:
                        cs_tilefilename = os.path.join(
                            self.options.prefix,
                            str(tz),
                            str(tx),
                            "%s.%s" % (tf_ty, self.tileext)
                        )

                    if self.options.verbose:
                        print(ti, '/', tcount, tilefilename)

                    if self.options.resume and os.path.exists(tilefilename):
                        if self.options.verbose:
                            print("Tile generation skipped because of --resume")
                        else:
                            self.progressbar(ti / float(tcount))
                        continue

                    # Create directories for the tile
                    if not os.path.exists(os.path.dirname(tilefilename)):
                        os.makedirs(os.path.dirname(tilefilename))

                    if self.options.profile == 'mercator':
                        # Tile bounds in EPSG:3857
                        b = self.mercator.TileBounds(tx, ty, tz)
                    elif self.options.profile in ('geodetic', 'tianditu'):
                        b = self.geodetic.TileBounds(tx, ty, tz)

                    # Don't scale up by nearest neighbour, better change the querysize
                    # to the native resolution (and return smaller query tile) for scaling

                    if self.options.profile in ('mercator', 'geodetic', 'tianditu'):
                        rb, wb = self.geo_query(ds, b[0], b[3], b[2], b[1])

                        # Pixel size in the raster covering query geo extent
                        nativesize = wb[0] + wb[2]
                        if self.options.verbose:
                            print("\tNative Extent (querysize", nativesize, "): ", rb, wb)

                        # Tile bounds in raster coordinates for ReadRaster query
                        rb, wb = self.geo_query(ds, b[0], b[3], b[2], b[1], querysize=querysize)

                        rx, ry, rxsize, rysize = rb
                        wx, wy, wxsize, wysize = wb

                    else:     # 'raster' profile:

                        tsize = int(self.tsize[tz])   # tilesize in raster coordinates for actual zoom
                        xsize = self.out_ds.RasterXSize     # size of the raster in pixels
                        ysize = self.out_ds.RasterYSize
                        if tz >= self.nativezoom:
                            querysize = self.tilesize

                        rx = (tx) * tsize
                        rxsize = 0
                        if tx == tmaxx:
                            rxsize = xsize % tsize
                        if rxsize == 0:
                            rxsize = tsize

                        rysize = 0
                        if ty == tmaxy:
                            rysize = ysize % tsize
                        if rysize == 0:
                            rysize = tsize
                        ry = ysize - (ty * tsize) - rysize

                        wx, wy = 0, 0
                        wxsize = int(rxsize/float(tsize) * self.tilesize)
                        wysize = int(rysize/float(tsize) * self.tilesize)
                        if wysize != self.tilesize:
                            wy = self.tilesize - wysize

                    if self.options.verbose:
                        print("\tReadRaster Extent: ",
                              (rx, ry, rxsize, rysize), (wx, wy, wxsize, wysize))

                    # Query is in 'nearest neighbour' but can be bigger in then the tilesize
                    # We scale down the query to the tilesize by supplied algorithm.

                    # Tile dataset in memory
                    dstile = self.mem_drv.Create('', self.tilesize, self.tilesize, tilebands)

                    data = alpha = None
                    # Read the source raster if anything is going inside the tile as per the computed
                    # geo_query
                    if rxsize != 0 and rysize != 0 and wxsize != 0 and wysize != 0:
                        data = ds.ReadRaster(rx, ry, rxsize, rysize, wxsize, wysize,
                                             band_list=list(range(1, self.dataBandsCount+1)))
                        alpha = self.alphaband.ReadRaster(rx, ry, rxsize, rysize, wxsize, wysize)

                    # The tile in memory is a transparent file by default. Write pixel values into it if
                    # any
                    if data:
                        if self.tilesize == querysize:
                            # Use the ReadRaster result directly in tiles ('nearest neighbour' query)
                            dstile.WriteRaster(wx, wy, wxsize, wysize, data,
                                               band_list=list(range(1, self.dataBandsCount+1)))
                            dstile.WriteRaster(wx, wy, wxsize, wysize, alpha, band_list=[tilebands])

                            # Note: For source drivers based on WaveLet compression (JPEG2000, ECW,
                            # MrSID) the ReadRaster function returns high-quality raster (not ugly
                            # nearest neighbour)
                            # TODO: Use directly 'near' for WaveLet files
                        else:
                            # Big ReadRaster query in memory scaled to the tilesize - all but 'near'
                            # algo
                            dsquery = self.mem_drv.Create('', querysize, querysize, tilebands)
                            # TODO: fill the null value in case a tile without alpha is produced (now
                            # only png tiles are supported)
                            dsquery.WriteRaster(wx, wy, wxsize, wysize, data,
                                                band_list=list(range(1, self.dataBandsCount+1)))
                            dsquery.WriteRaster(wx, wy, wxsize, wysize, alpha, band_list=[tilebands])

                            self.scale_query_to_tile(dsquery, dstile, tilefilename)
                            del dsquery

                    del data

                    if self.options.resampling != 'antialias':
                        # Write a copy of tile to png/jpg
                        self.out_drv.CreateCopy(tilefilename, dstile, strict=0)
                    del dstile

                    if self.storage_service is not None:
                        if os.path.exists(tilefilename):
                            try:
                                if self.options.verbose:
                                    print('Uploading tile tile %s to cloud storage.' % cs_tilefilename)
                                print(self.options.bucket)
                                print(cs_tilefilename)
                                print(tilefilename)
                                print(self.options.access)
                                self.storage_service.upload_file(
                                    self.options.bucket,
                                    cs_tilefilename,
                                    tilefilename,
                                    self.options.access
                                )
                            except Exception as e:
                                self.error(e)

                    if not self.options.verbose and not self.options.quiet:
                        self.progressbar(ti / float(tcount))
        elif self.options.format in ("Lerc", "GTiff"):
            outdir = self.output
            tempdir = outdir
            os.makedirs(outdir, exist_ok=True)
            if self.tianditu:
                outdir = os.path.join(self.output, "tif")
                tempdir = self.tempdir
                os.makedirs(outdir, exist_ok=True)
                os.makedirs(tempdir, exist_ok=True)

            if self.overwrite == 0 and self.storage_service is not None:
                for ty in range(tmaxy, tminy - 1, -1):
                    for tx in range(tminx, tmaxx + 1):
                        tilename = str(ty) + ".lerc"
                        cs_tilename = os.path.join(
                            self.tiler_prefix,
                            str(tz),
                            str(tx),
                            tilename
                        )
                        if self.storage_service.exist(
                                self.bucket,
                                cs_tilename
                        ):
                            print(
                                'Tile %s in bucket %s already exists, skip...' %
                                (cs_tilename, self.bucket)
                            )
                            continue

            elif (self.overwrite == 1 or self.overwrite is None and
                self.storage_service is not None):
                for ty in range(tmaxy, tminy - 1, -1):
                    for tx in range(tminx, tmaxx + 1):

                        if self.stopped:
                            break
                        ti += 1

                        tilefilename = os.path.join(
                            tempdir, str(tz), str(tx),
                            "%s.%s" % (ty, "tif"))

                        if self.options.verbose:
                            print(ti, '/', tcount, tilefilename)

                        if self.options.resume and os.path.exists(tilefilename):
                            if self.options.verbose:
                                print(
                                    "Tile generation skipped because of --resume")
                            else:
                                self.progressbar(ti / float(tcount))
                            continue

                        # Create directories for the tile
                        if not os.path.exists(os.path.dirname(tilefilename)):
                            os.makedirs(os.path.dirname(tilefilename))

                        if self.options.profile == 'mercator':
                            # Tile bounds in EPSG:3857
                            b = self.mercator.TileBounds(tx, ty, tz)
                        elif self.options.profile in ('geodetic', 'tianditu'):
                            b = self.geodetic.TileBounds(tx, ty, tz)

                        # Don't scale up by nearest neighbour, better change the querysize
                        # to the native resolution (and return smaller query tile) for scaling

                        if self.options.profile in (
                        'mercator', 'geodetic', 'tianditu'):
                            rb, wb = self.geo_query(ds, b[0], b[3], b[2], b[1])

                            # Pixel size in the raster covering query geo extent
                            nativesize = wb[0] + wb[2]
                            if self.options.verbose:
                                print("\tNative Extent (querysize", nativesize,
                                      "): ", rb, wb)

                            # Tile bounds in raster coordinates for ReadRaster query
                            rb, wb = self.geo_query(ds, b[0], b[3], b[2], b[1],
                                                    querysize=querysize)

                            rx, ry, rxsize, rysize = rb
                            wx, wy, wxsize, wysize = wb

                        else:  # 'raster' profile:
                            tsize = int(self.tsize[
                                            tz])  # tilesize in raster coordinates for actual zoom
                            xsize = self.out_ds.RasterXSize  # size of the raster in pixels
                            ysize = self.out_ds.RasterYSize
                            if tz >= self.nativezoom:
                                querysize = self.tilesize

                            rx = (tx) * tsize
                            rxsize = 0
                            if tx == tmaxx:
                                rxsize = xsize % tsize
                            if rxsize == 0:
                                rxsize = tsize

                            rysize = 0
                            if ty == tmaxy:
                                rysize = ysize % tsize
                            if rysize == 0:
                                rysize = tsize
                            ry = ysize - (ty * tsize) - rysize

                            wx, wy = 0, 0
                            wxsize = int(rxsize / float(tsize) * self.tilesize)
                            wysize = int(rysize / float(tsize) * self.tilesize)
                            if wysize != self.tilesize:
                                wy = self.tilesize - wysize

                        if self.options.verbose:
                            print("\tReadRaster Extent: ",
                                  (rx, ry, rxsize, rysize),
                                  (wx, wy, wxsize, wysize))

                        # Tile dataset in memory
                        dstile = self.mem_drv.Create('',
                                                     self.tilesize,
                                                     self.tilesize,
                                                     tilebands,
                                                     self.in_datatype)

                        data = None
                        # Read the source raster if anything is going inside the tile as per the computed
                        # geo_query
                        if rxsize != 0 and rysize != 0 and wxsize != 0 and wysize != 0:
                            data = ds.ReadRaster(
                                rx, ry, rxsize, rysize, wxsize, wysize,
                                band_list=list(
                                    range(
                                        1,
                                        tilebands + 1
                                    )
                                )
                            )

                        if data:
                            if self.tilesize == querysize:
                                # Use the ReadRaster result directly in tiles ('nearest neighbour' query)
                                dstile.WriteRaster(
                                    wx, wy, wxsize, wysize, data,
                                    band_list=list(
                                        range(
                                            1,
                                            tilebands + 1
                                        )
                                    )
                                )
                                dstile.SetGeoTransform(
                                    self.geodetic.tile_geo_transform(tx, ty, tz)
                                )
                                dstile.SetProjection(self.out_proj)
                                dstile.SetMetadataItem(
                                    'NODATA_VALUES',
                                    ' '.join(
                                        [str(i) for i in self.out_nodata]
                                    )
                                )

                                # Note: For source drivers based on WaveLet compression (JPEG2000, ECW,
                                # MrSID) the ReadRaster function returns high-quality raster (not ugly
                                # nearest neighbour)
                                # TODO: Use directly 'near' for WaveLet files
                            else:
                                # Big ReadRaster query in memory scaled to the tilesize - all but 'near'
                                # algo
                                dsquery = self.mem_drv.Create(
                                    '',
                                    querysize,
                                    querysize,
                                    tilebands,
                                    self.in_datatype
                                )

                                dsquery.WriteRaster(wx, wy, wxsize, wysize,
                                                    data,
                                                    band_list=list(range(1,
                                                                         tilebands + 1)))

                                dsquery.SetProjection(self.out_proj)
                                dsquery.SetMetadataItem(
                                    'NODATA_VALUES',
                                    ' '.join(
                                        [str(i) for i in self.out_nodata]
                                    )
                                )

                                self.scale_query_to_tile(dsquery, dstile,
                                                         tilefilename)
                                del dsquery

                        del data

                        if self.options.resampling != 'antialias':
                            # Write a copy of tile to GTiff
                            self.out_drv.CreateCopy(
                                tilefilename,
                                dstile,
                                strict=0
                            )
                        del dstile

                        if self.tianditu:
                            # convert ty value from TMS to tianditu tile style
                            tf_ty = int(math.pow(2, (tz - 1)) - 1 - ty)
                            tdt_tilefilename = os.path.join(
                                outdir, str(tz), str(tx),
                                "%s.%s" % (tf_ty, "tif")
                            )

                            if os.path.exists(tilefilename):
                                tdt_dir = os.path.dirname(tdt_tilefilename)
                                os.makedirs(tdt_dir, exist_ok=True)
                                shutil.copy(tilefilename, tdt_tilefilename)

                        if not self.options.verbose and not self.options.quiet:
                            self.progressbar(ti / float(tcount))

            # todo overwrite mode to cloud storage
            elif (self.overwrite == 2 and self.storage_service is not None):
                pass
                # if self.onlylerc:
                #     lercprefix = self.options.prefix
                #     tifprefix = self.options.prefix
                # else:
                #     lercprefix = os.path.join(self.options.prefix, "lerc")
                #     tifprefix = os.path.join(self.options.prefix, "tif")
                #


    def generate_overview_tiles(self):
        """Generation of the overview tiles (higher in the pyramid) based on existing tiles"""

        if not self.options.quiet:
            print("Generating Overview Tiles:")

        if self.options.format in ("PNG", 'JPEG'):
            tilebands = self.dataBandsCount + 1
        else:
            tilebands = self.dataBandsCount

        # Usage of existing tiles: from 4 underlying tiles generate one as overview.

        tcount = 0
        for tz in range(self.tmaxz-1, self.tminz-1, -1):
            tminx, tminy, tmaxx, tmaxy = self.tminmax[tz]
            tcount += (1+abs(tmaxx-tminx)) * (1+abs(tmaxy-tminy))

        ti = 0

        if self.options.format in ("PNG", "JPEG"):
            for tz in range(self.tmaxz-1, self.tminz-1, -1):
                tminx, tminy, tmaxx, tmaxy = self.tminmax[tz]
                for ty in range(tmaxy, tminy-1, -1):
                    for tx in range(tminx, tmaxx+1):

                        if self.stopped:
                            break

                        ti += 1
                        tf_ty = ty
                        if self.tianditu:
                            # convert ty value from TMS to tianditu tile style
                            tf_ty = int(math.pow(2, (tz - 1)) - 1 - ty)

                        tilefilename = os.path.join(
                            self.output, str(tz), str(tx),
                            "%s.%s" % (ty, self.tileext))

                        # cloud storage tile file name
                        if self.storage_service is not None:
                            cs_tilefilename = os.path.join(
                                self.options.prefix,
                                str(tz),
                                str(tx),
                                "%s.%s" % (tf_ty, self.tileext)
                            )

                        if self.options.verbose:
                            print(ti, '/', tcount, tilefilename)

                        if self.options.resume and os.path.exists(tilefilename):
                            if self.options.verbose:
                                print("Tile generation skipped because of --resume")
                            else:
                                self.progressbar(ti / float(tcount))
                            continue

                        # Create directories for the tile
                        if not os.path.exists(os.path.dirname(tilefilename)):
                            os.makedirs(os.path.dirname(tilefilename))

                        dsquery = self.mem_drv.Create('', 2*self.tilesize, 2*self.tilesize, tilebands)
                        # TODO: fill the null value
                        dstile = self.mem_drv.Create('', self.tilesize, self.tilesize, tilebands)

                        # TODO: Implement more clever walking on the tiles with cache functionality
                        # probably walk should start with reading of four tiles from top left corner
                        # Hilbert curve

                        children = []
                        # Read the tiles and write them to query window
                        for y in range(2*ty, 2*ty+2):
                            for x in range(2*tx, 2*tx+2):
                                minx, miny, maxx, maxy = self.tminmax[tz+1]
                                if x >= minx and x <= maxx and y >= miny and y <= maxy:
                                    dsquerytile = gdal.Open(
                                        os.path.join(self.output, str(tz+1), str(x),
                                                     "%s.%s" % (y, self.tileext)),
                                        gdal.GA_ReadOnly)
                                    if (ty == 0 and y == 1) or (ty != 0 and (y % (2*ty)) != 0):
                                        tileposy = 0
                                    else:
                                        tileposy = self.tilesize
                                    if tx:
                                        tileposx = x % (2*tx) * self.tilesize
                                    elif tx == 0 and x == 1:
                                        tileposx = self.tilesize
                                    else:
                                        tileposx = 0
                                    dsquery.WriteRaster(
                                        tileposx, tileposy, self.tilesize, self.tilesize,
                                        dsquerytile.ReadRaster(0, 0, self.tilesize, self.tilesize),
                                        band_list=list(range(1, tilebands+1)))
                                    children.append([x, y, tz+1])

                        self.scale_query_to_tile(dsquery, dstile, tilefilename)
                        # Write a copy of tile to png/jpg
                        if self.options.resampling != 'antialias':
                            # Write a copy of tile to png/jpg
                            self.out_drv.CreateCopy(tilefilename, dstile, strict=0)
                        del dstile

                        if self.storage_service is not None:
                            if os.path.exists(tilefilename):
                                try:
                                    if self.options.verbose:
                                        print(
                                            'Uploading tile tile %s to cloud storage.' % cs_tilefilename)

                                    self.storage_service.upload_file(
                                        self.options.bucket,
                                        cs_tilefilename,
                                        tilefilename,
                                        self.options.access
                                    )
                                except Exception as e:
                                    self.error(e)
                                finally:
                                    os.remove(tilefilename)

                        if self.options.verbose:
                            print("\tbuild from zoom", tz+1,
                                  " tiles:", (2*tx, 2*ty), (2*tx+1, 2*ty),
                                  (2*tx, 2*ty+1), (2*tx+1, 2*ty+1))


                        if not self.options.verbose and not self.options.quiet:
                            self.progressbar(ti / float(tcount))
        elif self.options.format in ("Lerc", "GTiff"):
            outdir = self.output
            tempdir = outdir
            if self.tianditu:
                outdir = os.path.join(self.output, "tif")
                tempdir = self.tempdir

            for tz in range(self.tmaxz - 1, self.tminz - 1, -1):
                tminx, tminy, tmaxx, tmaxy = self.tminmax[tz]
                for ty in range(tmaxy, tminy - 1, -1):
                    for tx in range(tminx, tmaxx + 1):

                        if self.stopped:
                            break

                        ti += 1

                        tilefilename = os.path.join(
                            tempdir, str(tz), str(tx),
                            "%s.%s" % (ty, "tif"))

                        if self.options.verbose:
                            print(ti, '/', tcount, tilefilename)

                        if self.options.resume and os.path.exists(tilefilename):
                            if self.options.verbose:
                                print(
                                    "Tile generation skipped because of --resume")
                            else:
                                self.progressbar(ti / float(tcount))
                            continue

                        # Create directories for the tile
                        if not os.path.exists(os.path.dirname(tilefilename)):
                            os.makedirs(os.path.dirname(tilefilename))

                        dsquery = self.mem_drv.Create('', 2 * self.tilesize,
                                                      2 * self.tilesize,
                                                      tilebands,
                                                      self.in_datatype)
                        # TODO: fill the null value
                        dstile = self.mem_drv.Create('', self.tilesize,
                                                     self.tilesize, tilebands,
                                                     self.in_datatype)

                        # TODO: Implement more clever walking on the tiles with cache functionality
                        # probably walk should start with reading of four tiles from top left corner
                        # Hilbert curve

                        children = []
                        # Read the tiles and write them to query window
                        for y in range(2 * ty, 2 * ty + 2):
                            for x in range(2 * tx, 2 * tx + 2):
                                minx, miny, maxx, maxy = self.tminmax[tz + 1]
                                if x >= minx and x <= maxx and y >= miny and y <= maxy:
                                    dsquerytile = gdal.Open(
                                        os.path.join(tempdir, str(tz + 1),
                                                     str(x),
                                                     "%s.%s" % (
                                                     y, self.tileext)),
                                        gdal.GA_ReadOnly)
                                    if (ty == 0 and y == 1) or (
                                            ty != 0 and (y % (2 * ty)) != 0):
                                        tileposy = 0
                                    else:
                                        tileposy = self.tilesize
                                    if tx:
                                        tileposx = x % (2 * tx) * self.tilesize
                                    elif tx == 0 and x == 1:
                                        tileposx = self.tilesize
                                    else:
                                        tileposx = 0

                                    dsquery.WriteRaster(
                                        tileposx, tileposy, self.tilesize,
                                        self.tilesize,
                                        dsquerytile.ReadRaster(0, 0,
                                                               self.tilesize,
                                                               self.tilesize),
                                        band_list=list(range(1, tilebands + 1)))
                                    children.append([x, y, tz + 1])

                        self.scale_query_to_tile(dsquery, dstile, tilefilename)
                        # Write a copy of tile to png/jpg
                        if self.options.resampling != 'antialias':
                            # Write a copy of tile to png/jpg
                            self.out_drv.CreateCopy(tilefilename, dstile,
                                                    strict=0)
                        del dstile


                        if self.tianditu:
                            # convert ty value from TMS to tianditu tile style
                            tf_ty = int(math.pow(2, (tz - 1)) - 1 - ty)
                            tdt_tilefilename = os.path.join(
                                outdir, str(tz), str(tx),
                                "%s.%s" % (tf_ty, "tif")
                            )

                            if os.path.exists(tilefilename):
                                tdt_dir = os.path.dirname(tdt_tilefilename)
                                os.makedirs(tdt_dir, exist_ok=True)
                                shutil.copyfile(tilefilename, tdt_tilefilename)

                        if self.options.verbose:
                            print("\tbuild from zoom", tz + 1,
                                  " tiles:", (2 * tx, 2 * ty),
                                  (2 * tx + 1, 2 * ty),
                                  (2 * tx, 2 * ty + 1),
                                  (2 * tx + 1, 2 * ty + 1))

                        if not self.options.verbose and not self.options.quiet:
                            self.progressbar(ti / float(tcount))


    def geo_query(self, ds, ulx, uly, lrx, lry, querysize=0):
        """
        For given dataset and query in cartographic coordinates returns parameters for ReadRaster()
        in raster coordinates and x/y shifts (for border tiles). If the querysize is not given, the
        extent is returned in the native resolution of dataset ds.

        raises Gdal2TilesError if the dataset does not contain anything inside this geo_query
        """
        geotran = ds.GetGeoTransform()
        rx = int((ulx - geotran[0]) / geotran[1] + 0.001)
        ry = int((uly - geotran[3]) / geotran[5] + 0.001)
        rxsize = int((lrx - ulx) / geotran[1] + 0.5)
        rysize = int((lry - uly) / geotran[5] + 0.5)

        if not querysize:
            wxsize, wysize = rxsize, rysize
        else:
            wxsize, wysize = querysize, querysize

        # Coordinates should not go out of the bounds of the raster
        wx = 0
        if rx < 0:
            rxshift = abs(rx)
            wx = int(wxsize * (float(rxshift) / rxsize))
            wxsize = wxsize - wx
            rxsize = rxsize - int(rxsize * (float(rxshift) / rxsize))
            rx = 0
        if rx+rxsize > ds.RasterXSize:
            wxsize = int(wxsize * (float(ds.RasterXSize - rx) / rxsize))
            rxsize = ds.RasterXSize - rx

        wy = 0
        if ry < 0:
            ryshift = abs(ry)
            wy = int(wysize * (float(ryshift) / rysize))
            wysize = wysize - wy
            rysize = rysize - int(rysize * (float(ryshift) / rysize))
            ry = 0
        if ry+rysize > ds.RasterYSize:
            wysize = int(wysize * (float(ds.RasterYSize - ry) / rysize))
            rysize = ds.RasterYSize - ry

        return (rx, ry, rxsize, rysize), (wx, wy, wxsize, wysize)

    def scale_query_to_tile(self, dsquery, dstile, tilefilename=''):
        """Scales down query dataset to the tile dataset"""

        querysize = dsquery.RasterXSize
        tilesize = dstile.RasterXSize
        tilebands = dstile.RasterCount

        if self.options.resampling == 'average':

            # Function: gdal.RegenerateOverview()
            for i in range(1, tilebands+1):
                # Black border around NODATA
                res = gdal.RegenerateOverview(dsquery.GetRasterBand(i), dstile.GetRasterBand(i),
                                              'average')
                if res != 0:
                    self.error("RegenerateOverview() failed on %s, error %d" % (tilefilename, res))

        elif self.options.resampling == 'antialias':

            # Scaling by PIL (Python Imaging Library) - improved Lanczos
            array = numpy.zeros((querysize, querysize, tilebands), numpy.uint8)
            for i in range(tilebands):
                array[:, :, i] = gdalarray.BandReadAsArray(dsquery.GetRasterBand(i+1),
                                                           0, 0, querysize, querysize)
            im = Image.fromarray(array, 'RGBA')     # Always four bands
            im1 = im.resize((tilesize, tilesize), Image.ANTIALIAS)
            if os.path.exists(tilefilename):
                im0 = Image.open(tilefilename)
                im1 = Image.composite(im1, im0, im1)
            im1.save(tilefilename, self.tiledriver)

        else:

            # Other algorithms are implemented by gdal.ReprojectImage().
            dsquery.SetGeoTransform((0.0, tilesize / float(querysize), 0.0, 0.0, 0.0,
                                     tilesize / float(querysize)))
            dstile.SetGeoTransform((0.0, 1.0, 0.0, 0.0, 0.0, 1.0))

            res = gdal.ReprojectImage(dsquery, dstile, None, None, self.resampling)
            if res != 0:
                self.error("ReprojectImage() failed on %s, error %d" % (tilefilename, res))

    def tiff2lerc(self, tifffiledir: str, outpath: str) -> None:
        """
    
        :param lerc_bin_path:
        :param outpath:
        :return:
        """
        if platform.system() == "Darwin":
            lerc_bin = '../bin/lerctiler_mac'
        else:
            lerc_bin = '../bin/lerctiler'
        if not os.path.exists(tifffiledir):
            print("The tiff files does not exist.")
        tiff_tile_path = tifffiledir
        tiffs_path = '{0}/'.format(tiff_tile_path)
        lercs_path = '{0}/'.format(outpath)
        if not os.path.exists(lercs_path):
            os.makedirs(lercs_path)
        try:
            tif_to_lerc_cmd = '{0} --input {1} --output {2} --band {3} --maxzerror {4}'.format(
            lerc_bin, tiffs_path, lercs_path, 1, 0.01)
            os.system(tif_to_lerc_cmd)
        except Exception as err:
            print(err)


def main():
    argv = gdal.GeneralCmdLineProcessor(sys.argv)
    if argv:
        raster2tiles = Raster2Tiles(argv[1:])
        raster2tiles.process()

if __name__ == '__main__':
    main()

# vim: set tabstop=4 shiftwidth=4 expandtab:
