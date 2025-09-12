SHELL := bash
.ONESHELL:


PHONY: install
install: ## Install dependencies
	uv sync


.PHONY: test
test:
	uv run pytest -v --cov-report term-missing --disable-warnings --cov=app tests/
