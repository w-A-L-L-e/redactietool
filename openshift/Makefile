.ONESHELL:
SHELL = /bin/bash

.PHONY: all test

test:
	apt-get update && apt-get install -y build-essential pkg-config libxml2-dev libxmlsec1-dev
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt --extra-index-url http://do-prd-mvn-01.do.viaa.be:8081/repository/pypi-all/simple --trusted-host do-prd-mvn-01.do.viaa.be
	pip install -r requirements-test.txt
	python -m  pytest -vvv --cov=./app --junit-xml=./tests/test_results.xml
