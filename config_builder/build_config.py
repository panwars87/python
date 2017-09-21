#
# A python script to build outgoing config template dynamically
#
# author: Shashant Panwar
#
# Important Note: If you are adding a new property follow below steps:
#                 1. Add a new property in PROPERTIES and PROP_USAGE.
#                 2. If it is a boolean property, add entry in BOOL_PROPS.
#                 3. If it is a mandatory property, add an entry in MANDATORY_PROPS.
#

import os
import argparse
from time import sleep
import ConfigParser

# Script global variables
conf = ""
args = ""
config_file_name = ""
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
    'is_sftp': False,
    'is_encrypt': False,
    'enc_format': 'pgp | gpg',
    'enc_recipient': '',
    'is_empty_check': True,
    'delimiter': '',
    'is_header': True,
    'props': 'set hive.execution.engine=mr; set hive.auto.convert.join=false;',
    'cmhogcdwdb': 'cmhpogcdw',
    'cmhcdwdb': 'cmhpcdw',
    'dt': '2017-08-10',
    'insert_hql_file_name': 'insert_og_apt_elfscoringseg.hql',
    'select_hql_file_name': 'select_og_apt_elfscoringseg.hql',
    'hive_cmd': 'hive --hiveconf cmhcdwdb=$cmhcdwdb --hiveconf cmhogcdwdb=$cmhpogcdw --hiveconf DATESTAMP=$dt',
    'emailfrom': 'outgoingfeeds_status@express.com',
    'emailTo': 'spanwar@express.com',
    'destination_sftp_username': 'express',
    'destination_sftp_password': '',
    'destination_sftp_url': '208.45.140.230',
    'destination_sftp_location': 'incoming',
    'project_dir': ''
}
BOOL_PROPS = {'is_gzip', 'is_encrypt', 'is_empty_check', 'is_header', 'is_sftp'}
MANDATORY_PROPS = {
    'module_name', 'temp_location', 'processed_location', 'file_name', 'delimiter', 'cmhogcdwdb', 'cmhcdwdb',
    'dt', 'select_hql_file_name', 'hive_cmd', 'emailfrom', 'emailTo', 'project_dir', 'is_sftp'
}
PROP_USAGE = {
    'custom_dt': 'Custom date if you want to run your script other than todays date.',
    'module_name': 'Module Name',
    'temp_location': 'Stage location of the file where you want to create.',
    'processed_location': 'Final location to store the file after sending it to vendor.',
    'file_name': 'Name of the file according to business requirement.',
    'is_gzip': 'Is compression required? Default: GZIP',
    'is_sftp': 'Do you want to upload file to sftp?',
    'is_encrypt': 'Is encryption required? Options: pgp | gpg',
    'enc_format': 'Encryption format. Availbale format: pgp | gpg',
    'enc_recipient': 'Encryption Recipient',
    'is_empty_check': 'Is empty check required?',
    'delimiter': 'File Delimiter',
    'is_header': 'Is header for file?',
    'props': 'Any additional property for hive? Eg: set hive.execution.engine=mr;.\n Script will prepend this in hql file. Do not repeat properties',
    'cmhogcdwdb': 'Hive outgoing database name',
    'cmhcdwdb': 'Main hive database name',
    'dt': 'Today date in YYYY-MM-DD format',
    'insert_hql_file_name': 'Insert HQL file name you want to execute.\n Please space seperated list of files. Eg: a.hql b.hql',
    'select_hql_file_name': 'Select HQL file name you want to execute.\n Please space seperated list of files. Eg: a.hql b.hql',
    'hive_cmd': 'Hive command with --hiveconf. Do not specify -f option with file name.\n Eg: hive --hiveconf cmhcdwdb=$cmhcdwdb --hiveconf cmhogcdwdb=$cmhpogcdw --hiveconf DATESTAMP=$dt',
    'emailfrom': 'Senders email. Eg: outgoingfeeds_status@express.com',
    'emailTo': 'Recipient email. Eg: spanwar@express.com',
    'destination_sftp_username': 'Vendor sftp username',
    'destination_sftp_password': 'Vendor sftp password',
    'destination_sftp_url': 'Vendore sftp hostname or ip address',
    'destination_sftp_location': 'Vendor sftp location',
    'project_dir': 'Project direcotry where all hql files exists, script will look for files in this dir'
}
# #######################


# function to set global variable
def fn_set_global_var():
    # first get config_file_name from script args
    global config_file_name
    config_file_name = fn_get_config_file()
    # second load config file in conf variable
    global conf
    conf = fn_resolve_config()


