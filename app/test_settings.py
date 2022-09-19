from .settings import *

# make tests faster
DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
