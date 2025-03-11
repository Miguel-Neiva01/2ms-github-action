FROM checkmarx/2ms:latest as twoms-env

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 py3-pip git nodejs npm

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

COPY --from=twoms-env /app /app

RUN chmod +x /app/entrypoint.py

CMD ["python3", "/app/entrypoint.py"]
