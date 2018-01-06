"""
Django settings for houseoffun project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9944wfl7gnp_k(lyps5a$lx+!!=(l-993@9&n33dc6pqaa0yvy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '192.168.99.100'
]


# Application definition

INSTALLED_APPS = [
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.core.mail',
    'mptt',
    'pipeline',
    'houseoffun.houseoffun',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'houseoffun.houseoffun.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'houseoffun.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'houseoffun/houseoffun/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'houseoffun.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
if os.getenv('TRAVIS', None):
    #Travis DB configuration goes here
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'travis_ci',
            'USER': 'travis',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': 3306,
            'OPTIONS': {
                'init_command': 'SET default_storage_engine=InnoDB',
            }
        }
    }
else:
    #Non-Travis DB configuration goes here
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'docker',
            'USER': 'docker',
            'PASSWORD': 'docker',
            'HOST': 'db',
            'PORT': 3306,
            'OPTIONS': {
                'init_command': 'SET default_storage_engine=InnoDB',
            }
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# Registration Settings
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/games'
SIMPLE_BACKEND_REDIRECT_URL = '/games'
LOGIN_EXEMPT_URLS = (
    r'^accounts/register',
    r'^accounts/login',
    r'^accounts/password/reset',
)

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages' # change this to a proper location

# CSS & JS Settings
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = '/tmp/media'
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE = {
    #'PIPELINE_ENABLED': True,
    'STYLESHEETS': {
        'main': {
            'source_filenames': (
              'css/bootstrap.css',
            ),
            'output_filename': 'css/min.css'
        },
    },
    'JAVASCRIPT': {
        'main': {
            'source_filenames': (
              'js/jquery.js',
              'js/popper.js',
              'js/bootstrap.js'
            ),
            'output_filename': 'js/min.js',
        }
    }
}

PIPELINE['YUGLIFY_BINARY'] = '/code/node_modules/yuglify/bin/yuglify'
