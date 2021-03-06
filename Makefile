.PHONY: test
test: lint

.PHONY: lint
lint:
	flake8 .
