from .settings import *
DEBUG = False
SECRET_KEY = 'django-insecure-dgu5*^9cexga$udi7@__0lwjbhm3lrkm7@c$320l!!)drw*onu'

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