# function to get script absolute path
def fn_get_script_path(file_name):
    return os.path.dirname(os.path.realpath(file_name))


# Function to check script env variables
def fn_get_config_file():
    fname = args.config_file_name
    script_dir_path = fn_get_script_path(fname)
    file_name = script_dir_path+"/py-config/"+fname
    print 'Looking for config file: {0}'.format(file_name)
    if not file_name.lower().endswith(".ini"):
        print 'Config file is not valid, name should end with .ini'
        exit(1)

    return file_name


# Function to check if config file exists on file-system or not
def fn_resolve_config():
    try:
        c = ConfigParser.RawConfigParser()
        if os.path.exists(config_file_name):
            print 'Found config, Looking from {0}'.format(config_file_name)
        else:
            print 'No config found {0}. Creating a new one.'.format(config_file_name)
            open(config_file_name, 'a').close()

        c.read(config_file_name)
    except Exception as err:
        print 'Error while loading config from file system {0}'.format(err)
        exit(1)

    return c


# function to check section in config file
def fn_check_section(section):
    try:
        if conf.has_section(section) is False:
            conf.add_section(section)
    except ConfigParser.Error:
        print 'Error while checking section in config file'
        exit(1)


# function to get property value from config
def fn_get_prop_val(section, props, def_val):
    try:
        fn_check_section(section)
        def_val = conf.get(section, props)
    except ConfigParser.NoOptionError:
        if args.verbose:
            print 'No {0} property found in {1}.'.format(props, section)
        return def_val

    return def_val


# function to get property value from config
def fn_get_all_prop_val(conf):
    props_map = {}
    for key, value in PROPERTIES.items():
        # print "Key is : " + str(key)
        # print "Value is : " + str(value)
        if key != "":
            temp_val = fn_get_prop_val(SECTIONS.get('file', 'file-section'), key, value)
            props_map[key] = temp_val

    return props_map


# function to check user input for boolean properties
def fn_check_bool_props(key, value):
    if args.verbose:
        print "fn_check_bool_props: Key is {0} & value is {1}".format(key, value)
    if key in BOOL_PROPS:
        if args.verbose:
            print "Found key in BOOL_PROPS array for value -- {0} and type -- {1}".format(value, type(value))
        if str(value) not in {"True", "False"}:    
            return False

    return True


# function to check user input for mandatory properties
def fn_check_mandatory_props(key, value):
    if args.verbose:
        print "fn_check_mandatory_props: Key is {0} & value is {1}".format(key, value)
    if key in MANDATORY_PROPS and value == "":
            return False

    return True


# function to get mandatory field message
def fn_get_mand_field_msg(key):
    if key in MANDATORY_PROPS:
        return '*Required Property*'
    else:
        return "*Optional Property*"


# function to get property usage
def fn_check_property_usage(key):
    if key in PROP_USAGE:
        return PROP_USAGE.get(key, "Description not available")

# function to check user input
def fn_check_user_input(key, value):
    err_msg = {
        'status': False,
        'message': "Success"
    }

    if not fn_check_mandatory_props(key, value):
        err_msg["status"] = True
        err_msg["message"] = '{0} is a required property'.format(key)
    if args.verbose:
            print 'Value from bool prop is : {0}'.format(fn_check_bool_props(key, value))
    if not fn_check_bool_props(key, value):
        err_msg["status"] = True
        err_msg["message"] = 'Valid values for boolean properties are: True/False'

    if args.verbose:
        print 'Sent error message is {0}'.format(err_msg)

    return err_msg


# function to add a new property in properties file
def fn_add_new_property(key, default_value, desc):
    PROPERTIES[key] = default_value
    PROP_USAGE[key] = desc
    if args.prop_mandatory:
        MANDATORY_PROPS.add(key)

    if args.prop_boolean:
        BOOL_PROPS.add(key)
    print 'Property {0} added successfully'.format(key)


# function to delete an existing property
def fn_delete_property(key):
    try:
        del PROPERTIES[key]
        del PROP_USAGE[key]
        if key in MANDATORY_PROPS:
            del MANDATORY_PROPS[key]
        if key in BOOL_PROPS:
            del BOOL_PROPS[key]
        print 'Property {0} deleted successfully'.format(key)
    except KeyError as err:
        print 'Error while deleting keys from properties: {0}.'.format(err.message)


