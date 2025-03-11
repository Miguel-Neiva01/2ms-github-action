
FROM checkmarx/2ms:latest as twoms-env

FROM alpine:latest



RUN apk add --no-cache python3 py3-pip git npm


WORKDIR /app


COPY package.json package-lock.json ./
RUN npm install


COPY ./create_summary /app/create_summary
COPY ./repos.json /app/repos.json
COPY ./entrypoint.py /app/entrypoint.py
COPY ./src /app/src  

RUN chmod +x /app/create_summary/main.js /app/entrypoint.py



CMD ["python3", "/app/entrypoint.py"]
