FROM python:3.8
LABEL maintainer="estanevi@emich.edu"
WORKDIR /app/DataTitans
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --deploy --ignore-pipfile
COPY . .
WORKDIR datatitan_site
ENV APP_ENV=docker
EXPOSE 8000
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]