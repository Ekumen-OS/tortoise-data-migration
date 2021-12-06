# tortoise-data-migration

[![tests](https://github.com/Ekumen-OS/tortoise-data-migration/actions/workflows/tests.yaml/badge.svg)](https://github.com/Ekumen-OS/tortoise-data-migration/actions/workflows/tests.yaml)
[![codecov](https://codecov.io/gh/Ekumen-OS/tortoise-data-migration/branch/main/graph/badge.svg?token=P92AYYHAR1)](https://codecov.io/gh/Ekumen-OS/tortoise-data-migration)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![poetry-managed](https://img.shields.io/badge/poetry-managed-blueviolet)](https://python-poetry.org)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tortoise-data-migration)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/tortoise-data-migration)
[![PyPI](https://img.shields.io/pypi/v/tortoise-data-migration?logo=python)](https://pypi.org/project/tortoise-data-migration/)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/Ekumen-OS/tortoise-data-migration.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Ekumen-OS/tortoise-data-migration/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Ekumen-OS/tortoise-data-migration.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Ekumen-OS/tortoise-data-migration/context:python)


`tortoise-data-migration` is a very simple project meant to perform migrations of data, similar to regular structural migrations.

The main use case is when your system has some "default data" that needs to exist for the system to work. Some examples:
 - The default username/password of a system
 - The default configuration values (if you store the config in the DB)

These values could be set in the system as part of the installation process, but then when writing tests that use those,
you would have to somehow get those values to the DB. So you create a test fixture, and very probably you will be
introducing duplication (the bringup/installation process has these values, and the fixture too).

tortoise-data-migrations are meant to be executed by the software (either during test execution of production) after the
database structure is up-to-date (in production software after running [aerich](https://github.com/tortoise/aerich) migrations for example
or during tests after the DB setup is done), but before the actual software starts executing. That's why
`tortoise-data-migration` is a library and not a command line tool.


## Installation

### Pip

`pip install tortoise-data-migration`

### Pipenv

`pipenv install tortoise-data-migration`

### Poetry

`poetry add tortoise-data-migration`

### PDM

`pdm add tortoise-data-migration`

## Notes for maintainers

### Release

To create a new release, create a github release and a github action will take care of building and publishing. After
that, there will be a PR automatically created to bump the version in `main`.
