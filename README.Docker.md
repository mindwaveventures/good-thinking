# Docker README

To build the Good Thinking Docker container, simply `docker build . -t goodthinking`

The Dockerfile also supports [multi-stage builds.](https://docs.docker.com/develop/develop-images/multistage-build/)

		docker build . --target gt-base -t gt-base:latest
		docker build . --target gt-core -t gt-core:latest
		docker build . --target gt-app -t goodthinking:latest
