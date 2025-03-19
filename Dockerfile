FROM golang:latest

# Instalar pacotes adicionais: git, curl, Python e Node.js
RUN apt-get update && apt-get install -y \
    git \
    curl \
    python3 python3-pip \
    nodejs npm

# Define a diretoria de trabalho dentro do container
WORKDIR /app

# Copiar os scripts e código-fonte para dentro do container
COPY entrypoint.sh /entrypoint.sh
COPY main.py /main.py
COPY src/ /app/src/

# Garantir que os scripts têm permissões de execução
RUN chmod +x /entrypoint.sh /main.py

# Define o script de entrada
ENTRYPOINT ["/entrypoint.sh"]
