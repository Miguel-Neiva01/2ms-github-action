#!/bin/sh
set -e  # Para sair imediatamente se algum comando falhar

COMMIT_HASH=$1

# Clonar diretamente o repositório 2ms
echo "Clonando o repositório 2ms..."
git clone https://github.com/checkmarx/2ms.git
cd 2ms

echo "Fazendo checkout para o commit: $COMMIT_HASH"
git checkout $COMMIT_HASH

echo "Instalando dependências do Go..."
go mod tidy

echo "Construindo o 2ms..."
mkdir -p dist
go build -o dist/2ms main.go

echo "Executando o 2ms..."
./dist/2ms

echo "Adicionando /app ao PYTHONPATH..."
export PYTHONPATH=$PYTHONPATH:/app

python3 /main.py