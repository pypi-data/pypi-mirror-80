The uow command
===============

The uow "binary" is a packaged python program.
When examinied with ``less`` or ``strings`` you should notice the first line is a stadard script decliaration.
It is then followed by zip data, python is able to execute the scripts contained within the zip archive.

The usage of the uow program is divided into several subcommands.

The ``bootstrap`` subcommand
----------------------------
Before any uow directories can be created, the program needs to be configured with two basic peices of information:

* The api end point.
* Your api key (find this on https://cchdo.ucsd.edu/staff/me)

It then creates and writes the uow config file to a sub directory of ``~/.config``.
The config file itself is simple YAML.

.. warning::
  The bootstrap process does not check to see if the api end point exists, or if your api key is valid.
  It only creates the config file.

The ``init`` subcommand
----------------------------
The init subcommand is what actually creates a uow directory.
It has two options:

* ``-e``, ``--expocode`` is the expocode of the cruise you want to create a uow directory for.
* ``-d``, ``--dir_name`` is the name of the directory which will be created.

If any option is not specified, it will be prompted for.

The uow directory name will be exactly as specified, there is no more implicit naming.

When run, the init subcommand will create the requestd uow direcory and all the default subdirectories.
It will also GET the the cruise object refered by the given ``expocode`` and a list of files attached to this cruise.

.. note::
  Unlike previous versions of the "fetch/commit" programs, files cannot be specified at uow directory creation time.
  No files are downloaded as part of the init process.

The ``list`` subcommand
----------------------------
The list subcommand shows information on the files attached to the cruise the uow directory is for.
The one positional argument specifies how to filter the list for display.
Allowed values are:

``all``
  Lists all the files attached to the cruise
``dataset``
  Lists only the files which have the role ``dataset``
``unprocessed``
  Lists only the files which have the role ``unprocessed``.
  This is equivalent to the "queue files" of the older systems.
``merged``
  Lists only files which have the role of ``merged``.
``other``
  Lists files which have a role other than ``dataset``, ``unprocessed``, or ``merged``.
  This would be non public files for argo, archive files, or hidden files.

The ``id`` listed by the list subcommand is what should be given to the ``fetch`` subcommand to download a file.

The ``info`` subcommand
----------------------------
The list subcommand shows the entire json object for the cruise or requested file id.
The one optional positional argument specifies the file json object to display.

If the file id is omitted, the cruise object for the current uow context is printed to stdout.
These can be very long so it is recommended that this output be piped to your pager of choice.

The ``id`` listed by the list subcommand is what should be given to the ``info`` subcommand to view a file json object.

The ``fetch`` subcommand
----------------------------
The fetch subcommand is used to actually download files to the 0.existing_files subdirectory in the uow directory.

It takes one or more file ids as positional arguments.

It has two optional arguments:

``--external``
  By default, the fetch subcommand will not allow fetching files not already attached to the cruise the uow is for.
  To override this limitation, simply include the ``--external`` flag.
  Before doing so, consider if the file should be attached to the cruise and perhaps do that first.

  .. note::
    The fetch subcommand only knows which files were attached to the cruise at the time of the ``init`` command.
    It will consider all files attached to the cruise after the uow was created to be external files.

``--panic``
  Sometimes the data is so strange, you just need to grab all the files and sort through them manually.
  Of particular interest will be the ``archive.tar`` file, as this is the pre pycchdo data directory.

The ``status`` subcommand
-------------------------
The status subcommnad shows several useful bits of information:

* a list of files which have been fetched and if they are still present and unmodified
* if a uow.json is present, it will be validated
* if a valid uow.json is present, the anticipated results of a commit based on it will be listed

The status subcommand has no positional or optional arguments (other than help).

The ``commit`` subcommand
-------------------------
The commit subcommand actually performs the commit.
It will do all the checks done by the status command.
Additionally, it will query the API to see if files which should already exist do, and files shich should not exist do not.

It has no positional or optional arguments (except for help).

After displaying the anticipated results of the commit, it will ask for confirmation to continue, any non "yes" response will abort the commit.

.. danger::
  Do not abort the commit after saying "yes" to continue.
  Depending on how large the files to commit are, and what the bandwidth is, it may take a very lone time to complete.
  
  Aborting a commit will cause any files which have already made it to the website to be orphaned.

.. danger::
  If anything goes wrong, a dump of the last api call will be printed to stdout, include it with any bug reports.

.. danger::
  Any interuption of the commit after saying "yes" to conintue will require manual fixing.
