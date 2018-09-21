# MetReLoad
Python application for downloading meteorological reanalysis data

## Installation

Python 3 is required. A [conda environment](https://conda.io/docs/user-guide/tasks/manage-environments.html)  or a [virtual environment](https://docs.python.org/3/library/venv.html) is recommended. 

Install required packages with

    pip install -r requirements.txt

Install MetReLoad with

    pip install [-e] .

Use the `-e` switch if you want an editable copy (for development).

## Usage

    metreload [OPTIONS] COMMAND [OPTIONS]...


##### General options

```
--version  Show version and exit
--debug    Set debug mode on
--help     Show this message and exit.
```
  
### Commands  
#### `merra2`  

Download MERRA-2 data. Note: You first need to register with NASA Earhdata, see instructions [here](https://disc.gsfc.nasa.gov/data-access).

##### Options
```
-c, --collection TEXT  Name of MERRA-2 collection (nine-character ESDT code)
-U, --username TEXT    [default: ererkka]
--password TEXT
-o, --output-dir PATH  Output directory  [default: .]
--start-time DATE      Start date (YYYY-MM-DD)
--end-time DATE        End date (YYYY-MM-DD)
--variables LIST       Comma separated list of variable names
--location ARG         Comma separated list of coordinates either (lat,lon
                       or north,west,south,east)or path to shapefile
--help                 Show this message and exit.
```

Refer to [MERRA-2 file specification](https://gmao.gsfc.nasa.gov/pubs/docs/Bosilovich785.pdf) for the names of data collections.


## Contributing

Install development requirements into your current Python environment with

    pip install -r requirements.txt -r requirements_dev.txt

Alternatively, if you are using `conda` you can also create a new development environment with

    conda env create --file conda/develop.yml --name <NAME>

Install the package in editable mode with

    pip install -e .

Before committing, run tests with

    python setup.py test

### Building with PyInstaller

PyInstaller version 3.4 is required. Excute 

    pyinstaller [-y] metreload.spec

to build an executable distribution into `dist/metreload`. (Use the `-y` switch to bypass confirmation for replacing old files.)

&nbsp;
<hr>
<center>
<table width=500px frame="none">
<tr>
<td valign="middle" width=100px>
<img src=https://europa.eu/european-union/sites/europaeu/files/docs/body/flag_yellow_low.jpg alt="EU emblem" width=100%></td>
<td valign="middle">This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 774629.</td>
</table>
</center>