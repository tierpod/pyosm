# default python version. For using python2, use:
# PYTHON_VER=2 make test
PYTHON_VER ?= 3

.PHONY: test
test:
	py.test-$(PYTHON_VER)

.PHONY: doctest
doctest:
	python$(PYTHON_VER) -m doctest pymetatile/*.py README.md

.PHONY: init-dev
init-dev:
	pip$(PYTHON_VER) install -r requirements-dev.txt

.PHONY: install-user
install-user:
	python$(PYTHON_VER) setup.py install --user

.PHONY: uninstall
uninstall:
	pip$(PYTHON_VER) uninstall pymetatile

.PHONY: install
	python$(PYTHON_VER) setup.py install

.PHONY: clean
clean:
	# clean setuptools stuff
	rm -rf build dist pymetatile.egg-info
	# clean python2-stuff
	find ./ -name '*.pyc' -delete
	# clean python3-stuff
	rm -rf pymetatile/__pycache__
