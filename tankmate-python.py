##################################################
## A simple python program for inteacting with  ##
## TankMate water sensors. This scrupt should   ##
## eventually allow you do perform most         ##
## functions from the API                       ##
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
USER_ID = config['auth']['USER_ID']

# Parse command line arguments
parser = argparse.ArgumentParser(description="Script to retrive the current tank utilisation percentage from a TankMate Sensor",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--formatted", action="store_true", help="human friendly output")
parser.add_argument("-l", "--list", action="store_true", help="List tanks by name and deviceID")
args = parser.parse_args()
config = vars(args)

# URL for tank level data JSON blob
url = "https://api.tankmate.app/status/?uid=" + USER_ID
# headers to send to API
headers = {'Accept': 'application/json', 'api-key': API_KEY}


def list_devices():
    # get data
    response = requests.get(url, headers=headers)
    json_data = response.json()
    print ("-------------------------------")
    for i in json_data:
        deviceID = i;
        tank_name = json_data[i]['tankName']
        print ("Tank Name: " + tank_name)
        print ("    deviceID: " + deviceID)
        print ("-------------------------------")

if (config['list']):
    list_devices()



#percent = str(json_data[DEVICE_ID]['currentPercent'])

#if (config['formatted']):
#    print("Current tank percentage is: "+ percent + "%")
#else:
#    print(percent)

# to print out all returned data for troubleshooting
# uncomment below line 
# print(json.dumps(json_data, indent=4))
