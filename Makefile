.DEFAULT_GOAL := all

.PHONY: all
all: check test

.PHONY: clean
clean:
	rm -f *.pyc

.PHONY: install-packages
install-packages:
	pip3 install --upgrade \
	  -r dev-requirements.txt \
	  -r requirements.txt

.PHONY: check
check: check-src type-check lint

.PHONY: check-src
check-src:
	flake8 .

.PHONY: type-check
type-check:
	mypy .

.PHONY: lint
lint:
	pylint synchronous_shopping.py

.PHONY: test
test: unittest

.PHONY: unittest
unittest: unittest-python

.PHONY: unittest-python
unittest-python:
	python3 -m unittest -v $(testcase)

.PHONY: run
run:
	python3 run_performance_check.py
