#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from temp.PrototypeGraphSetup import gen_images 

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
    #print(sys.argv[1])
    if(len(sys.argv) > 1 and sys.argv[1] == "run" ):
        gen_images()
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
