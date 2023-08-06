import click

from configparser import SafeConfigParser
import os.path
import json
from collections import namedtuple
import errno

import requests

from ._version import version as __version__

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "hdo_uow")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config")
API_ENDPOINT = "https://cchdo.ucsd.edu/api/v1"

session = requests.Session()

def load_config():
    """Loads the config file from ~/.config/hdo_uow/config

    Checks files existance first (because the config parser seems to not care)
    Then attemts to read the config file.

    Prints (hopefully) helpful messages for the user if things don't go right.

    Q: Why not let each part of the program attempt to read the keys in the
    config itself rather than everything here?
    A: So that, at program run, we already know our config file is good, not
    when we need to use something in it.

    :returns: a namedtuple with the names "api_key", "api_end_point" and "headers"
    where the "headers" key contains a dict which can be passed into the
    reqeusts "headers" keyword arg.
    """
    if not os.path.isfile(CONFIG_FILE):
        print("uow has not been configured")
        print("see `uow bootstrap --help`")
        raise click.Abort()
    config = SafeConfigParser()
    try:
        config.read(CONFIG_FILE)
    except ConfigParser.ParsingError:
        print("Error reading config file: {0}".format(CONFIG_FILE))
        print("You may fix manually or rerun `uow bootstrap`")
        raise click.Abort()

    try:
        conf_dict = {}
        conf_dict["api_key"] = config.get('api', 'api_key')
        conf_dict["api_end_point"] = config.get('api', 'api_end_point')
        conf_dict["headers"] = {"X-Authentication-Token": conf_dict["api_key"]}
    except ConfigParser.Error:
        print("Error reading config file: {0}".format(CONFIG_FILE))
        print("You may fix manually or rerun `uow bootstrap`")
        raise click.Abort()

    Config = namedtuple("config", ["api_key", "api_end_point", "headers"])
    config = Config(**conf_dict)
    session.headers.update(**conf_dict["headers"])
    return config

def get_uow_info():
    """Walks up the directory tree until it either hits the root level or finds
    a ".uow_info" json file of the correct format

    Will exit if the cwd does not appear to be a uow or a subdir of one.
    
    :returns: a uow_info json and the path to the root of the uow
    """
    last_dir = os.getcwd()
    info_file = None
    if os.path.exists(os.path.join(last_dir, ".uow_info")):
        info_file = os.path.join(last_dir, ".uow_info")
    else:
        while last_dir != os.path.dirname(last_dir):
            last_dir = os.path.dirname(last_dir)
            if os.path.exists(os.path.join(last_dir, ".uow_info")):
                info_file = os.path.join(last_dir, ".uow_info")
                break
    if not info_file:
        print("{} does not seem to be in a uow".format(os.getcwd()))
        raise click.Abort()

    try:
        with open(info_file, 'r') as f:
            uow_info = json.load(f)
    except ValueError:
        print("Invalid uow_info file: {}".format(info_file))
        raise click.Abort()

    if "cruise_id" not in uow_info:
        print("Invalid uow_info file: {}".format(info_file))
        raise click.Abort()
    return uow_info, os.path.dirname(info_file)

def get_fetch_events():
    config, basedir = get_uow_info()

    # The fetch log will not exist if no fetches have been done so check for
    # the specific error no and then return an empty list
    # TODO Clean up this method when we move to python3
    fetch_log_path = os.path.join(basedir, ".fetch_log")
    try:
        with open(fetch_log_path, 'r') as f:
            fetch_log = f.readlines()
    except IOError as e:
        if e.errno == errno.ENOENT:
            return []
        else:
            print(("Error while reading fetch log, please include the following "
                  "traceback with any bug reports:"))
            raise
    # The fetch log is written with one json "object" per line, we also have
    # newlines on either side of the objects, it is also possible for a fetch
    # to have been abborted in the middle of a log write, so we only care about
    # the json objects we can actually read and can safly ignore everything
    # else
    fetch_events = []
    for l in fetch_log:
        try:
            fetch_events.append(json.loads(l))
        except ValueError:
            pass

    # Here we are taking advantage of the both the order of the fetch events
    # (later events come later) and dicts keeping the latest assignment for any
    # given key. This will will have both the latest unique fetches in it.
    unique_events = {}
    for event in fetch_events:
        unique_events[event['id']] = event

    return unique_events.values()
