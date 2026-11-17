"""Verifica se a coleta está em dia: cada cidade deve ter sido atualizada recentemente.

Variáveis de ambiente:
    DATA_DIR              pasta do banco (padrão: dados)
    MAX_HORAS_SEM_COLETA  limite de horas sem coleta (padrão: 13)

Códigos de saída: 0 = em dia, 1 = desatualizado, 2 = erro (banco ou dados ausentes).
"""

import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ARQUIVO_BANCO = Path(os.environ.get("DATA_DIR", "dados")) / "clima.db"


def ler_limite_horas():
    """Lê MAX_HORAS_SEM_COLETA do ambiente e valida."""
    texto = os.environ.get("MAX_HORAS_SEM_COLETA", "13")
    try:
        horas = float(texto)
    except ValueError:
        print(f"ERRO: MAX_HORAS_SEM_COLETA inválido: '{texto}'.")
        sys.exit(2)
    if horas <= 0:
        print("ERRO: MAX_HORAS_SEM_COLETA deve ser maior que zero.")
        sys.exit(2)
    return horas


def buscar_ultimas_coletas():
    """Devolve a data/hora da última coleta de cada cidade."""
    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.row_factory = sqlite3.Row
    try:
        return conexao.execute(
            """
            SELECT c.nome AS cidade, MAX(p.coletado_em) AS ultima
            FROM cidades AS c
            INNER JOIN previsoes AS p ON p.cidade_id = c.id
            GROUP BY c.id, c.nome
            ORDER BY c.nome
            """
        ).fetchall()
    finally:
        conexao.close()


def main():
    limite = ler_limite_horas()

    if not ARQUIVO_BANCO.exists():
        print(f"ERRO: banco de dados não encontrado em {ARQUIVO_BANCO}.")
        sys.exit(2)

    try:
        coletas = buscar_ultimas_coletas()
    except sqlite3.OperationalError as erro:
        print(f"ERRO: não foi possível ler o banco: {erro}")
        sys.exit(2)

    if not coletas:
        print("ERRO: nenhuma coleta registrada.")
        sys.exit(2)

    agora = datetime.now(timezone.utc)
    atrasadas = 0

    for linha in coletas:
        ultima = datetime.fromisoformat(linha["ultima"])
        horas = (agora - ultima).total_seconds() / 3600
        if horas > limite:
            situacao = "ATRASADA"
            atrasadas += 1
        else:
            situacao = "OK"
        print(f"{situacao:<9} {linha['cidade']:<12} última coleta há {horas:.1f} h ({linha['ultima']})")

    if atrasadas:
        print(f"ALERTA: {atrasadas} cidade(s) sem coleta há mais de {limite:g} h.")
        sys.exit(1)

    print("Tudo em dia.")


if __name__ == "__main__":
    main()