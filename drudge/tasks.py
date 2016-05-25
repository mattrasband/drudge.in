from datetime import timedelta
import logging
import os

from celery import Celery
from drudge_parser import scrape_site
import psycopg2
from psycopg2.extras import DictCursor


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('drudge:tasks')


app = Celery('drudge:tasks',
             broker=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'))
app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE=os.environ.get('TIMEZONE', 'America/Indianapolis'),
    CELERY_ENABLE_UTC=True,
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERYBEAT_SCHEDULE={
        'scrape-every-120-seconds': {
            'task': 'drudge.tasks.scrape',
            'schedule': timedelta(seconds=os.environ.get('SCRAPE_TIME_SECONDS', 120)),
            'args': (os.environ['DATABASE_URL'],),
        },
    },
)


@app.task
def scrape(dsn):
    with psycopg2.connect(dsn, cursor_factory=DictCursor) as conn:
        with conn.cursor() as cur:
            try:
                logger.info('Beginning scrape')
                scraper = scrape_site()
                # Keeps track of any hrefs in th current scrape
                # so we can delete any that aren't still active on
                # the drudge report
                hrefs = []
                for article, image in scraper:
                    hrefs.append(article.href)

                    cur.execute('''SELECT title, href, location, image_url
                    FROM public.articles WHERE href = %s''',
                    [article.href])

                    res = cur.fetchone()
                    if not res:
                        logger.info('New article found: %s', article)
                        cur.execute('''INSERT INTO public.articles (
                            title, href, location, image_url, created_at,
                            updated_at
                        ) VALUES (
                            %(title)s, %(href)s, %(location)s, %(image_url)s,
                            now(), now()
                        )''', {
                            'title': article.title,
                            'href': article.href,
                            'location': article.location,
                            'image_url': image.src if image else '',
                        })
                    else:
                        existing = dict(res)
                        possibly_new = {
                            'title': article.title,
                            'href': article.href,
                            'location': article.location,
                            'image_url': image.src if image else '',
                        }
                        if existing != possibly_new:
                            logger.info('Existing: %s; New: %s', existing, possibly_new)
                            cur.execute('''UPDATE public.articles SET
                            title=%(title)s, location=%(location)s,
                            image_url=%(image_url)s, updated_at=now()
                            WHERE href=%(href)s
                            ''', {
                                'title': article.title,
                                'location': article.location,
                                'image_url': image.src if image else '',
                                'href': article.href,
                            })

                if hrefs:
                    # Note: Just builds a query, doesn't inject itself
                    query = '''DELETE FROM public.articles WHERE href NOT IN'''
                    query += '(' + ','.join(['%s' for _ in hrefs]) + ')'
                    cur.execute(query, hrefs)
            except Exception as e:
                logger.error('Exception during scrape: %s', e)
                raise e
            else:
                logger.info('Scrape finished successfully.')

