#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import datetime


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datatitan_site.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if sys.argv[1] == "test":
        make_migrate = ['manage', 'makemigrations']
        migrate = ['manage', 'migrate']
        runserver = ['manage', 'runserver']
        execute_from_command_line(make_migrate)
        execute_from_command_line(migrate)
        author = "Ben Potter"
        title = "Test"
        text = "Please work"
        created_date = datetime.datetime.today()
        published_date = datetime.datetime.today()
        from data.models import Post
        Post(3,author, title, text, created_date, published_date).save()
        for m in data.models:
            print(m)
        execute_from_command_line(runserver)
    
       
       
    elif len(sys.argv) > 1 and sys.argv[1] == "run":
        make_migrate = ['manage', 'makemigrations']
        migrate = ['manage', 'migrate']
        runserver = ['manage', 'runserver']
        execute_from_command_line(make_migrate)
        execute_from_command_line(migrate)
        execute_from_command_line(runserver)
        
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
