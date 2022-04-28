PYTEST?=	pytest
FLAKE8?=	flake8
MYPY?=		mypy
ISORT?=		isort
PYTHON?=	python3
TWINE?=		twine

lint: test flake8 mypy isort-check

test::
	/usr/bin/env PYTHONPATH=.:$$PYTHONPATH  ${PYTEST} ${PYTEST_ARGS} -v -rs

flake8::
	${FLAKE8} ${FLAKE8_ARGS} --application-import-names=github_env tests

mypy::
	${MYPY} ${MYPY_ARGS} github_env.py tests/*.py

isort-check::
	${ISORT} ${ISORT_ARGS} --check *.py tests/*.py

isort::
	${ISORT} ${ISORT_ARGS} *.py tests/*.py

sdist::
	${PYTHON} setup.py sdist

release::
	rm -rf dist
	${PYTHON} setup.py sdist
	${TWINE} upload dist/*.tar.gz
