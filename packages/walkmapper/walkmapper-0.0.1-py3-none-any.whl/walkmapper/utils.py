import datetime
import os
import re
import shutil
import datetime
import time

import gpxpy
import numpy as np
import pandas as pd


def haversine(l_1, l_2):
    '''
    Calculates haversine of angle

    Parameters
    -----------
    l_1: latitude or longitude of first point (in radians)
    l_2: latitude or longitude of second point (in radians)

    Returns
    ----------
    haversine of angle
    '''
    return (1 - (np.cos(l_2 - l_1))) / 2.0


def calculate_distance(lat_1, lon_1, lat_2, lon_2):
    '''
    Employs haversine function to calculate distance between two points

    Parameters
    -----------
    lat_1: latitude of first point
    lon_1: longitude of first point
    lat_2: latitude of second point
    lon_2: longitude of second point

    Returns
    -----------
    distance between two coordinates in meters
    '''
    lat_1 = np.radians(lat_1)
    lon_1 = np.radians(lon_1)
    lat_2 = np.radians(lat_2)
    lon_2 = np.radians(lon_2)

    r = 6367303     # radius at ~45.5 degree latitude (m)
    return 2 * r * np.arcsin(np.sqrt(haversine(lat_1, lat_2) + np.cos(lat_1) * np.cos(lat_2) * haversine(lon_1, lon_2)))


def map_file_name(current_map_file_path, ur_lat, ur_lon, ll_lat, ll_lon, description=None):
    '''
    Renames an existing map image based on lower-left-corner and upper-right-corner lats/lons

    Parameters
    -----------
    current_map_file_path: current file path to image of interest
    ur_lat: latitude of upper right corner of map image
    ur_lon: longitude of upper right corner of map image
    ll_lat: latitude of lower left corner of map image
    ll_lon: longitude of lower left corner of map image
    description: optional brief description of the map (e.g.: "Portland")

    Returns
    -----------
    Function does not return anything, instead copies and renames the image file
    '''

    # parsing the absolute path, the file name, and the extension of the image file
    absolute_path = os.path.split(os.path.abspath(current_map_file_path))[0]
    file_name, extension = os.path.splitext(
        os.path.basename(current_map_file_path))

    new_file_name = ''      # for building our new file name

    # add in the optional description
    if description:
        description = description.split(" ")
        append_description = ''
        for i in description:
            append_description += i.capitalize()
        new_file_name += append_description + '_'

    # incorporating the lat/lons of the upper right and lower left corners

    # upper right latitude
    if ur_lat < 0:
        new_file_name += "m{}_".format(abs(ur_lat))
    else:
        new_file_name += str(ur_lat) + '_'

    # upper right longitude
    if ur_lon < 0:
        new_file_name += "m{}".format(abs(ur_lon)) + '_'
    else:
        new_file_name += str(ur_lon) + '_'

    # lower left latitude
    if ll_lat < 0:
        # 'm' used as prefix for negative numbers
        new_file_name += "m{}_".format(abs(ll_lat))
    else:
        new_file_name += str(ll_lat) + '_'

    # lower left longitude
    if ll_lon < 0:
        new_file_name += "m{}".format(abs(ll_lon))
    else:
        new_file_name += str(ll_lon)

    new_file_name += extension  # add back the extension

    new_file_path = os.path.join(
        absolute_path, new_file_name)  # final path name

    # copy the image at the current path and save it with the new path name
    shutil.copy(os.path.abspath(current_map_file_path), new_file_path)


def bound_box_from_map(map_file_path):
    '''
    Parses map file name to extract bounding box (map file should have been named with map_file_name function)

    Parameters
    -----------
    map_file_path: path to map file

    Returns
    -----------
    bounding box as a tuple
    '''
    try:
        map_file_path = os.path.splitext(map_file_path)[0].split("_")
        temp_bound_box = [map_file_path[-1], map_file_path[-3],
                          map_file_path[-2], map_file_path[-4]]
    except IndexError:
        print("Error: please make sure map title has format Description_UpperRightLat_UpperRightLon_LowerLeftLat_LowerLeftLon.png")
        raise
    bound_box = []
    for i in temp_bound_box:
        try:
            bound_box.append(float(i))
        except:
            bound_box.append(-1 * float(i[1:]))

    return tuple(bound_box)


def gpx_to_dataframe(file_name, time_delta):
    '''
    Converts a GPX file to a pandas dataframe

    Parameters
    -----------
    file_name: path/file name of the GPX file
    time_delta: difference in hours between your timezone and UTC (-7 is PST)

    Returns
    -----------
    pandas dataframe containing time/longitued/latitude data
    '''
    # open and parse the GPX file
    with(open(file_name)) as f:
        gpx_file_data = gpxpy.parse(f)

    # arrays for storing data
    times = []
    longitudes = []
    latitudes = []

    # iterate through the GPX file and append data to arrays
    for track in gpx_file_data.tracks:
        for segment in track.segments:
            for point in segment.points:
                point.adjust_time(datetime.timedelta(
                    hours=time_delta))  # time is natively UTC
                times.append(point.time)
                longitudes.append(point.longitude)
                latitudes.append(point.latitude)

    return pd.DataFrame(data={"Time": times,
                              "Longitude": longitudes,
                              "Latitude": latitudes})


def route_distance(gpx_file_df):
    '''
    Calculates the distance traversed in a GPX file

    Parameters
    -----------
    gpx_file_df: GPX data already in a pandas dataframe

    Returns
    -----------
    total distance traversed in GPX data set
    '''
    lons = gpx_file_df["Longitude"]
    lats = gpx_file_df["Latitude"]

    distance = [calculate_distance(
        lats[i - 1], lons[i - 1], lats[i], lons[i]) for i in range(1, len(lons))]
    # converting from meters to miles and returning
    return round(sum(distance) * 0.000621371, 3)


def date_time_stamp():
    '''
    Creates a date/time stamp for file names (takes local time from your machine)
    '''
    t = datetime.datetime.fromtimestamp(time.time())
    return t.strftime("%Y%m%d_%H%M%S")
