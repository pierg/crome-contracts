SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run doc8 -q docs
	poetry run black crome_contracts tests/**/*.py
	poetry run pyupgrade
	poetry run pycln crome_contracts tests/**/*.py --all
	poetry run autoflake .
	poetry run isort .
	poetry run autopep8 --in-place -r crome_contracts tests/**/*.py
	poetry run docformatter --in-place -r crome_contracts tests/**/*.py
	poetry run yapf -ir .
# 	poetry run mypy crome_contracts tests/**/*.py
# 	poetry run bandit -r crome_contracts
	poetry run flake8 crome_contracts

.PHONY: unit
unit:
	poetry run pytest

.PHONY: package
package:
	poetry check
	poetry run pip check
	poetry run safety check --full-report

.PHONY: test
test: lint package unit
