FROM ubuntu:latest

# Instalar dependências
RUN apt-get update && \
    apt-get install -y python3 python3-pip git npm golang && \
    apt-get clean


# Adicionar um argumento para o commit hash
ARG COMMIT_HASH

# Clonar e compilar o 2MS com o commit específico
RUN git clone https://github.com/checkmarx/2ms.git && \
    cd 2ms && \
    git checkout ${COMMIT_HASH} && \
    go mod tidy && \
    go build -o /tmp/2ms main.go

# Copiar entrypoint
COPY entrypoint.py /entrypoint.py
RUN chmod +x /entrypoint.py

# Definir entrypoint
ENTRYPOINT ["python3", "/entrypoint.py"]
