FROM checkmarx/2ms:latest as twoms-env

FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip git && rm -rf /var/lib/apt/lists/*

COPY ./repos.json /app/repos.json

COPY --from=twoms-env /app /app

COPY ./entrypoint.py /entrypoint.py

RUN chmod +x /entrypoint.py

COPY ./ /app

CMD ["python3", "/entrypoint.py"]
