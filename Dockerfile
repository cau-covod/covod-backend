FROM kennethreitz/pipenv

RUN pipenv install gunicorn psycopg2

WORKDIR /app
COPY . .

EXPOSE 5000
RUN pipenv run python3 -m admin.insert-dummy-data
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "covod.app:app"]
