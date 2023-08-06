<!-- Landscape | [![Code Health](https://landscape.io/github/duniter/sakia/dev/landscape.svg?style=flat)](https://landscape.io/github/duniter/sakia/dev) -->

![sakia logo](https://raw.github.com/duniter/sakia/master/sakia.png)

# Sakia
 [![coverage report](https://git.duniter.org/clients/python/sakia/badges/gitlab/coverage.svg)](https://git.duniter.org/clients/python/sakia/commits/gitlab)
 [![pipeline status](https://git.duniter.org/clients/python/sakia/badges/gitlab/pipeline.svg)](https://git.duniter.org/clients/python/sakia/commits/gitlab)
 [![Build Status](https://travis-ci.org/duniter/sakia.svg?branch=travis)](https://travis-ci.org/duniter/sakia)
 [![Build status](https://ci.appveyor.com/api/projects/status/pvl18xon8pvu2c8w/branch/dev?svg=true)](https://ci.appveyor.com/project/Insoleet/sakia-bee4m/branch/dev)

========

Python3 and PyQt5 Client for [duniter](http://www.duniter.org) project.


### Features
  * Accounts management
  * Communities viewing
  * Money Transfer
  * Wallets management
  * Contacts management
  * Joining a community, publishing keys
  * Multiple wallets management

### Dependencies
  * Dependencies :
   * Qt5
   * [python3](https://www.python.org/downloads/)
   * [libsodium](http://doc.libsodium.org/installation/README.html)

  * General tips : use pyenv to build sakia, as described in the [wiki](https://github.com/duniter/sakia/wiki/Cutecoin-install-for-developpers)

  Building python 3 with pyenv requires libraries of `openssl` and `sqlite3`. On Ubuntu, install it using the following commands : 

```
apt-get update
apt-get install libssl-dev
apt-get install libsqlite3-dev
```

### Wheel Build scripts
  * Install __wheel__ with `pip install wheel`
  * Run `python3 gen_resources.py` in sakia folder
  * Run `python3 gen_translations.py` in sakia folder
  * To build the wheel : Run `python3 setup.py bdist_wheel` in sakia folder
  
### Pyinstaller Build scripts
  * Install __pyinstaller__ with `pip install pyinstaller`
  * Run `python3 gen_resources.py` in sakia folder
  * Run `python3 gen_translations.py` in sakia folder
  * To build the binaries : Run `pyinstall sakia.spec`

### Install with pip
  * Run `pip install sakia`
  * start "sakia" :)
 
### Download latest release
  * Go to [current release](https://github.com/duniter/sakia/releases)
  * Download corresponding package to your operating system
  * Unzip and start "sakia" :)
  * Join our beta community by contacting us on [duniter forum](http://forum.duniter.org/)

## Command line options

`-d` to display log to debug

`--currency g1-test` to connect to the g1-test currency network.

## Development
* When writing docstrings, use the reStructuredText format recommended by https://www.python.org/dev/peps/pep-0287/#docstring-significant-features
* Use make commands to check the code and the format it correct.

The development tools require Python 3.6.x or higher.

* Create a python virtual environment with [pyenv](https://github.com/pyenv/pyenv)
```bash
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

* Install dependencies
```bash
pip install -r requirements.txt
```

* Run Sakia from the source code
```bash
PYTHONPATH="`pwd`/src/." python src/sakia/main.py
```

* Before submiting a merge requests, please check the static typing and tests.

* Install dev dependencies
```bash
pip install -r requirements_dev.txt
```

* Check static typing with [mypy](http://mypy-lang.org/)
```bash
make check
```

* Run all unit tests (pytest module) with:
```bash
make tests
```
> **Warning:** *do not run tests with sakia installed in your dev environment, because pytest will use the installed Sakia.*

* Run only some unit tests by passing a special ENV variable:
```bash
make tests TESTS_FILTER=tests/functional/test_transfer_dialog.py::test_transfer
```

## Packaging and deploy
### PyPi
In the development pyenv environment, install the tools to build and deploy
```bash
pip install --upgrade -r requirements_deploy.txt
```

Change and commit and tag the new version number (semantic version number)
```bash
./release.sh 0.x.y
```

Build the PyPi package in the `dist` folder
```bash
make build
```

Deploy the package to PyPi test repository (prefix the command with a space in order for the shell not to save in its history system the command containing the password)
```bash
[SPACE]make deploy_test PYPI_TEST_LOGIN=xxxx PYPI_TEST_PASSWORD=xxxx
```

Install the package from PyPi test repository
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/simple/ sakia
```

Deploy the package on the PyPi repository (prefix the command with a space in order for the shell not to save in its history system the command containing the password)
```bash
[SPACE]make deploy PYPI_LOGIN=xxxx PYPI_PASSWORD=xxxx
```

## License
This software is distributed under [GNU GPLv3](https://raw.github.com/duniter/sakia/dev/LICENSE).
