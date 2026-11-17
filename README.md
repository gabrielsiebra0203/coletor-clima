# Coletor de Clima

Automação em Python que coleta a previsão do tempo e grava em um banco SQLite,
empacotada em Docker para rodar em qualquer servidor.

> Projeto em construção, feito durante os estudos de Docker e deploy.

## Executar o exemplo inicial

```bash
docker build -t coletor-clima:ola .
docker run --rm coletor-clima:ola
```

Com variável de ambiente:

```bash
docker run --rm -e NOME=Maria coletor-clima:ola
```