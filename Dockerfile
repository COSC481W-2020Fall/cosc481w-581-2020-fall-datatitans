FROM python:latest
LABEL maintainer="estanevi@emich.edu"
WORKDIR /app/DataTitans
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
WORKDIR datatitan_site
RUN python manage.py migrate
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]