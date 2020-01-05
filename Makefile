all: clean test

test:
	pytest tests

clean:
	rm -rf .pytest_cache
