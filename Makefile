.PHONY: clean-pyc clean-build docs clean
VENV=.venv
CHEESE=https://pypi.python.org/pypi
BUMPTYPE=patch
SPHINXBUILD=`realpath $VENV`/bin/sphinx-build

help:
	@echo "bootstrap - create a virtualenv and install the necessary packages for development."
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release."
	@echo '          use `-e CHEESE=http://localpypi` to release somewhere else.'
	@echo "dist - package"
	@echo "bump - bump the version number via bumpversion."
	@echo '       use `-e BUMPTYPE=minor` to specify `major` or `minor` (default is `patch`).'

bootstrap:
	virtualenv $(VENV)
	$(VENV)/bin/pip install -r dev_requirements.txt

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 taskin tests

test:
	$(VENV)/bin/py.test

test-all:
	tox

coverage:
	$(VENV)/bin/py.test --cov=taskin --cov-report term

docs:
	rm -f docs/taskin.rst
	rm -f docs/modules.rst
	source $(VENV)/bin/activate
	sphinx-apidoc -o docs/ taskin
	$(MAKE) -f docs/Makefile -C docs clean
	$(MAKE) -f docs/Makefile -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist register -r $(CHEESE) upload -r $(CHEESE)

dist: clean
	python setup.py sdist
	ls -l dist

bump:
	$(VENV)/bin/bumpversion $(BUMPTYPE)
	git push origin master
	git push --tags


run:
	$(VENV)/bin/honcho start -f Procfile.dev
