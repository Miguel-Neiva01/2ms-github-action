FROM golang:latest

# Instalar pacotes adicionais: git, curl, Python e Node.js
RUN apt-get update && apt-get install -y \
    git \
    curl \
    python3 python3-pip \
    nodejs npm

# Define a diretoria de trabalho dentro do container
WORKDIR /app

RUN apk add --no-cache python3 py3-pip git npm

WORKDIR /app

COPY ./ /app/

RUN chmod -R +x /app
RUN chmod +x /entrypoint.sh /main.py

# Define o script de entrada
ENTRYPOINT ["/entrypoint.sh"]
