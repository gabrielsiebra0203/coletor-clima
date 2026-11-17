# Coletor de Clima

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![API](https://img.shields.io/badge/API-Open--Meteo-4CAF50)](https://open-meteo.com/)

AutomaÃ§Ã£o desenvolvida em Python para coletar previsÃµes meteorolÃ³gicas, armazenar os dados em SQLite e acompanhar a atualizaÃ§Ã£o das coletas.

O projeto utiliza Docker para empacotamento e execuÃ§Ã£o, permitindo agendamento periÃ³dico em servidores Linux.

**RepositÃ³rio:**
https://github.com/gabrielsiebra0203/coletor-clima

---

## Sobre o projeto

O Coletor de Clima consulta a API pÃºblica Open-Meteo e armazena previsÃµes meteorolÃ³gicas de trÃªs cidades brasileiras:

- Fortaleza (CE)
- SÃ£o Paulo (SP)
- Recife (PE)

Os dados sÃ£o persistidos em um banco SQLite, evitando duplicidade de registros e atualizando as previsÃµes existentes a cada nova coleta.

O projeto tambÃ©m possui ferramentas para consultar os dados armazenados e verificar se as coletas estÃ£o acontecendo dentro do intervalo esperado.

## Funcionalidades

- Consulta automÃ¡tica Ã  API Open-Meteo.
- Coleta de temperatura mÃ¡xima e mÃ­nima.
- Coleta de precipitaÃ§Ã£o prevista.
- Armazenamento em banco de dados SQLite.
- AtualizaÃ§Ã£o de registros existentes sem duplicaÃ§Ã£o.
- Consulta e resumo dos dados coletados.
- VerificaÃ§Ã£o da Ãºltima coleta por cidade.
- IdentificaÃ§Ã£o de coletas atrasadas.
- ExecuÃ§Ã£o automatizada com Cron.
- PersistÃªncia de dados por volume Docker.
- ExecuÃ§Ã£o do container com usuÃ¡rio nÃ£o-root.

## Tecnologias utilizadas

| Tecnologia | AplicaÃ§Ã£o |
|---|---|
| Python 3.12 | LÃ³gica de coleta e processamento |
| Requests | RequisiÃ§Ãµes HTTP Ã  API |
| SQLite | PersistÃªncia dos dados |
| Docker | Empacotamento e isolamento |
| Docker Compose | ConfiguraÃ§Ã£o e execuÃ§Ã£o |
| Linux / Cron | Agendamento das coletas |
| Open-Meteo | Fonte dos dados meteorolÃ³gicos |

## Estrutura do projeto

```text
coletor-clima/
â”œâ”€â”€ agendamento/
â”‚   â”œâ”€â”€ crontab.exemplo
â”‚   â””â”€â”€ logrotate.exemplo
â”œâ”€â”€ app/
â”‚   â”œâ”€â”€ coletor.py
â”‚   â”œâ”€â”€ consultar.py
â”‚   â””â”€â”€ verificar.py
â”œâ”€â”€ scripts/
â”‚   â”œâ”€â”€ rodar-coletor.sh
â”‚   â””â”€â”€ verificar-coleta.sh
â”œâ”€â”€ .dockerignore
â”œâ”€â”€ .env.example
â”œâ”€â”€ .gitignore
â”œâ”€â”€ Dockerfile
â”œâ”€â”€ compose.yaml
â”œâ”€â”€ requirements.txt
â””â”€â”€ README.md
```

## Requisitos

- Python 3.12 ou superior, caso execute fora do Docker.
- Docker instalado.
- Docker Compose.
- ConexÃ£o com a internet para acessar a API Open-Meteo.

## ConfiguraÃ§Ã£o

Clone o repositÃ³rio:

```bash
git clone https://github.com/gabrielsiebra0203/coletor-clima.git
cd coletor-clima
```

Crie o arquivo de configuraÃ§Ã£o:

```bash
cp .env.example .env
```

No PowerShell, utilize:

```powershell
Copy-Item .env.example .env
```

### VariÃ¡veis de ambiente

| VariÃ¡vel | PadrÃ£o | DescriÃ§Ã£o |
|---|---|---|
| `DIAS_PREVISAO` | `7` | Quantidade de dias de previsÃ£o, entre 1 e 16 |

Exemplo para coletar trÃªs dias de previsÃ£o:

```env
DIAS_PREVISAO=3
```

## Executando com Docker Compose

Construa a imagem:

```bash
docker compose build
```

Execute o coletor:

```bash
docker compose run --rm coletor
```

O coletor funciona como um job: executa a coleta e encerra o processo ao terminar.

## Consultando os dados

Para consultar os registros armazenados:

```bash
docker compose run --rm coletor python consultar.py
```

O relatÃ³rio apresenta:

- Quantidade de registros.
- VerificaÃ§Ã£o de registros duplicados.
- Ãšltima coleta registrada por cidade.
- Dias com maior volume de precipitaÃ§Ã£o prevista.

## VerificaÃ§Ã£o de saÃºde

Para verificar se as coletas estÃ£o atualizadas:

```bash
docker compose run --rm coletor python verificar.py
```

O verificador analisa a Ãºltima coleta de cada cidade e utiliza a variÃ¡vel `MAX_HORAS_SEM_COLETA`, cujo padrÃ£o Ã© de 13 horas.

CÃ³digos de saÃ­da:

| CÃ³digo | Significado |
|---|---|
| `0` | Coletas atualizadas |
| `1` | Coleta atrasada |
| `2` | Banco, dados ou configuraÃ§Ã£o invÃ¡lidos |

## PersistÃªncia dos dados

O banco SQLite Ã© armazenado no diretÃ³rio `/dados` dentro do container.

O Docker Compose utiliza um volume nomeado:

```yaml
volumes:
  dados-clima:
```

Assim, os dados permanecem armazenados mesmo apÃ³s o encerramento ou a remoÃ§Ã£o dos containers temporÃ¡rios.

## Agendamento automÃ¡tico

O projeto inclui exemplos de agendamento utilizando Cron:

```text
agendamento/crontab.exemplo
```

TambÃ©m disponibiliza scripts para execuÃ§Ã£o e verificaÃ§Ã£o:

```text
scripts/rodar-coletor.sh
scripts/verificar-coleta.sh
```

Os exemplos podem ser utilizados em servidores Linux para automatizar as coletas em horÃ¡rios definidos.

O projeto tambÃ©m inclui um exemplo de configuraÃ§Ã£o de rotaÃ§Ã£o de logs:

```text
agendamento/logrotate.exemplo
```

## SeguranÃ§a e boas prÃ¡ticas

- Container executado com usuÃ¡rio nÃ£o-root.
- Dados persistidos em volume Docker.
- Arquivos de configuraÃ§Ã£o locais protegidos pelo `.gitignore` e `.dockerignore`.
- Logs do Docker limitados a 10 MB por arquivo, com atÃ© 3 arquivos.
- RequisiÃ§Ãµes HTTP realizadas com a biblioteca Requests.

## API utilizada

Os dados meteorolÃ³gicos sÃ£o obtidos por meio da API pÃºblica Open-Meteo:

https://open-meteo.com/

## Autor

Desenvolvido por Gabriel Braga.

GitHub:
https://github.com/gabrielsiebra0203
