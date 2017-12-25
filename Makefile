.PHONY: test
test:
	pytest-3

.PHONY: init
init:
	pip3 install -r requirements.txt
