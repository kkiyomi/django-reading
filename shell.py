import os
import sys
import django

# The path to your project
path = 'file:C:/Users/user/Desktop/python/django_project'
if path not in sys.path:
    sys.path.append(path)

# Change to your project settings root
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

# django.setup()

# exec(open('shell.py').read())

from django.core.management import execute_from_command_line

execute_from_command_line(['.', 'shell'])
