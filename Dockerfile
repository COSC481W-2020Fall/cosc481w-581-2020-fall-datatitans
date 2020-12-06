FROM python:3.8
LABEL maintainer="estanevi@emich.edu"
WORKDIR /app/DataTitans
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --deploy --ignore-pipfile
VOLUME /app/DataTitans/datatitan_site
COPY . .
WORKDIR datatitan_site
ENV APP_ENV=docker INPUT_FILE=/app/DataTitans/datatitan_site/data/input/owid-covid-data.csv
EXPOSE 8000
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
