
FROM checkmarx/2ms:latest as twoms-env
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 py3-pip git npm

WORKDIR /app

COPY ./ /app/
COPY --from=twoms-env /app/2ms /app/2ms

RUN chmod -R +x /app

CMD ["python3", "/app/entrypoint.py"]






