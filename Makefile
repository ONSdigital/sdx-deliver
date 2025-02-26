SHELL := bash
.ONESHELL:


.PHONY: test
test:
	. venv/bin/activate \
	&& python3 --version \
	&& python3 -m pip install --upgrade pip \
	&& pip install -r requirements.txt \
	&& pip install -r test-requirements.txt \
	&& python3 -m pytest -vv --cov-report term-missing --disable-warnings --cov=app tests
