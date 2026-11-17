"""Consultas de verificação sobre os dados coletados."""

import os
import sqlite3
import sys
from pathlib import Path

ARQUIVO_BANCO = Path(os.environ.get("DATA_DIR", "dados")) / "clima.db"


def formatar(valor, sufixo=""):
    """Mostra um traço quando a API não trouxe valor para o dia."""
    if valor is None:
        return "-"
    return f"{valor:.1f}{sufixo}"


def main():
    if not ARQUIVO_BANCO.exists():
        print("Banco não encontrado. Rode antes o coletor.")
        sys.exit(1)

    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.row_factory = sqlite3.Row
    try:
        total = conexao.execute("SELECT COUNT(*) AS total FROM previsoes").fetchone()
        print(f"Registros em previsoes: {total['total']}")

        duplicados = conexao.execute(
            """
            SELECT cidade_id, data
            FROM previsoes
            GROUP BY cidade_id, data
            HAVING COUNT(*) > 1
            """
        ).fetchall()
        print(f"Registros duplicados: {len(duplicados)}")

        print("\nÚltima coleta por cidade (UTC):")
        coletas = conexao.execute(
            """
            SELECT c.nome AS cidade, COUNT(p.id) AS dias, MAX(p.coletado_em) AS ultima
            FROM cidades AS c
            INNER JOIN previsoes AS p ON p.cidade_id = c.id
            GROUP BY c.id, c.nome
            ORDER BY c.nome
            """
        ).fetchall()
        for linha in coletas:
            print(f"  {linha['cidade']:<12} {linha['dias']:>2} dia(s)  {linha['ultima']}")

        print("\nOs 5 dias com mais chuva prevista:")
        chuvosos = conexao.execute(
            """
            SELECT c.nome AS cidade, p.data, p.chuva_mm
            FROM previsoes AS p
            INNER JOIN cidades AS c ON c.id = p.cidade_id
            WHERE p.chuva_mm IS NOT NULL
            ORDER BY p.chuva_mm DESC
            LIMIT 5
            """
        ).fetchall()
        for linha in chuvosos:
            print(f"  {linha['data']}  {linha['cidade']:<12} {formatar(linha['chuva_mm'], ' mm')}")
    finally:
        conexao.close()


if __name__ == "__main__":
    main()