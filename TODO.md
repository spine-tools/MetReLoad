# TODO notes for MetReLoad

## Fix
- Only show debug messages if debug mode is on
- Case if area is over 180° longitude or around the poles or if user request whole world except area
- Variables argument for MERRA-2 should be given like `--variables xxx,yyy,zzz`

## Add
- Coordinates as command line options
- Better error messages for bad coordinates (`MERRA2Dataset.subset()`)
- Better error messages for unable to connect to MERRA-2 server
- Add hint that password can be saved to `~/.netrc`
- Check time and location arguments before connecting to data
- Move checking of dates to a function which can be called from multiple places
- Move checking of coordinates to function which can be used from multiple places
- Add help to coordinates and time options (merra2)
