

install-dependencies:
	pdm install --no-lock

test:
	pdm run python -m unittest

build:
	pdm build

coverage:
	pdm run coverage run --source tortoise_data_migration --module unittest discover
	pdm run coverage xml
