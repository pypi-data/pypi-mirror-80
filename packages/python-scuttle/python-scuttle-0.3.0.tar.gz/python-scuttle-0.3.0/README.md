# python-scuttle

![tests](https://github.com/scuttle/python-scuttle/workflows/tests/badge.svg)
[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python wrapper around [SCUTTLE](https://github.com/scuttle/scuttle) API.

## Installation

To install the latest release from PyPI:

```shell
pip install python-scuttle
```

Or, to install the latest commit to master from source:

```shell
pip install -e git+https://github.com/scuttle/python-scuttle.git
```

## Usage

Check out the [wiki](https://github.com/scuttle/python-scuttle/wiki/API-v1) for
theoretical usage and concept explanation, or the tests for live usage.

Current SCUTTLE API documentation can be found on [its
wiki](http://scuttle.wikidot.com/api). As of writing, all methods are
reproduced with similar names.

## Testing

Install [Pipenv](https://pypi.org/project/pipenv/) and development
dependencies:

```shell
pipenv install --dev
```

Run tests in pipenv environment:

```shell
pipenv run pytest
```

Tests require a SCUTTLE API key with full read permissions. Tests will look for
this key in the `SCUTTLE_API_KEY` environment variable. Tests require at least
Python 3.8.
