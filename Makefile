.PHONY: test
test: lint

.PHONY: lint
lint:
	flake8 .

.PHONY: start
start:
	FLASK_APP=asrd/app.py flask run
