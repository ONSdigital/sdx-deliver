build:
	pip install -r requirements.txt

start:
	 python run.py

test:
	pip install -r test_requirements.txt ; \
	python -m unittest discover -s tests
