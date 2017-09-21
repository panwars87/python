#
# A python script to build outgoing config template dynamically
#
# author: Shashant Panwar

import os
import sys
import json
from time import sleep
import ConfigParser

# Script global variables
conf = ""
config_file_name = ""
json_data_dump = {}
SECTIONS = {
    'file': 'file-section',
}
PROPERTIES = {
    'custom_dt': '',
    'module_name': 'apt',
    'temp_location': '',
    'processed_location': '',
    'file_name': '',
    'is_gzip': False,
    'is_encrypt': False,
    'enc_format': '',
    'enc_recipient': '',
    'is_empty_check': True,
    'delimiter': '',
    'is_header': True,
    'props': 'set hive.execution.engine=mr; set hive.auto.convert.join=false;',
    'cmhogcdwdb': 'cmhpcdw',
    'cmhcdwdb': 'cmhpogcdw',
    'dt': 'date +%Y-%m-%d',
    'hql_file_name': 'insert_og_apt_elfscoringseg.hql',
    'hive_cmd': 'hive --hiveconf cmhcdwdb=$cmhcdwdb --hiveconf cmhogcdwdb=$cmhpogcdw --hiveconf DATESTAMP=$dt',
    'emailfrom': 'outgoingfeeds_status@express.com',
    'emailTo': 'spanwar@express.com',
    'destination_sftp_username': 'express',
    'destination_sftp_password': '',
    'destination_sftp_url': '208.45.140.230',
    'destination_sftp_location': 'incoming'
}
# #######################


# function to set global variable
def fn_set_global_var():
    # first get config_file_name from script args
    global config_file_name
    config_file_name = fn_get_config_file()
    # second load config file in conf variable
    global json_data_dump
    json_data_dump = fn_resolve_config()


# Function to check script env variables
def fn_get_config_file():
    no_of_args = len(sys.argv)
    if no_of_args != 2:
        print "Usage: python <script-name> <config-file-path>"
        exit(1)
    else:
        args = sys.argv
        file_name = args[1]

    print "Looking for config file: " + file_name
    if not file_name.lower().endswith(".json"):
        print "Config file is not valid, name should end with .json"
        exit(1)

    return file_name


# Function to check if config file exists on file-system or not
def fn_resolve_config():
    try:
        if os.path.exists(config_file_name):
            print "Found config, Looking from " + config_file_name
        else:
            print "No config found " + config_file_name + ". Creating a new one."
            open(config_file_name, 'a').close()

        with open(config_file_name, 'r') as f:
            try:
                json_dump = json.load(f)
            except ValueError:
                json_dump = {}

    except Exception as err:
        print "Error while loading json data from file system. ---> " + err.message
        exit(1)

    return json_dump


# function to get property value from config
def fn_get_prop_val(props, def_val):
    try:
        def_val = json_data_dump[props]
    except Exception as err:
        print 'No {0} property found.'.format(props)
        return def_val

    return def_val


# function to get property value from config
def fn_get_all_prop_val(conf):
    props_map = {}
    for key, value in PROPERTIES.items():
        # print "Key is : " + str(key)
        # print "Value is : " + str(value)
        if key != "":
            temp_val = fn_get_prop_val(key, value)
            props_map[key] = temp_val

    return props_map


# main function
def main():
    print "****************************************"
    print "Running build-config"
    print "****************************************"

    # set global vars
    fn_set_global_var()

    # get all default prop values
    props_map = fn_get_all_prop_val(conf)

    print "****************************************"
    print "User Input"
    print "****************************************"
    # get props to input user values
    for k, v in props_map.items():
        # print ("%s: %s" % (k, v))
        user_input = raw_input("Enter {0} [{1}]:".format(k, v))
        if user_input == '':
            props_map[k] = v
        else:
            props_map[k] = user_input

    print "****************************************"
    print "Store Configs"
    print "****************************************"

    # Writing our configuration file to the user defined module config file
    print "Saving the configs, please wait"
    sleep(2)
    #
    try:
        with open(config_file_name, 'w') as f:
            json.dump(props_map, f)
    except Exception as err:
        print "Error while writing json in config file" + err
        exit(1)
    #
    sleep(2)
    print "Done"
    print "****************************************"
    print "****************************************"

# Running Main
if __name__ == "__main__":
    main()
