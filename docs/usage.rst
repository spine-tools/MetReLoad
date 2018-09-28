.. _usage:

Usage
=====

::
   metreload [OPTIONS] COMMAND [OPTIONS]...


General options
~~~~~~~~~~~~~~~

--version  Show version and exit
--debug    Set debug mode on
--help     Show this message and exit.

The ``merra2`` command
----------------------

Download MERRA-2 data. Note: You first need to `register with NASA
Earhdata <https://disc.gsfc.nasa.gov/data-access>`_. Downloaded data will
be saved as netCDF-4 files, one file per day, with filenames of format
``MERRA-2.<COLLECTION ID>.<DATE>.SUB.nc4``.

Options
~~~~~~~
-c, --collection TEXT  Name of MERRA-2 collection (nine-character ESDT code)
-U, --username TEXT    Username [default: <system username>]
--password TEXT        Password
-o, --output-dir PATH  Output directory  [default: .]
--start-time DATE      Start date (YYYY-MM-DD)
--end-time DATE        End date (YYYY-MM-DD)
--variables LIST       Comma separated list of variable names
--location ARG         Comma separated list of coordinates either (lat,lon
                       or north,west,south,east) or path to shapefile
--help                 Show help and exit.

Refer to `MERRA-2 file
specification <https://gmao.gsfc.nasa.gov/pubs/docs/Bosilovich785.pdf>`_
for the names of data collections.
