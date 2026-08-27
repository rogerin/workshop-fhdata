from __future__ import annotations

import csv
import json
import sqlite3
from functools import lru_cache
from typing import Any

from rag.config import BUNDLE_PATH, CSV_PATH

NUMERIC_COLS = {
    "ganho",
    "valor",
    "receita_ganha",
    "valor_perdido",
    "dias_consignacao",
    "dias_pagamento",
    "ciclo_total_dias",
    "dias_cotacao_autorizacao",
    "dias_cirurgia_faturamento",
    "valor_glosado",
    "valor_recuperado",
    "glosa_nao_recuperada",
}


def _to_number(value: str) -> float:
    if value is None or value == "":
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0


def load_rows() -> list[dict[str, Any]]:
    with CSV_PATH.open("r", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for col in NUMERIC_COLS:
            row[col] = _to_number(row.get(col, ""))
    return rows


def load_bundle() -> dict[str, Any]:
    with BUNDLE_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_sqlite(rows: list[dict[str, Any]]) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE negocios (
            negocio TEXT PRIMARY KEY,
            etapa1_cotacao TEXT,
            etapa2_autorizacao TEXT,
            etapa3_cirurgia TEXT,
            etapa4_faturamento TEXT,
            status TEXT,
            ganho INTEGER,
            ano INTEGER,
            mes TEXT,
            vendedor TEXT,
            cliente TEXT,
            tipo_pagador TEXT,
            estado TEXT,
            produto TEXT,
            linha_produto TEXT,
            valor REAL,
            receita_ganha REAL,
            valor_perdido REAL,
            motivo_perda TEXT,
            etapa_perda TEXT,
            dias_consignacao REAL,
            dias_pagamento REAL,
            ciclo_total_dias REAL,
            dias_cotacao_autorizacao REAL,
            dias_cirurgia_faturamento REAL,
            valor_glosado REAL,
            valor_recuperado REAL,
            glosa_nao_recuperada REAL
        )
        """
    )
    cols = [
        "negocio",
        "etapa1_cotacao",
        "etapa2_autorizacao",
        "etapa3_cirurgia",
        "etapa4_faturamento",
        "status",
        "ganho",
        "ano",
        "mes",
        "vendedor",
        "cliente",
        "tipo_pagador",
        "estado",
        "produto",
        "linha_produto",
        "valor",
        "receita_ganha",
        "valor_perdido",
        "motivo_perda",
        "etapa_perda",
        "dias_consignacao",
        "dias_pagamento",
        "ciclo_total_dias",
        "dias_cotacao_autorizacao",
        "dias_cirurgia_faturamento",
        "valor_glosado",
        "valor_recuperado",
        "glosa_nao_recuperada",
    ]
    payload = []
    for row in rows:
        payload.append(
            tuple(
                int(row[c]) if c in {"ganho", "ano"} else row.get(c, "")
                for c in cols
            )
        )
    cur.executemany(
        f"INSERT INTO negocios ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
        payload,
    )
    conn.commit()
    return conn


def distinct_values(rows: list[dict[str, Any]], field: str) -> list[str]:
    values = sorted({str(r.get(field, "")).strip() for r in rows if r.get(field)})
    return values


@lru_cache(maxsize=1)
def get_catalog() -> dict[str, list[str]]:
    rows = load_rows()
    return {
        "anos": distinct_values(rows, "ano"),
        "vendedores": distinct_values(rows, "vendedor"),
        "clientes": distinct_values(rows, "cliente"),
        "estados": distinct_values(rows, "estado"),
        "produtos": distinct_values(rows, "produto"),
        "linhas": distinct_values(rows, "linha_produto"),
        "pagadores": distinct_values(rows, "tipo_pagador"),
        "status": distinct_values(rows, "status"),
        "motivos_perda": distinct_values(rows, "motivo_perda"),
        "etapas_perda": distinct_values(rows, "etapa_perda"),
    }


SQL_SCHEMA = """
Tabela negocios (um registro por negócio da FH Saúde, 2021-2025):
- negocio TEXT PK (ex: FH-2021-00059)
- etapa1_cotacao, etapa2_autorizacao, etapa3_cirurgia, etapa4_faturamento TEXT (datas ISO ou vazio)
- status TEXT: Ganho | Perdido
- ganho INTEGER: 1 se ganho, 0 se perdido
- ano INTEGER, mes TEXT (YYYY-MM)
- vendedor, cliente, tipo_pagador, estado, produto, linha_produto TEXT
- valor REAL (pipeline)
- receita_ganha REAL (0 se perdido)
- valor_perdido REAL (0 se ganho)
- motivo_perda, etapa_perda TEXT (vazios se ganho)
- dias_consignacao, dias_pagamento, ciclo_total_dias REAL
- dias_cotacao_autorizacao, dias_cirurgia_faturamento REAL
- valor_glosado, valor_recuperado, glosa_nao_recuperada REAL

Receita líquida = SUM(receita_ganha) - SUM(glosa_nao_recuperada)
Win rate = AVG(ganho) * 100
Ticket médio = SUM(receita_ganha) / COUNT(ganho=1)
"""
