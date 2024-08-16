# Contains basic auxiliary commands for working with a project.

# run linters
lint:
	ruff check . --config=pyproject.toml --fix

# run tests
test:
	pytest -vv -p no:warnings

# run API
api:
	uvicorn --port 8000 --host 127.0.0.1 src.main:app --reload
