# CoVoD Backend

## Dev setup
1. Install `pipenv`
2. Run `pipenv install`
3. Copy .env.default to .env.
4. Run `pipenv run flask run` to start the development webserver.

## Filling db with test data
1. Run `pipenv run flash shell`
2. Run `exec(open("admin/insert-dummy-data.py").read())`