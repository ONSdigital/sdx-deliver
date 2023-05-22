build:
	pip install -r requirements.txt
start: build
	python run.py
test: build
	pip install -r test-requirements.txt
	flake8
	pytest -v --cov-report term-missing --disable-warnings --cov=app tests/
