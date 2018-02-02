# default python version. For using python2, use:
# PY=2 make test
PY      ?= 3
PACKAGE := pyosm
VENV    := venv

.PHONY: test
test:
	py.test-$(PY)

.PHONY: doctest
doctest:
	find $(PACKAGE) -name '*.py' -print | xargs python$(PY) -m doctest
	python$(PY) -m doctest README.md

$(VENV):
	virtualenv -p /usr/bin/python$(PY) $(VENV)

.PHONY: init-dev
init-dev:
	pip$(PY) install -U -r requirements-dev.txt
	pip$(PY) install -U --editable .

.PHONY: install-user
install-user:
	python$(PY) setup.py install --user

.PHONY: uninstall
uninstall:
	pip$(PY) uninstall $(PACKAGE)

.PHONY: install
	python$(PY) setup.py install

.PHONY: clean
clean:
	# clean setuptools stuff
	rm -rf build dist $(PACKAGE).egg-info
	# clean python2-stuff
	find ./ -name '*.pyc' -delete
	# clean python3-stuff
	find ./ -name __pycache__ -type d -print | xargs rm -r

.PHONY: archive
archive:
	python setup.py sdist
