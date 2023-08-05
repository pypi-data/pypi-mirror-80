.PHONY: install
install:
	pip3 install . --upgrade

.PHONY: build
build:
	rm -rf dist
	python3 setup.py sdist bdist_wheel

.PHONY: upload
upload: build
	python3 -m twine upload dist/*

.PHONY: unittest
unittest:
	PYTHONPATH=$(PYTHONPATH):tap_file python3 -m unittest discover -s test -v

.PHONY: lint
lint:
	flake8 tap_file test
