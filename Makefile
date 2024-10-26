.DEFAULT_GOAL := all

.PHONY: all
all:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@

.PHONY: clean
clean:
	cd synchronous_shopping && $(MAKE) $@
	# cd flipping_bits && $(MAKE) $@
	# cd coin_change && $(MAKE) $@

.PHONY: install-packages
install-packages:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	# cd coin_change && $(MAKE) $@

.PHONY: check
check:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@

.PHONY: check-src
check-src:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@

.PHONY: type-check
type-check:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@

.PHONY: lint
lint:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@

.PHONY: test
test:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@

.PHONY: unittest
unittest:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@

.PHONY: unittest-python
unittest-python:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@

.PHONY: run
run:
	cd synchronous_shopping && $(MAKE) $@
	# cd flipping_bits && $(MAKE) $@
	# cd coin_change && $(MAKE) $@

.PHONY: run-performance-check
run-performance-check:
	cd synchronous_shopping && $(MAKE) $@
	# cd flipping_bits && $(MAKE) $@
	# cd coin_change && $(MAKE) $@

.PHONY: graphs
graphs:
	cd synchronous_shopping && $(MAKE) $@
	# cd flipping_bits && $(MAKE) $@
	# cd coin_change && $(MAKE) $@