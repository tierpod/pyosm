.PHONY: test
test:
	pytest-3

.PHONY: doctest
doctest:
	python3 -m doctest -v pymetatile/__init__.py

.PHONY: init
init:
	pip3 install -r requirements.txt
