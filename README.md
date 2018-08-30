# MetReLoad
Python application for downloading meteorological reanalysis data

## Installation

Install requirered packages with

    pip install -r requirements.txt
   
Install MetReLoad with

    pip install [-e] .


## Usage

    metreload [OPTIONS] COMMAND [ARGS]...


Option | Functionality
--- | ---
`--version` | Show version and exit
`--debug` | Set debug mode on
`--help`  | Show this message and exit.


Command | Functionality 
--- | ---
`merra2`  | Download MERRA-2 data
