#!/bin/sh
pipenv run flask insert-dummy-data
pipenv run gunicorn --bind 0.0.0.0:5000 covod.app:app
