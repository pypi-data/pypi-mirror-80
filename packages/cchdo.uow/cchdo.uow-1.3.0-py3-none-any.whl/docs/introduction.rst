Introduction
============
The launch of the new API based CCHDO website required both a rewrite and a rethink of how a unit of work and fetch/commits should function.

The cchdo website API is rather low level compared to what may are used to.
It has no concept of what a commit is, it barely has a concept of what a cruise is, and has a slightly stronger concept of what a file is.

Here are some important differences:

* UOW directories are **cruise contexts**
  
  * Everything done inside them is done in the context of the cruise for which is was initialized with.
  * This means all files commited as part of a uow are attached to the cruise

* Multiple files of any particular data type and format may be in a cruises dataset
  
  * Files being replaced must be explicitly marked as "merged"

* Commits **do not occur within a transaction**
  
  * If an API call fails, the commit aborts, however any number of API calls may have already been made, and any number of API calls may have yet to be made
  * Failing in the middle of a commit requries manual fixing.


Getting Started
---------------
The uow command is a packaged collection of python scripts which may be executed like a normal program.
It has no external dependancies.

TODO: Put the packaged program somewhere

Simply grab the program, ensure the executable bit is set and run it.
For convienence, you should put the program somewhere in your ``$PATH``.

Building From Source
--------------------
Get the srouce from (TODO some location), and run ``make`` where the Makefile is.
