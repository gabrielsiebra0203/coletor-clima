#!/bin/sh
# Confere se a coleta esta em dia. Pensado para ser chamado pelo cron.
# Se a variavel HEALTHCHECK_URL estiver definida, avisa o servico de monitoramento
# quando esta tudo certo (ele alerta voce quando os avisos deixam de chegar).

set -u

cd "$(dirname "$0")/.." || exit 1

agora() {
    date -u '+%Y-%m-%d %H:%M:%S UTC'
}

if docker compose run --rm -T coletor python verificar.py; then
    echo "[$(agora)] Verificacao OK"
    if [ -n "${HEALTHCHECK_URL:-}" ]; then
        curl -fsS -m 10 --retry 3 -o /dev/null "$HEALTHCHECK_URL" \
            || echo "[$(agora)] Aviso: nao foi possivel avisar o servico de monitoramento"
    fi
else
    codigo=$?
    echo "[$(agora)] Verificacao FALHOU (codigo $codigo)"
    exit "$codigo"
fi
