a.PHONY: test
test: lint

.PHONY: lint
lint:
	flake8 .

.PHONY: db
db:
	FLASK_APP=asrd:app flask db init
	FLASK_APP=asrd:app flask db migrate
	FLASK_APP=asrd:app flask db upgrade

.PHONY: start
start:
	FLASK_APP=asrd:app flask run
