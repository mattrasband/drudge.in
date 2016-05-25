import os


DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_POOL_MIN = os.environ.get('MIN_POOL_SIZE', 5)
DATABASE_POOL_MAX = os.environ.get('MAX_POOL_SIZE', 15)
DEBUG = False
