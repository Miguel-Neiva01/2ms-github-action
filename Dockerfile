FROM checkmarx/2ms:latest as twoms-env

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 py3-pip git

RUN apk add --no-cache nodejs npm

COPY ./repos.json /app/repos.json

COPY --from=twoms-env /app /app

COPY ./entrypoint.py /entrypoint.py

COPY ./src /app/src

RUN chmod +x /entrypoint.py

COPY ./ /app

CMD ["python3", "/entrypoint.py"]
