import datetime
from functools import partial
import json

from aiohttp import web


def default_json(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError('Unable to serialize {!r}'.format(obj))


json_dumps = partial(json.dumps, default=default_json)
json_response = partial(web.json_response, dumps=json_dumps)
