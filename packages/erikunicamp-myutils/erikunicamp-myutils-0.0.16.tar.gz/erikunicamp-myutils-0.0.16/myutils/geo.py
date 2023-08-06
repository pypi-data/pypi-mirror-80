import numpy as np
import os
from math import radians, cos, sin, asin, sqrt
import geopandas as geopd
import scipy.optimize

R = 6378

##########################################################
def haversine(lon1, lat1, lon2, lat2, unit='km'):
    """Calculate the great circle distance (in meters) between two points
    on the earth (specified in decimal degrees) """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    if unit in ['m', 'meters']: return c * R * 1000
    else: return c * R

##########################################################
def get_shp_points(shppath):
    """Get points from @shppath and returns list of points, x and y """

    geodf = geopd.read_file(shppath)
    shapefile = geodf.geometry.values[0]
    return shapefile.exterior.xy

##########################################################
def deg2num(lon_deg, lat_deg, zoom, imgsize=256):
    """From the (lat,lon) in degrees, get the (x, y) of the tile,
    as well as the pixel in the image."""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = ((lon_deg + 180.0) / 360.0 * n)
    ytile = ((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (int(xtile), int(ytile),
            int(math.modf(xtile)[0]*imgsize), int(math.modf(ytile)[0]*imgsize))

##########################################################
def num2deg(xtile, ytile, zoom):
    """From the tile x and y, get the (lat,lon) in degrees"""
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lon_deg, lat_deg)

##########################################################
def dist_to_deltalon(dist, lonref, latref):
    """Get the variation in longitude based on a reference lat and lon.
    For the same distance, lon varies more than lat."""
    def get_delta_lon_from_d(lon1, lat1=latref, lon2=lonref, lat2=latref):
        return dist - haversine(lon1, lat1, lon2, lat2)

    lon2 = lonref + 20 # a large enough diff in lon to contain the @dist
    lon2 = scipy.optimize.bisect(get_delta_lon_from_d, lonref, lon2,
            xtol=0.00001, rtol=0.00001)
    return np.abs(lon2 - lonref)

