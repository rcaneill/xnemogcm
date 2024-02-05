## Requirements for dev

We use *poetry* to set up a virtual environment containing all
needed packages to run xnemogcm and the tests.
To install all the dependencies, type `poetry install --with test,dev,docs`
after cloning the directory. This will create a new virtual environment.
Typing `poetry shell` in the package directory will activate the virtual environment.

## About test data

Test data are based on the GYRE configuration, and produced by another repository:
[rcaneill/xnemogcm_test_data](https://github.com/rcaneill/xnemogcm_test_data).
Testing is built in a way that it is quite easy to add other nemo version to test.
