# -*- coding: utf-8 -*-
# Django settings for clickpb project.

import sys
import os, os.path

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(PROJECT_PATH, 'apps'))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (    
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_PATH, 'banco.sqlite'), # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
    }
}
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Recife'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = join(PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = join(PROJECT_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files

STATICFILES_DIRS = (
    ('site', join(PROJECT_DIR, 'sitestatic')),                
)

SERVE_STATIC_FILES = True

ADMIN_MEDIA_ROOT = join(STATIC_ROOT, 'grappelli')

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5jxrrg**ikh(-g*v7k8nu22qy8&v8iuz6^8_c5y&$b5qmczwd@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'common.middleware.RequestCheckMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    
)

ROOT_URLCONF = 'projeto.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # default context
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',        
    'django.core.context_processors.request',
    'utils.context_processors.get_current_path',
    'utils.context_processors.is_mobile',
)

INSTALLED_APPS = (
    # django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.comments',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    # grappelli before admin
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # external apps
    'registration',
    'south',
    'filebrowser',        
    'pagination',
    'easy_thumbnails',    
    'captcha',
    # local apps        
    'articles',    
    'blogs',
    'comments',
    'common',
    'contact',    
    'homepage',
    'polls',
    'registration',
    'videos',
    
)

INTERNAL_IPS = ('127.0.0.1',)
#MeuClick settings
#versao atual sem o meuclick
#LOGIN_URL = "/cadastro/acessar/"

#Tagging settings
FORCE_LOWERCASE_TAGS  = True

# Flag to serve static files from django.
SERVE_STATIC_FILES = True

# Grappelli settings
GRAPPELLI_ADMIN_TITLE = 'Administração'

# FILEBROWSER SETTINGS
FILEBROWSER_URL_FILEBROWSER_MEDIA = '/media/filebrowser/'
FILEBROWSER_DIRECTORY = 'filebrowser/'

# Caching settings
CACHE_BACKEND = 'locmem://'

#varnishapp settings
#ENABLE_DJANGO_VARNISH = False
#VARNISH_MANAGEMENT_ADDRS = ('localhost:6082')

# Captcha settings
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_BACKGROUND_COLOR = "#FFFACD"
CAPTCHA_FOREGROUND_COLOR = 'black'
CAPTCHA_LETTER_ROTATION = None
CAPTCHA_NOISE_FUNCTIONS = None

# Load settings local if exists
try:
    execfile(os.path.join(PROJECT_PATH, 'settings_local.py'), globals(), locals())
except IOError:
    pass

