
FROM checkmarx/2ms:latest as twoms-env


FROM cgr.dev/chainguard/wolfi-base:latest


RUN apk add --no-cache python3 py3-pip git npm

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install


COPY ./create_summary /app/create_summary
COPY ./repos.json /app/repos.json
COPY --from=twoms-env /app /app
COPY ./entrypoint.py /entrypoint.py
COPY ./src /app/src


RUN chmod +x /app/create_summary/main.js /entrypoint.py

CMD ["python3", "/entrypoint.py"]
