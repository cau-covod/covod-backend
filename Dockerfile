FROM 183321040270.dkr.ecr.eu-central-1.amazonaws.com/covod-web-app:latest AS web-app

FROM python:3.8

RUN pip install pipenv

RUN mkdir /app
WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system --deploy

RUN pipenv install gunicorn psycopg2

COPY --from=web-app /usr/share/nginx/html web-app
COPY . .

EXPOSE 5000
RUN chmod +x docker-start
CMD ["./docker-start"]
