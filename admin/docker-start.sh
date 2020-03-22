#!/bin/sh
pipenv run gunicorn --bind 0.0.0.0:5000 covod.app:app
