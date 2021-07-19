
test:
	poetry run python -m pytest tests/

test-watch:
	find . -name \*.py | entr poetry run python -m pytest -k tests


build:
	poetry build

coverage:
	poetry run coverage run --source tortoise_data_migration --module pytest tests/
	poetry run coverage xml
	poetry run coverage report
