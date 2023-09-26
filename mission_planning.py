#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
from pathlib import Path
from collections import deque
from itertools import cycle
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import configparser
from ast import literal_eval
from numpy import Inf
from pygeodesy.sphericalTrigonometry import LatLon
from pygeodesy.sphericalNvector import intersection, LatLon as LatLonS
from pygeodesy.points import isclockwise, isconvex, centroidOf
from pyproj import Transformer
from utils import get_angle_wp,background_foreground_color, background_color, foreground_color
from waypoint import WayPoint
from waypointsmap import WaypointMap
from dict2djikml import dict2djikml
from drone_orientation.classes.droneorientation import DroneOri
from drones import Drones
import json




def load_coordinates_json(json_path):
  # Open and read the JSON file
  with open(json_path, 'r') as file:
    data = json.load(file)

  return(data)
   


def main():

  '''
  def dict2djikml (dic,
                  output_filename,
                  reverse_coordonates_transformer,
                  altitude,
                  onfinish='hover',
                  speed = 5,
                  turnmode = 'Auto',
                  over_time_before_picture=0):
                 
  '''
  output_dir = '/home/pcs/Documents/Python/DJI_mission_generator/'
  coordinates_path = '/home/pcs/Documents/Python/DJI_mission_generator/sample_klm_dji_pilot/coordinates.json'

  output_dir =  Path(output_dir)


  final_waypoint_dict = load_coordinates_json(coordinates_path)
  print(final_waypoint_dict)

#                           reverse_coordonates_transformer,


  wp_extras = dict2djikml(final_waypoint_dict, 
                          output_dir.joinpath('project_name'+'_for_PILOT.kml'),
                          altitude=35,
                          gimbal=[-900,-450, -300, -150],
                          heading=0,
                          N_photos=4,
                          onfinish='hover',
                          speed = 2,
                          turnmode = 'Auto',
                          over_time_before_picture=1)
  print(wp_extras[0])


# Create the map
  the_map = WaypointMap(wp_extras[0])

  # waypoints to the map
  for waypoint in wp_extras:
      the_map.add_waypoint(waypoint, direction=False,
                            footprint=False, footprint_markers=False)

  the_map.add_colored_waypoint_path(wp_extras)

  # Export html map
  the_map.export_to_file(output_dir.joinpath('project_name'+'.html'))


if __name__ == '__main__':
  main()
