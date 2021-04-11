.PHONY: test
test: lint

.PHONY: lint
lint:
	flake8 .

.PHONY: db
db:
	FLASK_APP=asrd/app.py flask db init
	FLASK_APP=asrd/app.py flask db migrate
	FLASK_APP=asrd/app.py flask db upgrade

.PHONY: start
start:
	FLASK_APP=asrd/app.py flask run
