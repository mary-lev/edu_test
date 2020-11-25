web: gunicorn edu_test.wsgi
worker: celery -A edu_test worker -l info -O fair --without-gossip --without-mingle --without-heartbeat --concurrency=2