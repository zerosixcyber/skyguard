.PHONY: lint test format check clean

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

check: lint
	ruff format --check src/ tests/

test:
	pytest -v --tb=short

test-cov:
	pytest -v --cov=skyguard --cov-report=term-missing

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache dist build
