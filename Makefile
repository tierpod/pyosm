.PHONY: test
test:
	pytest-3

.PHONY: doctest
doctest:
	python3 -m doctest -v pymetatile/__init__.py

.PHONY: init
init:
	pip3 install -r requirements.txt

.PHONY: install-user
install-user:
	python3 setup.py install --user

.PHONY: clean
clean:
	# clean setuptools stuff
	rm -rf build dist pymetatile.egg-info
