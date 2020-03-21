FROM kennethreitz/pipenv

RUN pipenv install gunicorn psycopg2

WORKDIR /app
COPY . .

EXPOSE 5000
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "covod.app:app"]
