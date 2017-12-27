.PHONY: test
test:
	py.test-3

.PHONY: doctest
doctest:
	python3 -m doctest pymetatile/*.py

.PHONY: init-dev
init-dev:
	pip3 install -r requirements-dev.txt

.PHONY: install-user
install-user:
	python3 setup.py install --user

.PHONY: uninstall
uninstall:
	pip3 uninstall pymetatile

.PHONY: install
	python3 setup.py install

.PHONY: clean
clean:
	# clean setuptools stuff
	rm -rf build dist pymetatile.egg-info
	find ./ -name '*.pyc' -delete
