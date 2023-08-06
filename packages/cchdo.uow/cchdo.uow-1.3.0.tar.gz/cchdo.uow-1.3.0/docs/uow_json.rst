The uow.json File
=================

Introduction
------------

A ``uow.json`` file must be created in the root of your uow directory.
The file provides the instructions needed to make the correct API calls to accomplish the commit.
It is more explicit than having files "in the right place" or having a program guess the data type by reading the file extention.

As of writing this document, the ``uow.json`` file is not generated automatically.
This chapter describes the ``uow.json`` file and the reasoning behind what is present in it.

This is a blank ``uow.json``:

.. sourcecode:: javascript
  :linenos:

  {
  "files": [
  ],
  "processing_note":{
      "date": "",
      "data_type": "",
      "action":"",
      "summary": "",
      "name": "",
      "notes": ""
    }
  }

It has two basic requried elements: an array for files (line 2-3), and a processing note object (line 4-11).
These are both under a ``files`` and ``processing_note`` key, respectivly.
No other elements are allowed at the root level.

Since the ``files`` array is more complicated, lets discuss the ``processing_note`` first.

The Processing Note
-------------------
With the commit is a processing note which gets attached to the cruise.
This note is described by an object contained within the ``processing_note`` root level key.
The processing note object has the following required keys: ``date``, ``data_type``, ``action``, ``summary``, ``name``, and ``notes``.
No other keys are allowed.

They are as follows:

``date``
  The ``date`` key contains a string with an ISO-8601 date in it.
  This format is ``YYYY-MM-DD``, with zero padded month and days.
  It can be set to any valid date.
  The reccomended value is the commit date.
``data_type``
  The ``data_type`` key contains a string which may contain any valid unicode charicters.
  It is displayed under the "Data Type" field on the website.
  Reccomended values are the paramters that were merged in, or "CrsRpt" in the case of documentation updates.
``action``
  The ``action`` key contains a string which may contain any valid unicode charicters.
  It is displayed under the "Action" field on the website.
  Almost always it is set to "Website Update".
``summary``
  The ``summary`` key contains a string which may contain any valid unicode charicters.
  It is displayed under the "Summary" field on the website.
  It should be a short description of what was done.
  For example, "Updated DOC, TDN, NUTS, bottle data online in all formats".
``name``
  The ``name`` key contains a string which may contain any valid unicode charicters.
  It is displayed under the "Name" field of the website.
  It should be set to the name of the person doing the commit (or however they want to be represented on the website).
``notes``
  The ``notes`` key contains a string which may contain any valid unicode charicters.
  It is displayed under the "Note" field on the website in a ``<pre>`` tag (this means it will appear exactly is).
  The ``notes`` field has some special bahavior if it starts with an ``@`` charicter.

  When the ``notes`` field starts with an ``@`` charicter, the ``uow`` command will interpert the rest of the string as a path to a file.
  The file path is relitave to the root of your uow directory.
  For example, if your processing notes are in a file called ``notes.txt``, the ``notes`` key would contain ``"@notes.txt"``.
  The uow would then look for the ``notes.txt`` file and include it as the note.
  It is reccomended that the any notes be less than 80 characters wide.
  This behavior was inspired by how the ``curl`` command works.

  .. warning::
    If not using a seperate file for the notes, do not start the ``notes`` string with an ``@``.
    Additionally, when not using a seperate file for notes, do not manually write new lines charicters (``\n``).
  
  .. note::
    When designing the cruise JSON object we were faced with the following limitations and tradeoffs when it came to actually storing notes.
    
    JSON does not support multi-line strings, so how should multi-line history notes actualy be stored?
    There were two options, store the notes as single lines with escaped new lines (``\n``) in them, or store the notes as an array of strings where each line of the note is a seperate string in the array.

    There were downsides to both, but the array representation was chosen for human readabiltiy.

The Files Array
---------------
The archetectural changes of the cchdo website allows for new functionality.
One major new feature is the ability to have multiple files of the same "kind" in a cruises dataset.
For example, there can now be two exchange bottle files online.
This new ability means certain actions which were previously implicit can no longer be.
The files array contains objects with information to construct the actions (API calls) of the commit.

File Array Objects
^^^^^^^^^^^^^^^^^^
Each object in the ``files`` array represent a single file to which an action will be done to.
All file objects must contain ``file`` and ``action`` as keys with strings as values.
The ``file`` is the path to the file, relative to the uow directory root.
The ``action`` must a string of either ``new`` or ``merge``.
Let's start with file the ``merge`` action.

The ``merge`` action
********************

Here is a complete file object with the ``merge`` action:

.. sourcecode:: javascript
  :linenos:

    {
      "file":"0.existing_files/4126_BerPolarforsch2002433do.pdf",
      "action":"merge"
    }

The file path is specified under the ``file`` key on line 2.
The action, "merge", is specified on line 3.
No other keys are needed or allowed.

