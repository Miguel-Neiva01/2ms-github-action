
FROM checkmarx/2ms:latest as twoms-env

FROM cgr.dev/chainguard/wolfi-base:latest


RUN apk add --no-cache python3 py3-pip git npm


WORKDIR /app


COPY package.json package-lock.json ./
RUN npm install


COPY --from=twoms-env /app/2ms /app/2ms
COPY ./create_summary /app/create_summary
COPY ./repos.json /app/repos.json
COPY ./entrypoint.py /app/entrypoint.py
COPY ./src /app/src  


RUN chmod +x /app/2ms
RUN chmod +x /app/entrypoint.py


CMD ["python3", "/app/entrypoint.py"]

