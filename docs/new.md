# What's new

### (unreleased)
* Rework doc: set up readthedocs
* Drop python 3.8
* Add python 3.12
* pyOpenSci review process: improve documentation

### v0.4.2 (2023-08-07)
* Allow additional dimension names occurring when variables on inner grid are diagnosed, e.g. `x_grid_U_inner` or `x_grid_U`.
* Add coordinates into the DataArrays
* Add some standard names and units in domcfg

### v0.4.1 (2023-03-29)
* Allow to open files if time bounds are missing
* Minor bug correction for nemo 3.6
* Add nemo 3.6 and 4.2.0 test data
* Update code to support nemo 3.6 and 4.2.0

### v0.4.0 (2022-12-08)
* Optimize speed
* Add option to decode grid type from attributes
* Shift from pipenv and setupy.py to poetry
* Refactor data test to allow testing of multiple version of NEMO

### v0.3.4 (2021-06-15)
* Adding some example
* Bug fixes
* Add option to compute extra scale factors

### v0.3.2 - v0.3.3 (2021-05-05)
* By default adds the lat/lon/depth variables of domcfg as coordinates

### v0.3.1 (2021-05-04)
* Minor bug fix when merging
* better squeezing of time in domcfg + nemo v3.6 compatibility

### v0.3.0 (2021-04-13)
* Cleaning the backend
* Removing the saving options (that were useless and confusing)
* Minor bug fixes
* Tested with realistic regional configuration

### v0.2.3 (2021-03-15)
* Support for surface only files
* Reshaping the data files for the tests (dev)
