.PHONY: init
init:
	pip install --upgrade pip tox pre-commit
	pip install --upgrade -e ".[dev]"
	pip install --group docs
	pre-commit install
