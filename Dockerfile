FROM kennethreitz/pipenv

RUN pipenv install gunicorn psycopg2

WORKDIR /app
COPY . .

EXPOSE 5000
CMD ["./docker-start"]
