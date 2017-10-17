web: python manage.py migrate && python manage.py collectstatic -c --no-input --settings cms.settings.production && gunicorn  cms.wsgi --bind 0.0.0.0:$PORT --preload
