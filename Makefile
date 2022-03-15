.PHONY: init
init:
	pip install --upgrade pip tox pre-commit
	pip install --upgrade -e ".[dev]"
	pre-commit install
