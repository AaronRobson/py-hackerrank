.DEFAULT_GOAL := all

.PHONY: all
all:
	cd synchronous_shopping && $(MAKE) $@

.PHONY: clean
clean:
	cd synchronous_shopping && $(MAKE) $@

.PHONY: install-packages
install-packages:
	cd synchronous_shopping && $(MAKE) $@

.PHONY: check
check:
	cd synchronous_shopping && $(MAKE) $@

.PHONY: check-src
check-src:
	cd synchronous_shopping && $(MAKE) $@

.PHONY: type-check
type-check:
	cd synchronous_shopping && $(MAKE) $@

.PHONY: lint
lint:
	python3 -m pylint .

.PHONY: test
test:
	cd synchronous_shopping && $(MAKE) $@

.PHONY: unittest
unittest:
	cd synchronous_shopping && $(MAKE) $@

.PHONY: unittest-python
unittest-python:
	cd synchronous_shopping && $(MAKE) $@

.PHONY: run
run:
	cd synchronous_shopping && $(MAKE) $@

.PHONY: run-performance-check
run-performance-check:
	cd synchronous_shopping && $(MAKE) $@

.PHONY: graphs
graphs:
	cd synchronous_shopping && $(MAKE) $@
