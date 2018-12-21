PYTHON=python3.7
app=muckr-service

all:

virtualenv:
	virtualenv --python=$(PYTHON) venv

requirements/%.txt: requirements/%.in
	pip install pip-tools
	python -m piptools compile \
	    --verbose \
	    --upgrade \
	    --generate-hashes \
	    --output-file=$@ $<

requirements: requirements/base.txt requirements/dev.txt

install:
	pip install \
	    --requirement requirements/base.txt \
	    --requirement requirements/dev.txt

test:
	python -m flake8 muckr tests setup.py wsgi.py migrations
	python -m pytest tests --verbose --cov=muckr

flask-run:
	env FLASK_ENV=development flask run

flask-shell:
	flask shell

heroku-local:
	heroku local

heroku-secretkey:
	heroku config:set --app=$(app) SECRET_KEY=$$(python -c 'import secrets; print(secrets.token_urlsafe())')

heroku-logs:
	heroku logs --app=$(app)

heroku-db-upgrade:
	heroku run --app=$(app) muckr-service flask db upgrade

travis-install: install

travis-script: test

env-secretkey:
	echo SECRET_KEY=$$(python -c 'import secrets; print(secrets.token_urlsafe())') >> .env

distclean:
	git clean -fxd
