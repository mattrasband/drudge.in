import logging

from aiohttp import web
import arrow

logger = logging.getLogger('drudge.io')


async def latest_articles(request):
    with await request.app['pool'].cursor() as cur:
        query = '''
        SELECT
            id, title, href, location, image_url, created_at, updated_at
        FROM
            public.articles
        ORDER BY updated_at DESC, location DESC'''
        query_args = []

        if request.GET.get('since'):
            try:
                since = arrow.get(request.GET.get('since'))
                query += ' WHERE created_at > %s'
                query_args.append(since.datetime)
            except:
                raise web.HTTPBadREquest(text='Invalid date format')

        await cur.execute(query, query_args)
        articles = []
        async for row in cur:
            articles.append(dict(row))
            articles[-1]['created_at'] = str(articles[-1]['created_at'])
            articles[-1]['updated_at'] = str(articles[-1]['updated_at'])
        return web.json_response(articles)


def setup(app):
    app.router.add_route('GET', '/api/v1/articles/latest', latest_articles)

