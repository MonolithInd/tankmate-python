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
parser.add_argument("-j", "--json", action="store_true", help="output requested data as JSON and exit")
parser.add_argument("-l", "--list", action="store_true", help="List tanks by deviceID and name")
parser.add_argument("-id", "--deviceID",action="store", type=str,  help="Specify the deviceID for arguments that require it. If not specified the first deviceID associated with the account is used")
parser.add_argument("-r", "--readings", action="store_true", help="Return readings from tank. If -d <days> and -id <deviceID> are not specificed, defailts to 1 day for first device found on account")
parser.add_argument("-d", "--days",action="store", type=str,  help="Specify number of days to return tank data for", default="1")
args = parser.parse_args()
config = vars(args)

# URL for tank level data JSON blob
url = "https://api.tankmate.app/status/?uid=" + USER_ID
# headers to send to API
headers = {'Accept': 'application/json', 'api-key': API_KEY}


###############################################
# Function to list all deviceIDs and human
# readable names

def list_devices():
    # get data
    response = requests.get(url, headers=headers)
    json_data = response.json()
    if config['json']:
        print(json_data)
    else: 
        print ("-------------------------------")
        for i in json_data:
            deviceID = i;
            tank_name = json_data[i]['tankName']
            print ("deviceID: " + deviceID)
            print ("    Tank Name: " + tank_name)
            print ("-------------------------------")


###############################################
# Function to return reading data for specified
# timeframe (default 1 day)
# if not deviceID is specified it pulls the 
# first one for the UID and returns those 
# readings

def get_readings():
    print (config['deviceID'])
    # check if deviceID specified.
    if (config['deviceID'] == "None"):
        print("No device ID!")



if (config['list']):
    list_devices()

if (config['readings']):
    get_readings()


#percent = str(json_data[DEVICE_ID]['currentPercent'])

#if (config['formatted']):
#    print("Current tank percentage is: "+ percent + "%")
#else:
#    print(percent)

# to print out all returned data for troubleshooting
# uncomment below line 
# print(json.dumps(json_data, indent=4))
