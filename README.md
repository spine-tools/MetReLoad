# MetReLoad

[![Documentation Status](https://readthedocs.org/projects/metreload/badge/?version=latest)](https://metreload.readthedocs.io/en/latest/?badge=latest)

Python application for downloading meteorological reanalysis data

## Installation

Python 3 is required. A [conda environment](https://conda.io/docs/user-guide/tasks/manage-environments.html)  or a [virtual environment](https://docs.python.org/3/library/venv.html) is recommended. 

Install required packages with

    pip install -r requirements.txt

Install MetReLoad with

    pip install .

## Usage

    metreload [OPTIONS] COMMAND [OPTIONS]...

### General options

```
--version  Show version and exit
--debug    Set debug mode on
--help     Show this message and exit.
```
  
See documentation in folder `docs` for more information.

## Contributing

Install development requirements into your current Python environment with

    pip install -r requirements.txt -r requirements_dev.txt

Alternatively, if you are using conda you can also create a new development environment with

    conda env create --file conda/develop.yml --name <NAME>

Install the package in editable mode with

    pip install -e .

Before committing, run tests with

    python setup.py test

### Building with PyInstaller

PyInstaller version 3.4 (or newer) is required. 
Follow above instructions to install all development requirements (including PyInstaller).
Excute 

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