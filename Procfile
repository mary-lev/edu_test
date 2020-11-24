web: gunicorn edu_test.wsgi
worker: celery -A edu_test.celery worker -B --loglevel=info