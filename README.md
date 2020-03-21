# CoVoD Backend

## Dev setup
1. Install `pipenv`
2. Run `pipenv install`
3. Copy .env.default to .env.
4. Run `pipenv run flask run` to start the development webserver.

## Filling db with test data
1. Run `pipenv run flask insert-dummy-data` to drop all existing tables and to initialize dummy data

## Getting tokens
Check out the "Generate token" request in the included `covod.postman_collection.json`
for an example resource owner credentials grant.