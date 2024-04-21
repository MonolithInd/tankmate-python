##################################################
## A simple python program for inteacting with  ##
## TankMate water sensors. This script prints   ##
## out the last level reading from the tank     ##
##                                              ##
## https://tankmate.com.au                      ##
## Written by Kai Frost                         ##
##################################################

import requests
import json
import argparse
import configparser
from pprint import pprint

# read config file that contains things like the API key and userID
# required to make the calls
config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['auth']['API_KEY']
DEVICE_ID = config['auth']['DEVICE_ID']
# number of days to call. set to lowest value to minimise API load
DAYS = "1"

# Parse command line arguments
parser = argparse.ArgumentParser(description="Script to show latest Tankmate Sensor water level reading",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--formatted", action="store_true", help="human friendly format")
args = parser.parse_args()
config = vars(args)

# URL for tank level data JSON blob
url = "https://api.tankmate.app/level-data/?deviceId=" + DEVICE_ID + "&days=" + DAYS
# headers to send to API
headers = {'Accept': 'application/json', 'api-key': API_KEY}

# get data
response = requests.get(url, headers=headers)

# pardsed json data
json_data = response.json()

# iterate through the response data to find the last value
for i in json_data:
    last_entryID = i

water_level = json_data[last_entryID]['data']

if (config["formatted"]):
        print ("Last Water level reading was: " + water_level + "m")
else:
    print (water_level)

# to print out all returned data for troubleshooting
# uncomment below line
# print(json.dumps(json_data, indent=4))
