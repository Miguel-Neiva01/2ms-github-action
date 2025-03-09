FROM python:3.9-slim as base-env

FROM checkmarx/2ms:latest as twoms-env

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk update && apk add --no-cache python3 py3-pip git

RUN python3 --version

COPY ./repos.json /app/repos.json

COPY --from=twoms-env /app /app

COPY ./entrypoint.py /entrypoint.py

RUN chmod +x /entrypoint.py

COPY ./ /app

RUN echo "Starting the build process..." && \
    python3 --version && \
    ls -la / && \
    echo "Checking if entrypoint.py is in the right place..." && \
    ls -la /entrypoint.py

RUN ls -l /entrypoint.py


ENTRYPOINT ["sh", "-c", "echo 'Running entrypoint.py...' && /usr/bin/python3 /entrypoint.py"]
