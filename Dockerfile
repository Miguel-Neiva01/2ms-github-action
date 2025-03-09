FROM checkmarx/2ms:latest as twoms-env

FROM cgr.dev/chainguard/wolfi-base:latest

COPY ./repos.json /app/repos.json

COPY --from=twoms-env /app /app

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

COPY ./ /app

ENTRYPOINT ["entrypoint.sh"]
