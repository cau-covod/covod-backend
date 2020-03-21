FROM kennethreitz/pipenv

RUN pipenv install

CMD ["pipenv", "run", "flask", "run"]
