FROM kennethreitz/pipenv

RUN pipenv install gunicorn

WORKDIR /app
COPY . .

EXPOSE 5000
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "covod.app:app"]
