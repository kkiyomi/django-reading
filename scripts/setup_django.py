def setup_django():
    import sys
    import django
    import os

    path = "C:/Users/user/Desktop/python/django_project"
    if path not in sys.path:
        sys.path.append(path)  # /home/projects/my-djproj
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
    django.setup()
