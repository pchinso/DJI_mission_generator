#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
from pathlib import Path
from collections import deque
from itertools import cycle
import time
import json
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import configparser
from ast import literal_eval
from numpy import Inf
from pygeodesy.sphericalTrigonometry import LatLon
from pygeodesy.sphericalNvector import intersection, LatLon as LatLonS
from pygeodesy.points import isclockwise, isconvex, centroidOf
from pyproj import Transformer

# functions
from functions.utils import get_angle_wp,background_foreground_color, background_color, foreground_color
from functions.waypoint import WayPoint
from functions.waypointsmap import WaypointMap
from functions.dict2djikml import dict2djikml
from functions.drone_orientation.classes.droneorientation import DroneOri
from functions.drones import Drones


def load_json(json_path):
  
  try:
    # Open and read the JSON file
    with open(json_path, 'r') as file:
      data = json.load(file)
  except TypeError:
    file = json_path
    data = json.load(file)

  return(data)
   
def create_mission_for_DJI_Pilot(coordinates_path, project_name, output_dir):

  final_waypoint_dict = load_json(coordinates_path)

  output_dir =  Path(output_dir)

  if not os.path.exists(output_dir):
    os.mkdir(output_dir)

  wp_extras = dict2djikml(final_waypoint_dict, 
                          output_dir.joinpath(project_name +'_for_PILOT.kml'),
                          altitude=35,
                          gimbal=[-900,-450, -300, -150],
                          heading=0,
                          N_photos=4,
                          onfinish='hover',
                          speed = 2,
                          turnmode = 'Auto',
                          over_time_before_picture=1)

# Create the map
  the_map = WaypointMap(wp_extras[0])

  # waypoints to the map
  for waypoint in wp_extras:
      the_map.add_waypoint(waypoint, direction=False,
                            footprint=False, footprint_markers=False)

  the_map.add_colored_waypoint_path(wp_extras)

  # Export html map
  the_map.export_to_file(output_dir.joinpath(project_name +'.html'))


if __name__ == '__main__':

  coordinates_path = '/home/pcs/Documents/Python/DJI_mission_generator/sample_klm_dji_pilot/coordinates.json'
  project_name = 'test1'

  output_dir = '/home/pcs/Documents/Python/DJI_mission_generator/mission/'

  create_mission_for_DJI_Pilot(coordinates_path, project_name, output_dir)
