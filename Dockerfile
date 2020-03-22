FROM 183321040270.dkr.ecr.eu-central-1.amazonaws.com/covod-web-app:latest AS web-app

FROM kennethreitz/pipenv

RUN apt update && apt install -y \
    libopencv-dev \
    python3-opencv \
 && rm -rf /var/lib/apt/lists/*

RUN pipenv install gunicorn psycopg2

WORKDIR /app
COPY --from=web-app /usr/share/nginx/html web-app
COPY . .

EXPOSE 5000
RUN chmod +x docker-start
CMD ["./docker-start"]