# function to get a concatenated array of select.hql and select file names.
def fn_get_select_array(select_hql_array, select_file_array):
    # print 'hql array: {0}, file array: {1}'.format(select_hql_array, select_file_array)
    try:
        if select_file_array == "" or select_hql_array == "":
            if args.verbose:
                print 'Arrays are empty'
            return ""
        else:
            arr_1 = select_hql_array.split(" ")
            arr_2 = select_file_array.split(" ")

            if len(arr_1) != len(arr_2):
                print 'select_hql_file_name & file_name are not in sync. ' \
                      '\n Count of select_hql_file_name are not equal to output file_name '
                exit(1)

            return map('#'.join, zip(arr_1, arr_2))
    except Exception as err:
        print 'Error while creating consolidated select array'.format(err.message)


# main function
def main():
    print '****************************************'
    print 'Running build-config'
    print '****************************************'

    global args
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    add_prop_grp = parser.add_mutually_exclusive_group()

    group.add_argument("-q", "--quiet", help="Run script quietly, script will not print property messages.",
                       action="store_true")
    group.add_argument("-v", "--verbose", help="Print property message.", action="store_true")

    add_prop_grp.add_argument("-a", "--add_property", help="Set -a to add a new property in file.",
                       action="store_true")
    add_prop_grp.add_argument("-d", "--delete_property", help="Set -d to delete an existing property from file.",
                       action="store_true")
    parser.add_argument("-name", "--prop_name", help="Default value of property", default="")
    parser.add_argument("-value", "--prop_default_value", help="Default value of property", default="")
    parser.add_argument("-desc", "--prop_description", help="Property Description", default="")
    parser.add_argument("-m", "--prop_mandatory", help="Set if property is mandatory", action="store_true")
    parser.add_argument("-b", "--prop_boolean", help="Set if it is a Boolean property and you want boolean check", action="store_true")
    parser.add_argument("config_file_name", help="Config file path")

    args = parser.parse_args()
    if args.verbose:
        print args

    # add & delete simply add or remove the property from dict.
    # actual handling happens in fn_get_all_prop_val
    if args.add_property:
        if args.prop_name == "" or args.prop_default_value == "" or args.prop_description == "":
            print 'Please enter name, default value and description for the property'
            exit(1)
        else:
            print 'Adding new property : {0}'.format(args.prop_name)
            fn_add_new_property(args.prop_name, args.prop_default_value, args.prop_description)

    # need to fix delete by moving the props to a JSON object and read it dynamically
    if args.delete_property:
        if args.prop_name == "":
            print 'Please enter property name'
            exit(1)
        else:
            print 'Deleting property : {0}'.format(args.prop_name)
            fn_delete_property(args.prop_name)

    fn_set_global_var()
    props_map = fn_get_all_prop_val(conf)

    # skip this piece if user opted for add or delete property
    # if args.add_property or args.delete_property:
    print '****************************************'
    print 'User Input'
    print '****************************************'
    # get props to input user values
    for k, v in props_map.items():
        user_input = raw_input("{0} -- {1}\nEnter {2} [{3}]:".format(fn_check_property_usage(k), fn_get_mand_field_msg(k), k, v))
        if user_input == '':
            user_input = v

        err_msg = fn_check_user_input(k, user_input)
        if not err_msg.get("status"):
            props_map[k] = user_input
        else:
            print err_msg.get("message", "Error while validation value for the property.")
            print 'Please rerun script and enter valid details'
            exit(1)

    final_select_arr = fn_get_select_array(props_map.get('select_hql_file_name'), props_map.get('file_name'))
    props_map['final_select_arr'] = " ".join(final_select_arr)
    if args.verbose:
        print 'final select array is : {0}'.format(final_select_arr)

    print '****************************************'
    print 'Store Configs'
    print '****************************************'
    section = SECTIONS.get('file', 'file-section')
    for k, v in props_map.items():
        print ("%s: %s" % (k, v))
        try:
            conf.set(section, k, v)
        except ConfigParser.Error as err:
            print 'Error while setting property in config file {0}'.format(err)
            exit(1)

    # Writing our configuration file to the user defined module config file
    print '****************************************'
    print 'Saving the configs, please wait'
    sleep(2)

    try:
        with open(config_file_name, 'wb') as configfile:
            conf.write(configfile)
    except ConfigParser.Error as err:
        print 'Error while writing property in config file {0}'.format(err)
        exit(1)

    sleep(2)


# Running Main
if __name__ == "__main__":
    main()

