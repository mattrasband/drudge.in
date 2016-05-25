web: gunicorn drudge.application:app --bind 0.0.0.0:${PORT:-8080} --worker-class aiohttp.worker.GunicornWebWorker
worker: celery -A drudge.tasks:app worker -B -l INFO
