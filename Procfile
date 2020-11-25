web: gunicorn edu_test.wsgi
worker: celery -A edu_test worker --beat --scheduler django --loglevel=info