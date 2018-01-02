source good-thinking-env-variables.sh

python3.6 manage.py migrate
python3.6 manage.py collectstatic -c --no-input --settings $DJANGO_SETTINGS_MODULE
python3.6 manage.py runserver --settings $DJANGO_SETTINGS_MODULE 192.168.33.20:8001
