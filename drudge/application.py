import asyncio
import logging
import os

from aiohttp import web
from aiopg import create_pool
from psycopg2.extras import DictCursor

from drudge import controllers
from drudge import settings

logging.basicConfig(level=logging.ERROR,
                    format=('%(asctime)s [%(module)s#%(lineno)s]'
                            ' [%(processName)s:%(process)d] %(levelname)s'
                            ' %(message)s'))
logger = logging.getLogger('drudge.io')
logger.setLevel(logging.DEBUG)


loop = asyncio.get_event_loop()
app = web.Application(middlewares=(), loop=loop, debug=settings.DEBUG)

app.update(
    pool=loop.run_until_complete(create_pool(settings.DATABASE_URL,
                                             minsize=settings.DATABASE_POOL_MIN,
                                             maxsize=settings.DATABASE_POOL_MAX,
                                             cursor_factory=DictCursor)),
)

controllers.setup(app)

