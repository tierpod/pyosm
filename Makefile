PY      ?= 3
PACKAGE := pyosmkit
VENV    := venv

.PHONY: test
test:
	py.test

.PHONY: doctest
doctest:
	find $(PACKAGE) -name '*.py' -print | xargs python -m doctest
	python$(PY) -m doctest README.md

$(VENV):
	python$(PY) -m venv $@

.PHONY: init-dev
init-dev:
	python$(PY) -m pip install -U -r requirements-dev$(PY).txt
	python$(PY) -m pip install -U --editable .

.PHONY: install
	python$(PY) setup.py install

.PHONY: clean
clean:
	# clean setuptools stuff
	rm -rf build dist *.egg-info
	# clean python stuff
	find ./ -name '*.pyc' -delete
	find ./ -name __pycache__ -type d -print | xargs rm -rf

.PHONY: archive
archive:
	python$(PY) setup.py sdist bdist_wheel

.PHONY: pypi-test-upload
pypi-test-upload:
	twine upload --repository testpypi dist/*

.PHONY: pypi-upload
pypi-upload:
	twine upload --repository pypi dist/*
