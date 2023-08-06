import click

import os
import errno
import json

from . import load_config, session

DIR_NAMES = [
        "0.existing_files",
        "1.new_files",
        "2.processing",
        "3.archive",
        ]


def _load_cruise_list(config):
    """Loads the current cruise list via the API

    :returns: dict with string expocodes as keys and int cruise ids as values
    """

    cruise_list_url = "{api_end_point}/cruise".format(**config._asdict())
    r = session.get(cruise_list_url)
    if not r.status_code == 200:
        print(("Something has gone wrong with the cruise list load, please "
               "include the following with the bug report:"))
        print(r.__dict__)
        raise click.Abort()
    cruises = r.json()["cruises"]
    return {c["expocode"]: c["id"] for c in cruises}

def _get_cruise_id(expocode, cruises):
    try:
        cruise_id = cruises[expocode]
    except KeyError:
        msg = ("Cruise Not Found\n"
               "'{}' does not appear to exist as an expocode at cchdo.\n\n"
               "Some tips:"
               "• Copy the expocode exactly as it appears on the cruise page."
               "• It is case sensitive (318M != 318m)").format(expocode)
        print(msg)
        raise click.Abort()
    
    return cruise_id

def _load_cruise_metadata(config, cruise_id):
    cruise_metadata_url = "{api_end_point}/cruise/{cruise_id}".format(
            cruise_id=cruise_id,
            **config._asdict()
            )

    r = session.get(cruise_metadata_url)
    if not r.status_code == 200:
        print(("Something has gone wrong with the cruise metadata load, please "
               "include the following with the bug report:"))
        print(r.__dict__)
        raise click.Abort()
    return r.json()

def _load_cruise_files(config, cruise_id):
    file_list_url = "{api_end_point}/cruise/{cruise_id}/files".format(
            cruise_id=cruise_id,
            **config._asdict()
            )
    r = session.get(file_list_url)
    if not r.status_code == 200:
        print(("Something has gone wrong with the cruise file list  load, "
               "please include the following with the bug report:"))
        print(r.__dict__)
        raise click.Abort()

    files_dict = {}
    with click.progressbar(r.json()['files'], label="Loading attached file metadata") as file_ids:
        for file_id in file_ids:
            file_url = "{api_end_point}/file/{file_id}".format(
                    file_id=file_id,
                    **config._asdict()
                    )
            r = session.get(file_url)
            if not r.status_code == 200:
                print(("Something has gone wrong with the cruise file list load, "
                       "please include the following with the bug report:"))
                print(r.__dict__)
                raise click.Abort()
            files_dict[file_id] = r.json()
    return files_dict

def _make_uow_dirs(base_name):
    for sub_dir in DIR_NAMES:
        path = os.path.join(base_name, sub_dir)
        try:
            os.makedirs(path, 0o755)
        except OSError:
            print("Could not create UOW directory")
            print("Most common cause of this is the directory already existing.")
            raise click.Abort()

def _write_uow_cache(base_name, cruise_id, cruise_meta, file_meta):
    path = os.path.join(base_name, ".uow_info")
    uow_info = {
            "cruise_id": cruise_id,
            "cruise_metadata": cruise_meta,
            "file_metadata": file_meta
            }
    with open(path, 'w') as f:
        json.dump(uow_info, f)

def do_init(expocode, dir_name):
    """Create a UOW directory
    """
    config = load_config()
    cruises = _load_cruise_list(config)
    cruise_id = _get_cruise_id(expocode, cruises)
    cruise_metadata = _load_cruise_metadata(config, cruise_id)
    cruise_files = _load_cruise_files(config, cruise_id)
    _make_uow_dirs(dir_name)
    _write_uow_cache(dir_name, cruise_id, cruise_metadata, cruise_files)
