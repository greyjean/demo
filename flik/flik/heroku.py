import dj_database_url
from flik.base import *

REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0')

DEBUG = True

DATABASES['default'] =  dj_database_url.config()

