# TODO notes for MetReLoad

## Fix
- Case if area is over 180° longitude or around the poles or if user request whole world except area

## Add
- Better error messages for bad coordinates (`MERRA2Dataset.subset()`)
- Add hint that password can be saved to `~/.netrc`
- Check time and location arguments before connecting to data
- Move checking of dates to a function which can be called from multiple places
- Move checking of coordinates to function which can be used from multiple places
