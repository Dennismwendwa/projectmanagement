from .settings import *
DEBUG = True
SECRET_KEY = 'django-insecure-dgu5*^9cexga$udi7@__0lwjbhm3lrkm7@c$320l!!)drw*onu'

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
# AWS Bucket settings
#AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
#AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
#AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
#AWS_S3_SIGNATURE_NAME = os.environ.get("AWS_S3_SIGNATURE_NAME")
#AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
#AWS_S3_FILE_OVERWRITE = os.environ.get("AWS_S3_FILE_OVERWRITE")
#AWS_DEFAULT_ACL = None
#AWS_S3_VERITY = os.environ.get("AWS_S3_VERITY")
#DEFAULT_FILE_STORAGE = os.environ.get("DEFAULT_FILE_STORAGE")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        # "LOCATION": "redis://username:password@127.0.0.1:6379", pro
    },
    "special_cache": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_special_cache",
        "OPTIONS": {
            "MAX_ENTRIES": 1000,
        }
    },
}
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_KEY_PREFIX = ""
CACHE_MIDDLEWARE_SECONDS = 0