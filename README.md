# DataTitans

## Description of Prototype
1. User can navigate to data page and view chart
2. User can navigate to about page
3. User can view blog page to read about future of the site
4. Charts are built with downloaded CSV file integrated to SQLite database with visualization through seaborn library

## Getting Started

In order to set up and run the project you will need to have Python 3.8 and Django installed.

### Installing Python
You can either install python directly on your machine or use a python engine such as [Anaconda](https://www.anaconda.com/products/individual).
It is advised to run Python inside a virtual environment.

### Installing Django
1. Run `python -m pip install --upgrade pip`
2. Run `pip install -r requirements.txt`. This will install the required packages.

## Running the Web Server
1. Inside the datatitans directory, where `manage.py` is, run `python manage.py migrate`. This sets up the database. (Currently SQLite)
2. Run `python manage.py runserver`
