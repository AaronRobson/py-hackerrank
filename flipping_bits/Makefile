.DEFAULT_GOAL := all

.PHONY: all
all: check test

.PHONY: install-packages
install-packages:
	python3 -m pip install --upgrade \
	  -r test-requirements.txt

.PHONY: check
check: check-src type-check lint

.PHONY: check-src
check-src:
	python3 -m flake8 .

.PHONY: type-check
type-check:
	python3 -m mypy .

.PHONY: lint
lint:
	python3 -m pylint .

.PHONY: test
test: unittest

.PHONY: unittest
unittest: unittest-python

.PHONY: unittest-python
unittest-python:
	python3 -m unittest -v $(testcase)