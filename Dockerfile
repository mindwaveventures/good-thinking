# Copyright 2019 Mindwave Ventures
# Dockerfile supporting multi-stage builds

# Base container
FROM python:3.6 AS gt-base

LABEL org.label-schema.vendor="Mindwave Ventures" \
      org.label-schema.url="https://www.mindwaveventures.com/" \
      org.label-schema.name="Good Thinking - Base image" \
      org.label-schema.version="v0.0.0" \
      org.label-schema.docker.schema-version="1.0" \
      com.mindwave.maintainer="David Bower" \
      com.mindwave.contact="david@mindwaveventures.com"

# Install required packages and remove the apt packages cache when done.
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y curl \
  software-properties-common && \
  `# Install nodejs from nodesource.com` \
  curl -sL https://deb.nodesource.com/setup_11.x | bash - && \
  apt-get install -y \
  nginx \
  supervisor \
  nodejs \
  npm && \
  npm -g install yuglify && \
  # ln -s /usr/bin/nodejs /usr/bin/node && \
  pip3 install uwsgi && \
  echo "daemon off;" >> /etc/nginx/nginx.conf \
  `# Remove unwanted packages` \
  rm -rf /usr/lib/gcc && \
  rm -rf /usr/share/man && \
  apt-get autoremove && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*


# Core components and config
FROM gt-base AS gt-core

LABEL org.label-schema.vendor="Mindwave Ventures" \
      org.label-schema.url="https://www.mindwaveventures.com/" \
      org.label-schema.name="Good Thinking - App Base Image" \
      org.label-schema.version="v0.0.0" \
      org.label-schema.docker.schema-version="1.0" \
      com.mindwave.maintainer="David Bower" \
      com.mindwave.contact="david@mindwaveventures.com"

# COPY all the config files
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code
# to prevent Docker re-installing dependencies when code changes in the app.
COPY requirements.txt /home/docker/code/

RUN pip3 install -r /home/docker/code/requirements.txt

# App container
FROM gt-core AS gt-app

LABEL org.label-schema.vendor="Mindwave Ventures" \
      org.label-schema.url="https://www.mindwaveventures.com/" \
      org.label-schema.name="Good Thinking" \
      org.label-schema.version="v0.0.0" \
      org.label-schema.docker.schema-version="1.0" \
      com.mindwave.maintainer="David Bower" \
      com.mindwave.contact="david@mindwaveventures.com"

# COPY our app code
COPY . /home/docker/code/

WORKDIR /home/docker/code/
RUN chmod a+x wagtail.sh && \
  npm install && \
  npm run install:elm

EXPOSE 80
CMD ["supervisord", "-n"]
