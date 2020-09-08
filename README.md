# DataTitans

## Getting Started

In order to set up and run the project you will need to have Python 3.7 and Django installed.

### Installing Python
You can either install python directly on your machine or use an python engine such as [anaconda](https://www.anaconda.com/products/individual)
It is advised to run inside a virtual environment

### Installing Django
1. Run `python -m pip install --upgrade pip`
2. Run `pip install -r requirements.txt`. This will install the required packages.

## Ruuning the Web Server
1. Inside the datatitans directory, where `manage.py` is, run `python manage.py migrate`. This sets up the database. (Currently SQLite)
2. Run `python manage.py runserver`