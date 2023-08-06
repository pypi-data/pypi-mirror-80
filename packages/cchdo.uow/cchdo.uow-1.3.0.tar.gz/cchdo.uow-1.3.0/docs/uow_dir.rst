A uow Directoy
==============
When a uow directory is initialized, several empty directories and a file is created.


Subdirectories of a uow
-----------------------

0.existing_files
  Any files fetched wtit the ``uow fetch`` command will be downloaded here.
  Generally, it should not be modified, copy the files out of here when needed.
1.new_files
  A convienence directory to place new files to go online, files placed in this are not automatically put online when a commit is done
2.processing
  A convienvece directory to do work in.
4.archive
  Place any files in here should just be attached as part of the commit (custom scripts for example).

  .. danger::
    This archive feature is not yet implimented.
    Nothing happens with this directory.

Dotfiles of a uow
-----------------

Several "dot files" will also be created in a uow directories lifetime:

.uow_info
  This is a JSON file which contains information about the uow context.
  It has the cruise json object, and all the file json objects which are attached to that cruise.
  This files existance is used to display the available files with the ``uow list`` command.
  It is also used to determine if the current working directory is a uow or a subdirectory of one.
.fetch_log
  When any file is fetched, its entire (and current) json metadata object is logged to this file.
.api_call_log
  When an actual commit is done, all the API calls are logged to this file, to be used for debugging if anything goes wrong.
.committed
  When a commit occurs, this file is touched and will contain the text "DONE".
  Its presnce will stop any commit from occuring

.. danger::
  Do not delete or modify any of these files.
