#!/usr/bin/env python

import ConfigParser
import json
import cStringIO
import sys


def string_config(string, defaults):
    """ Read a Config String and Build a Configuration Dictionary. """
    return load_config(cStringIO.StringIO(string), defaults)


def load_config(file, defaults):
    """ Open a Config File and Build a Configuration Dictionary. """
    config = ConfigParser.ConfigParser()
    configuration = defaults.copy() if isinstance(defaults, dict) else {}

    # Open the file
    if isinstance(file, str):
        # Can't open the file, return the default
        if not config.read(file):
            return configuration
    # Or read the buffer
    else:
        try:
            config.readfp(file)
        except:
            return configuration

    for section in config.sections():
        configuration[section] = {}
        for option in config.options(section):
            configuration[section][option] = config.get(section, option)

    return configuration


def main(argv):
    """
    The function to be executed on a standalone call of the program.
    Used to test the function of the script.
    """
    print json.dumps(load_config("config/dummy.conf", {'section_00': {'a':1}}), indent=4)


if __name__ == "__main__":
    main(sys.argv[1:])
