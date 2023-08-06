# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.s

import os
from csv import DictReader
from collections import namedtuple


StationInfo = namedtuple("StationInfo", ["index", "bikes", "capacity", "id"])


def get_station_info(station_state_file: str):
    """get stations information from specified csv file"""
    stations_info = [] 
    if station_state_file.startswith("~"):
        station_state_file = os.path.expanduser(station_state_file)
    with open(station_state_file, "r") as fp:
        reader = DictReader(fp)

        for row in reader:
            si = StationInfo(
                int(row["station_index"]),
                int(row["init"]), # init bikes
                int(row["capacity"]), 
                int(float(row["station_id"])) # It's a patch for the uncleaned data in the original files, such as 12345.0
            )

            stations_info.append(si)

    return stations_info