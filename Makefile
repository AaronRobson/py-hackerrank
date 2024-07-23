.DEFAULT_GOAL := all

DOT?=neato

.PHONY: all
all: check test graphs

.PHONY: clean
clean:
	rm -f *.pyc *.dot *.gv *.bmp *.jpeg *.jpg *.pdf *.png *.pic *.ps *.svg

.PHONY: install-packages
install-packages:
	python3 -m pip install --upgrade \
	  -r dev-requirements.txt \
	  -r requirements.txt

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
	python3 -m pylint

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

%.gv : %.txt
	cat $< | python3 generate_graph.py > $@

%.svg : %.gv
	$(DOT) -Tsvg -o $@ $<

%.png : %.gv
	$(DOT) -Tpng -o $@ $<

SRC_FILES=$(wildcard input*.txt)
GZ_FILES=$(SRC_FILES:.txt=.gv)
OUT_FILES=$(GZ_FILES:.gv=.svg)

.PHONY: listtargets
listtargets:
	@echo $(OUT_FILES)

.PHONY: graphs
graphs: $(OUT_FILES)
