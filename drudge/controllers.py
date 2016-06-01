import logging

from aiohttp import web
import arrow

from drudge.util import json_response

logger = logging.getLogger('drudge.io')


async def latest_articles(request):
    with await request.app['pool'].cursor() as cur:
        query = '''
        SELECT
            id, title, href, location, image_url, created_at, updated_at
        FROM
            public.articles'''
        query_args = []

        # Easy way to check for both new and updated articles,
        # it's up to the client to figure out which it is
        # from their perspective.
        if request.GET.get('since'):
            try:
                since = arrow.get(request.GET.get('since'))
                query += ' WHERE updated_at > %s'
                query_args.append(since.datetime)
            except:
                raise web.HTTPBadRequest(text='Invalid date format')

        query += ' ORDER BY location ASC, updated_at DESC'

        await cur.execute(query, query_args)
        articles = []
        async for row in cur:
            articles.append(dict(row))
        return json_response(articles)


def setup(app):
    app.router.add_route('GET', '/api/v1/articles/latest', latest_articles)
