#!/bin/sh
# Executa o coletor de clima uma vez. Pensado para ser chamado pelo cron.

set -u

# Vai para a raiz do projeto, qualquer que seja a pasta de onde o script foi chamado.
cd "$(dirname "$0")/.." || exit 1

agora() {
    date -u '+%Y-%m-%d %H:%M:%S UTC'
}

echo "[$(agora)] Iniciando coleta"

if docker compose run --rm -T coletor; then
    echo "[$(agora)] Coleta concluida com sucesso"
else
    codigo=$?
    echo "[$(agora)] Coleta FALHOU (codigo $codigo)"
    exit "$codigo"
fi