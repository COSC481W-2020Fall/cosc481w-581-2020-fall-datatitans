FROM python:latest
LABEL maintainer="estanevi@emich.edu"
WORKDIR /app/DataTitans
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --deploy --ignore-pipfile
COPY . .
WORKDIR datatitan_site
RUN pipenv run python manage.py migrate
VOLUME /app/DataTitans/datatitan_site/data/input
EXPOSE 8000
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]