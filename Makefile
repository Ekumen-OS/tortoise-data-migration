

install-dependencies:
	pdm install --no-lock

test:
	pdm run python -m unittest

build:
	pdm build
