.DEFAULT_GOAL := all

.PHONY: all
all:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@
	cd fibonacci_modified && $(MAKE) $@
	cd kittys_calculations_on_a_tree && $(MAKE) $@

.PHONY: clean
clean:
	cd synchronous_shopping && $(MAKE) $@
	# cd flipping_bits && $(MAKE) $@
	# cd coin_change && $(MAKE) $@
	# cd fibonacci_modified && $(MAKE) $@
	# cd kittys_calculations_on_a_tree && $(MAKE) $@

.PHONY: install-packages
install-packages:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	# cd coin_change && $(MAKE) $@
	# cd fibonacci_modified && $(MAKE) $@
	cd kittys_calculations_on_a_tree && $(MAKE) $@

.PHONY: check
check:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@
	cd fibonacci_modified && $(MAKE) $@
	cd kittys_calculations_on_a_tree && $(MAKE) $@

.PHONY: check-src
check-src:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@
	cd fibonacci_modified && $(MAKE) $@
	cd kittys_calculations_on_a_tree && $(MAKE) $@

.PHONY: type-check
type-check:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@
	cd fibonacci_modified && $(MAKE) $@
	cd kittys_calculations_on_a_tree && $(MAKE) $@

.PHONY: lint
lint:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@
	cd fibonacci_modified && $(MAKE) $@
	cd kittys_calculations_on_a_tree && $(MAKE) $@

.PHONY: test
test:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@
	cd fibonacci_modified && $(MAKE) $@
	cd kittys_calculations_on_a_tree && $(MAKE) $@

.PHONY: unittest
unittest:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@
	cd fibonacci_modified && $(MAKE) $@
	cd kittys_calculations_on_a_tree && $(MAKE) $@

.PHONY: unittest-python
unittest-python:
	cd synchronous_shopping && $(MAKE) $@
	cd flipping_bits && $(MAKE) $@
	cd coin_change && $(MAKE) $@
	cd fibonacci_modified && $(MAKE) $@
	cd kittys_calculations_on_a_tree && $(MAKE) $@

.PHONY: run
run:
	cd synchronous_shopping && $(MAKE) $@
	# cd flipping_bits && $(MAKE) $@
	# cd coin_change && $(MAKE) $@
	# cd fibonacci_modified && $(MAKE) $@
	# cd kittys_calculations_on_a_tree && $(MAKE) $@

.PHONY: run-performance-check
run-performance-check:
	cd synchronous_shopping && $(MAKE) $@
	# cd flipping_bits && $(MAKE) $@
	# cd coin_change && $(MAKE) $@
	# cd fibonacci_modified && $(MAKE) $@
	# cd kittys_calculations_on_a_tree && $(MAKE) $@

.PHONY: graphs
graphs:
	cd synchronous_shopping && $(MAKE) $@
	# cd flipping_bits && $(MAKE) $@
	# cd coin_change && $(MAKE) $@
	# cd fibonacci_modified && $(MAKE) $@
	# cd kittys_calculations_on_a_tree && $(MAKE) $@
