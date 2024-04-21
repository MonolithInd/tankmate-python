##################################################
## A simple python program for inteacting with  ##
## TankMate water sensors. This script prints   ##
## out the current percenteage tank utilisation ##
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
USER_ID = config['auth']['USER_ID']

# Parse command line arguments
parser = argparse.ArgumentParser(description="Script to retrive the current tank utilisation percentage from a TankMate Sensor",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--formatted", action="store_true", help="human friendly format")
args = parser.parse_args()
config = vars(args)

# URL for tank level data JSON blob
url = "https://api.tankmate.app/status/?uid=" + USER_ID
# headers to send to API
headers = {'Accept': 'application/json', 'api-key': API_KEY}

# get data
response = requests.get(url, headers=headers)

# parse json data
json_data = response.json()

percent = str(json_data[DEVICE_ID]['currentPercent'])

if (config['formatted']):
    print("Current tank percentage is: "+ percent + "%")
else:
    print(percent)

# to print out all returned data for troubleshooting
# uncomment below line 
# print(json.dumps(json_data, indent=4))
