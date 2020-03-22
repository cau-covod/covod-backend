FROM 183321040270.dkr.ecr.eu-central-1.amazonaws.com/covod-web-app:latest AS web-app

FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
    libglib2.0 \
  && rm -rf /var/cache/apt/archives

RUN pip install pipenv

RUN mkdir /app
WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN set -ex && pipenv install --deploy --system

COPY . .

COPY --from=web-app /usr/share/nginx/html web-app

EXPOSE 5000
ENTRYPOINT ["sh", "./admin/docker-start.sh"]
