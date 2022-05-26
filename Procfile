web: gunicorn eng_backend.wsgi
release: pyhton manage.py makemigrations --noinput
release: pyhton manage.py migrate --noinput
release: pyhton manage.py collectstatic --noinput