.. note::
  What will happen at commit time?

  When the uow is comitted several actions occur.

  * The path listed in ``file`` will be checked for existance.
  * If the file exists, it will be hashed with sha256.
  * This hash will be searched for in the fetch log.
  * If a fetch event for this file is found, the id and other needed information is extracted to construct the PATCH request that will be emitted.
  * Finally the API itself is asked to ensure that the file already exists on the server.

  If any of the above actions fail, the commit is aborted before any state changing API calls are made.

  Finally, for all the files with the merge action, an HTTP PATCH request is made which changes the files "role" to merged.

The ``new`` action
********************
Comitting files which do not currently exist in the system requires the action of ``new`` to be specified.
There are two types of new files, one which replace one currently in the dataset, and one that is not replaceing anything (a completly new file).

To understand what the ``replaces`` key does, let's first look at completly new file.

Here is complete file object with the ``new`` action:

.. sourcecode:: javascript
  :linenos:

    {
      "file":"1.new_files/ARK-XVII-1_06AQ20010619.txt",
      "action":"new",
      "data_format":"text",
      "data_type":"documentation",
      "role": "dataset"
    }

As with a "merged" files, the path is specified by the ``file`` key on line 2.
The action, "new", is specified on line 3.
A file object which does not have the ``replaces`` key in it, must have these keys present: ``data_format``, ``data_type``, and ``role``.

The ``data_format`` key
```````````````````````
The ``data_format`` key is a string describing the format the data is actually in, allowed values are:

``exchange``
 This is data in exchange format, both plain csv and zip archives containing exchange formatted data should have this as the data format.
``whp_netcdf``
  This is data in the default netCDF format CCHDO uses, the ``whp_`` prefix is to distinguish these files from netCDF files which may conform to some other standard such as OceanSites or CF.
  These files will almost always be zip archives.
``woce``
  This is data in the legacy woce formats for bottle, ctd, and summary.
  This could be both zip archives and plain (ASCII) text.
``text``
  This is data which is simply plain (UTF-8) text.
  Typically only used for the cruise report or other documentation.
``pdf``
  Used exclusivly for any PDF documentation.

The ``data_type`` key
```````````````````````
The ``data_type`` key is a string which describes the kind of data this file is, allowed values are:

``bottle``
  This file represents discrete bottle data.
``ctd``
  This file represents the in situ continious ctd data.
``documentation``
  This file contains human readable documentation.
``summary``
  This file is a legacy woce sum file.
``large_volume``
  This is a "large volume sample" file.
  Usually it is in the the ``woce`` data format.
``trace_metals``
  This is a file containing (only) trace metal data.
  Usually it is in the ``exchange`` data format.
  Trace metals typically occur on seperate casts and tend to be kept seperate from the bottle data.

The ``role`` key
```````````````````````
The ``role`` key is a string which describes how the site should display the file a cruise page, allowed values are:

``dataset``
  This file should be part of the main dataset.
  A file with the dataset role will appear in the "Dataset" section of the website AND be included in any bulk download actions.
``unprocessed``
  An unprocessed file appear in the "Data as Received" section of the website, it will only be publicly available by going to the cruise page.
  This is the role given to user submitted files to make the available as received.
``merged``
  This file should be marked as merged, it will appear in the "Data as Received" section of the wesbite.
  It can only be downloaded by going to the cruise page.
  This is the role given to user submitted files which have been merged into the main dataset.
  It should also be given to files which were in the main dataset but were merged with another file.
``hidden``
  Hidden is just that, the file will be hidden from all but the staff, it will only be accessable through the API.
``archive``
  Archive is the role that was given to the tar files which contain the legacy "data directory".
  It will also be given to the archive containing extra files associated with a commit.
  Generally, this should not be user set.

Let's then look at a file object which has the ``replaces`` key in it, here is a complete file object:

.. sourcecode:: javascript

    {
      "file":"1.new_files/06AQ20010619_do.pdf",
      "action":"new",
      "replaces":"0.existing_files/4126_BerPolarforsch2002433do.pdf"
    }

This object still has ``new`` as the action, but is lacking the ``data_format``, ``data_type``, and ``role`` keys.
The ``replaces`` key contains a string with a file path to a file.
This path must also appear as a seperate file object in the files array containing the ``merge`` action.
When the ``replaces`` key is specified, the uow copies the ``data_format``, ``data_type``, and ``role`` values from the existing file to use for this new one.

.. note::
  What will happen at commit time?

  * All the file objects with the ``new`` action specified are verified to exist at the path specified by ``file``.
  * These files are then hashed with sha256.
  * The ``replaces`` key is looked for, if present, the uow looks for a file object with the same path as the one in ``replaces``

    * If found, the ``data_format``, ``data_type``, and ``role`` values are coppied from the file being replaced.
  * If the ``replaces`` key is not present, the ``data_format``, ``data_type``, and ``role`` keys are searched for.

    * Their values are verfied to be one of the allowed values.
  * A new file json is constructed containing the needed metadata and the file itself base64 encoded.
  * The API is asked to ensure the file DOES NOT already exist in the system.

  If any of the above fail, the commit is aborted before any state modifying API calls are made.

  As the new files are being POSTed to the api, new file IDs are being returned, these are then used to attach the file to the cruise.


The optional ``from`` key
`````````````````````````
Any file object which has the ``new`` action may also have an array of file path strings under the ``from`` key.
This key is intented to allow for a record of what files were involved in the creation of this new file.
Some examples would be two or more files merged to create a new one, or even a zip archive which was simply split apart.

