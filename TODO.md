# TODO notes for MetReLoad

## Fix
- Case if area is over 180° longitude or around the poles or if user request whole world except area

## Add
- Coordinates as command line options
- Better error messages for bad coordinates (`MERRA2Dataset.subset()`)
- Better error messages for unable to connect to MERRA-2 server
- Add hint that password can be saved to `~/.netrc`
- Check time and location arguments before connecting to data