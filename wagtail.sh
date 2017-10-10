#!/bin/bash

cd /home/docker/code/
# python manage.py migrate
python manage.py collectstatic -c --no-input --settings cms.settings.production
python manage.py runserver --settings cms.settings.production 127.0.0.1:8001
