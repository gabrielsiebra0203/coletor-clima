# Coletor de Clima

Automação em Python que coleta a previsão do tempo (API Open-Meteo) e grava em um
banco SQLite, sem duplicar registros. Empacotada em Docker.

## Como rodar

```bash
docker build -t coletor-clima:1.0 .
docker run --rm -v dados-clima:/dados coletor-clima:1.0
```

## Rodando com Docker Compose

```bash
cp .env.example .env        # no PowerShell: Copy-Item .env.example .env
docker compose build
docker compose run --rm coletor
```

Ver os logs da última execução e os dados coletados:

```bash
docker compose logs --tail 20
docker compose run --rm coletor python consultar.py
```

> O coletor é um *job*: roda e termina. Para execução periódica, use agendamento (cron).

## Configuração

| Variável | Padrão | Descrição |
|---|---|---|
| `DATA_DIR` | `/dados` (no container) | Pasta onde o banco é gravado |
| `DIAS_PREVISAO` | `7` | Dias de previsão (1 a 16) |

Exemplo:

```bash
docker run --rm -v dados-clima:/dados -e DIAS_PREVISAO=3 coletor-clima:1.0
```

## Verificar os dados coletados

```bash
docker run --rm -v dados-clima:/dados coletor-clima:1.0 python consultar.py
```

## Código de saída

O programa termina com `0` em caso de sucesso e `1` se alguma cidade falhar.