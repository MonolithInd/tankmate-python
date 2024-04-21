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
import os
# from pprint import pprint

# Parse command line arguments
parser = argparse.ArgumentParser(description="Script to retrive the current tank utilisation percentage from a TankMate Sensor",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-j", "--json", action="store_true", help="output requested data as JSON and exit")
parser.add_argument("-c", "--config",action="store", type=str,  help="Specify the config file that contains things like the API key and UserID", default="config.ini")
parser.add_argument("-u", "--userid",action="store", type=str,  help="Manually specify the userID for queries.")
parser.add_argument("-a", "--apikey",action="store", type=str,  help="Manually specify the apikey for queries")
parser.add_argument("-l", "--list", action="store_true", help="List tanks by deviceID and name")
parser.add_argument("-id", "--deviceID",action="store", type=str,  help="Specify the deviceID for arguments that require it. If not specified the first deviceID associated with the account is used")
parser.add_argument("-r", "--readings", action="store_true", help="Return readings from tank. If -d <days> and -id <deviceID> are not specificed, defailts to 1 day for first device found on account")
parser.add_argument("-d", "--days",action="store", type=str,  help="Specify number of days to return tank data for")
args = parser.parse_args()
args= vars(args)

# read config file that contains things like the API key and userID
# or grab from command line required to make the calls

if (args['userid'] and args['apikey']):
    API_KEY = args['apikey']
    USER_ID = args['userid']
else:
    if (os.path.isfile(args['config'])):
        configfile = configparser.ConfigParser()
        configfile.read(args['config'])
        API_KEY = configfile['auth']['API_KEY']
        USER_ID = configfile['auth']['USER_ID']
    else:
        print("\n!!! Invalid config file specified and apikey and userid not defined on commandline !!!\n")
        parser.print_help()
        quit()

# headers to send to API
HEADERS = {'Accept': 'application/json', 'api-key': API_KEY}
# URL for tank/deviceID data we always need to pull this as it's needed for
# all other calls.
TANKURL = "https://api.tankmate.app/status/?uid=" + USER_ID

###############################################
# Function to grab tankdata and populate the 
# data blob with all tank info for processing
# TODO look at way to make more efficent.

def get_tankdata():
    response = requests.get(TANKURL, headers=HEADERS)
    json_data = response.json()
    return json_data

# define tank data blob
TANKDATA = get_tankdata()

# unless we're listing tanks if devicde_id is defined on the command line use it, otherwise 
# return data for first tank found in TANKDATA
if not args['list']:
    if args['deviceID']:
        DEVICE_ID=args['deviceID']
    else:
        print("### No device ID specified, using tank ID of first tank associated with userID ###")
        DEVICE_ID=next(iter(TANKDATA))

    if (args['readings']):
        if not (args['days']):
            print ("### Numebr of days to get readings for not defined, defaulting to 1 ###") 
            DAYS="1"
        else:
            DAYS=args['days']
    # URL for tank readings
    if (args['readings']):
        READINGSURL = "https://api.tankmate.app/level-data/?deviceId=" + DEVICE_ID + "&days=" + DAYS

### Setup of all required variables done
### move to main program 

###############################################
# Function to list all deviceIDs and human
# readable names

def list_devices():
    if args['json']:
        print(TANKDATA)
    else: 
        print ("-------------------------------")
        for i in TANKDATA:
            deviceID = i;
            tank_name = TANKDATA[i]['tankName']
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
    # check if deviceID specified.
    if not (args['deviceID']):
        print("No device ID!")



if (args['list']):
    list_devices()

if (args['readings']):
    get_readings()


#percent = str(json_data[DEVICE_ID]['currentPercent'])

#if (config['formatted']):
#    print("Current tank percentage is: "+ percent + "%")
#else:
#    print(percent)

# to print out all returned data for troubleshooting
# uncomment below line 
# print(json.dumps(json_data, indent=4))
