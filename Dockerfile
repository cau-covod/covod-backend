FROM kennethreitz/pipenv

RUN pipenv install gunicorn psycopg2

WORKDIR /app
COPY . .

EXPOSE 5000
RUN chmod +x docker-start
CMD ["./docker-start"]
