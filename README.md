# MetReLoad
Python application for downloading meteorological reanalysis data

## Installation

A [conda environment](https://conda.io/docs/user-guide/tasks/manage-environments.html)  or a [virtual environment](https://docs.python.org/3/library/venv.html) is recommended. Install required packages with

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

Download MERRA-2 data

##### Options
```
  -c, --collection TEXT  Name of MERRA-2 collection (nine-character ESDT code)
  -U, --user TEXT        Username
  --password TEXT
  -o, --output-dir TEXT  Output directory
  --help                 Show this message and exit.
```


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