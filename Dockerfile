FROM kennethreitz/pipenv

RUN pipenv install && pipenv install waitress

WORKDIR /app
COPY . .

CMD ["pipenv", "run", "waitress-serve", "--call", "covod.app:create_app"]
