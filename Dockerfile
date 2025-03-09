FROM checkmarx/2ms:latest as twoms-env

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 py3-pip git

COPY ./repos.json /app/repos.json

COPY --from=twoms-env /app /app

COPY ./entrypoint.py /entrypoint.py

RUN chmod +x /entrypoint.py

COPY ./ /app

CMD ["python3", "/entrypoint.py"]
