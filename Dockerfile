# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python:3.6

MAINTAINER David Bower (david@mindwaveventures.com)

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
	nginx \
	supervisor \
    nodejs \
    npm && \
    npm -g install yuglify && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/nodejs /usr/bin/node && \
    pip3 install uwsgi && \
    echo "daemon off;" >> /etc/nginx/nginx.conf

# setup all the configfiles

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.

COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/
COPY requirements.txt /home/docker/code/

RUN pip3 install -r /home/docker/code/requirements.txt

# add (the rest of) our code
COPY . /home/docker/code/

WORKDIR /home/docker/code/
RUN chmod a+x wagtail.sh && \
    npm install && \
    npm run install:elm

EXPOSE 80
CMD ["supervisord", "-n"]
