"""
Django settings for tests project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = ["tests"]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
import pymysql

pymysql.version_info = (1, 4, 2, "final", 0)
pymysql.install_as_MySQLdb()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "PASSWORD": os.environ["MYSQL_PWD"],
        "OPTIONS": {
            'read_default_file': BASE_DIR / 'my.cnf',
        },
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
