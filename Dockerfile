FROM python:latest
LABEL maintainer="estanevi@emich.edu"
WORKDIR /app/DataTitans
RUN pip install pipenv
RUN apt-get -y update && apt-get install -y wait-for-it
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --deploy --ignore-pipfile
COPY . .
WORKDIR datatitan_site
VOLUME /app/DataTitans/datatitan_site/data/input
EXPOSE 8000
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]