Here is an example of a file object containing a ``from`` key:

.. sourcecode:: javascript
  :linenos:

  {
    "file":"1.new_files/33RR20050106_hy1.csv",
    "action":"new",
    "from":[
      "0.existing_files/2099_33RR20050106.exc.csv",
      "0.existing_files/271_33RR20050106_hy1.csv"
    ],
    "replaces":"0.existing_files/271_33RR20050106_hy1.csv"
  }

The paths listed in the ``from`` key must also exist as seperate file objects in the files array.
At commit time, those files sha256 hashes are simply added to the file json to be committed under the ``file_sources`` key.

The paths in the ``from`` array can be both ``merged`` files or ``new`` files.
For example, a netCDF file created from a newly merged exchnage file would have that exchange file as the ``from`` source.

Here is a complete uow.json example:

.. sourcecode:: javascript
  :linenos:

  {
  "files": [
    {"file":"0.existing_files/2099_33RR20050106.exc.csv",
      "action":"merge"
    },
    {"file":"0.existing_files/2671_33RR20050106_nc_hyd.zip",
      "action":"merge"
    },
    {"file":"0.existing_files/271_33RR20050106_hy1.csv",
      "action":"merge"
    },
    {"file":"0.existing_files/528_LDEO_NGL_CliVarTritium4CCHDO_P16S.xlsx",
      "action":"merge"
    },
    {"file":"0.existing_files/8297_33RR20050106hy.txt",
      "action":"merge"
    },
    {"file":"1.new_files/33RR20050106_hy1.csv",
      "action":"new",
      "from":[
        "0.existing_files/2099_33RR20050106.exc.csv",
        "0.existing_files/271_33RR20050106_hy1.csv"
      ],
      "replaces":"0.existing_files/271_33RR20050106_hy1.csv"
    },
    {"file":"1.new_files/33RR20050106_nc_hyd.zip",
      "action":"new",
      "from":[
        "1.new_files/33RR20050106_hy1.csv"
      ],
      "replaces": "0.existing_files/2671_33RR20050106_nc_hyd.zip"
    },
    {"file":"1.new_files/33RR20050106hy.txt",
      "action":"new",
      "from":[
        "1.new_files/33RR20050106_hy1.csv"
      ],
      "replaces":"0.existing_files/8297_33RR20050106hy.txt"
    }
  ],
  "processing_note":{
      "date": "2015-05-14",
      "data_type": "Bottle",
      "action":"Merge",
      "summary": "Tr Merged",
      "name": "Andrew Barna",
      "notes": "@00README.txt"
    }
  }

In the above example the following has occured:

* Two submitted files were marked as merged (lines 3-4, 12-13).
* Three files already in the dataset were replaced, so they were also marked as merged (lines 6-11, 15-16).
* A new exchange bottle file is to be placed on line, it was merged from the existing dataset file and a submitted file (lines 21, 22).
  It is replacing a file so grab the metadata from the old file (line 24).
* A new netCDF bottle file (lines 26-32) was created from the new exchange file (line 28-30).
  It is replacing a file online to grab the metadata from the old file (line 31).
* A new woce bottle file (lines 33-39) was created from the new exchange file (lines 35-37).
  It is replacing a file online so grab the metadta from the old file (line 38)
* The processing note (lines 41-48) contents are in a seperate file, so use the @path syntax (line 47)


Blank File Object Snippets
--------------------------

Here are some useful blank file objects to construct a uow.json ``files`` array.

Blank Merge File
^^^^^^^^^^^^^^^^

.. sourcecode:: javascript

  {
    "file":"",
    "action":"merge"
  }

Blank New File Replacing
^^^^^^^^^^^^^^^^^^^^^^^^

Without "from" array:

.. sourcecode:: javascript

  {
    "file":"",
    "action":"new",
    "replaces":""
  }

With "from" array:

.. sourcecode:: javascript

  {
    "file":"",
    "action":"new",
    "from":[
      ""
    ],
    "replaces":""
  }

Blank New File
^^^^^^^^^^^^^^

Without "from" array:

.. sourcecode:: javascript

  {
    "file":"",
    "action":"new",
    "role":"",
    "data_format":"",
    "data_type":""
  }

With "from" array:

.. sourcecode:: javascript

  {
    "file":"",
    "action":"new",
    "from":[
      ""
    ],
    "role":"",
    "data_format":"",
    "data_type":""
  }
