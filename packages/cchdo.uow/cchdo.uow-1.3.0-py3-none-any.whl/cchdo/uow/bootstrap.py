import os
import errno
from configparser import ConfigParser

from click import prompt

from . import CONFIG_DIR, CONFIG_FILE, API_ENDPOINT

def _ensure_config_dir(path):
    try:
        os.makedirs(path, 0o700)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def do_bootstrap():
    """Interactivly set up the config file

    This command will create (or recreate) the config file used by the uow
    program. It will ask for two peices of information:

    1. The API end point.

    2. Your api key (find this at https://cchdo.ucsd.edu/staff/me)

    It will then write this to the config file at:
    ~/.config/hdo_uow/config

    It will create any intermediate directories as needed.
    """
    end_point_location = prompt("API end point", default=API_ENDPOINT)
    if end_point_location.strip() == "":
        end_point_location = API_ENDPOINT

    api_key = prompt("Your API Key")

    try:
        _ensure_config_dir(CONFIG_DIR)
    except:
        print("Something has gone wrong with the creation of the config file directory")
        raise
    print("Writing config")
    config = ConfigParser()
    config.add_section('api')
    config.set('api', 'api_end_point', end_point_location)
    config.set('api', 'api_key', api_key)
    with open(CONFIG_FILE, 'w') as f:
            config.write(f) 
