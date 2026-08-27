from __future__ import annotations

import json
import re
import sqlite3
import threading
from typing import Any

from rag.store import SQL_SCHEMA, get_catalog

_SQL_FORBIDDEN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|ATTACH|DETACH|PRAGMA|CREATE|REPLACE|VACUUM|INTO|TRIGGER|GRANT|REVOKE)\b",
    re.IGNORECASE,
)

GROUP_FIELDS = {
    "ano": "ano",
    "mes": "mes",
    "vendedor": "vendedor",
    "cliente": "cliente",
    "produto": "produto",
    "linha": "linha_produto",
    "linha_produto": "linha_produto",
    "estado": "estado",
    "pagador": "tipo_pagador",
    "tipo_pagador": "tipo_pagador",
    "status": "status",
    "motivo_perda": "motivo_perda",
    "etapa_perda": "etapa_perda",
}


def _fmt_rows(rows: list[dict[str, Any]], limit: int = 40) -> str:
    clipped = rows[:limit]
    return json.dumps(clipped, ensure_ascii=False, default=str, indent=2)


class QueryTools:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.lock = threading.Lock()
        self.calls: list[dict[str, Any]] = []

    def reset_calls(self) -> None:
        self.calls = []

    def _log(self, name: str, args: dict[str, Any], preview: str) -> None:
        self.calls.append({"name": name, "args": args, "preview": preview[:280]})

    def executar_sql(self, sql: str) -> str:
        """Executa SQL SELECT na tabela negocios da FH Saúde. Use para números exatos, rankings, filtros cruzados e comparações. Apenas SELECT. Sempre inclua LIMIT (máx 80). Valores em reais."""
        original = sql
        sql = sql.strip().rstrip(";")
        if not sql.lower().startswith("select"):
            return "Erro: apenas SELECT é permitido."
        if _SQL_FORBIDDEN.search(sql):
            return "Erro: comando SQL não permitido."
        if "limit" not in sql.lower():
            sql += " LIMIT 50"
        try:
            with self.lock:
                cur = self.conn.execute(sql)
                cols = [d[0] for d in cur.description]
                rows = [dict(zip(cols, row)) for row in cur.fetchall()]
            preview = _fmt_rows(rows)
            self._log("executar_sql", {"sql": original}, preview)
            if not rows:
                return "Consulta sem resultados."
            return preview
        except sqlite3.Error as exc:
            return f"Erro SQL: {exc}\nEsquema:\n{SQL_SCHEMA}"

    def agregar_metricas(
        self,
        agrupamento: str,
        ano: str | None = None,
        estado: str | None = None,
        vendedor: str | None = None,
        cliente: str | None = None,
        produto: str | None = None,
        linha_produto: str | None = None,
        tipo_pagador: str | None = None,
        status: str | None = None,
        limite: int = 20,
    ) -> str:
        """Agrega KPIs (deals, ganhos, perdidos, win_rate, receita_ganha, receita_liquida, valor_perdido, glosa, ticket_medio, DSO). agrupamento: ano, mes, vendedor, cliente, produto, linha, estado, pagador, status, motivo_perda, etapa_perda."""
        field = GROUP_FIELDS.get((agrupamento or "").strip().lower())
        if not field:
            return f"Agrupamento inválido. Use: {', '.join(sorted(set(GROUP_FIELDS)))}"

        filters = {
            "ano": ano,
            "estado": estado,
            "vendedor": vendedor,
            "cliente": cliente,
            "produto": produto,
            "linha_produto": linha_produto,
            "tipo_pagador": tipo_pagador,
            "status": status,
        }
        where = []
        params: list[Any] = []
        for col, value in filters.items():
            if value not in (None, ""):
                where.append(f"{col} = ?")
                params.append(int(value) if col == "ano" else value)

        where_sql = f"WHERE {' AND '.join(where)}" if where else ""
        limit = max(1, min(int(limite or 20), 50))
        sql = f"""
            SELECT
                {field} AS grupo,
                COUNT(*) AS deals,
                SUM(ganho) AS ganhos,
                SUM(CASE WHEN status = 'Perdido' THEN 1 ELSE 0 END) AS perdidos,
                ROUND(AVG(ganho) * 100.0, 1) AS win_rate,
                ROUND(SUM(valor), 2) AS pipeline,
                ROUND(SUM(receita_ganha), 2) AS receita_ganha,
                ROUND(SUM(receita_ganha) - SUM(glosa_nao_recuperada), 2) AS receita_liquida,
                ROUND(SUM(valor_perdido), 2) AS valor_perdido,
                ROUND(SUM(valor_glosado), 2) AS valor_glosado,
                ROUND(SUM(valor_recuperado), 2) AS valor_recuperado,
                ROUND(SUM(glosa_nao_recuperada), 2) AS glosa_nao_recuperada,
                ROUND(SUM(receita_ganha) / NULLIF(SUM(ganho), 0), 2) AS ticket_medio,
                ROUND(AVG(CASE WHEN ganho = 1 THEN dias_pagamento END), 1) AS dso_medio,
                ROUND(AVG(CASE WHEN ganho = 1 THEN ciclo_total_dias END), 1) AS ciclo_medio
            FROM negocios
            {where_sql}
            GROUP BY {field}
            ORDER BY receita_ganha DESC
            LIMIT {limit}
        """
        try:
            with self.lock:
                cur = self.conn.execute(sql, params)
                cols = [d[0] for d in cur.description]
                rows = [dict(zip(cols, row)) for row in cur.fetchall()]
            preview = _fmt_rows(rows)
            self._log("agregar_metricas", {"agrupamento": agrupamento, **filters}, preview)
            return preview if rows else "Sem dados para esse recorte."
        except sqlite3.Error as exc:
            return f"Erro ao agregar: {exc}"

    def perfil_entidade(self, tipo: str, nome: str) -> str:
        """Perfil detalhado de uma entidade. tipo: vendedor, cliente, produto, estado, pagador, linha. nome: valor exato ou parcial."""
        mapping = {
            "vendedor": "vendedor",
            "cliente": "cliente",
            "produto": "produto",
            "estado": "estado",
            "pagador": "tipo_pagador",
            "tipo_pagador": "tipo_pagador",
            "linha": "linha_produto",
            "linha_produto": "linha_produto",
        }
        field = mapping.get((tipo or "").strip().lower())
        if not field:
            return f"Tipo inválido. Use: {', '.join(sorted(set(mapping)))}"
        sql = f"""
            SELECT
                {field} AS nome,
                COUNT(*) AS deals,
                SUM(ganho) AS ganhos,
                ROUND(AVG(ganho) * 100.0, 1) AS win_rate,
                ROUND(SUM(receita_ganha), 2) AS receita_ganha,
                ROUND(SUM(receita_ganha) - SUM(glosa_nao_recuperada), 2) AS receita_liquida,
                ROUND(SUM(valor_perdido), 2) AS valor_perdido,
                ROUND(SUM(glosa_nao_recuperada), 2) AS glosa_nao_recuperada,
                ROUND(AVG(CASE WHEN ganho = 1 THEN dias_pagamento END), 1) AS dso_medio,
                ROUND(AVG(CASE WHEN ganho = 1 THEN ciclo_total_dias END), 1) AS ciclo_medio
            FROM negocios
            WHERE {field} LIKE ?
            GROUP BY {field}
            ORDER BY receita_ganha DESC
            LIMIT 8
        """
        with self.lock:
            cur = self.conn.execute(sql, (f"%{nome}%",))
            cols = [d[0] for d in cur.description]
            rows = [dict(zip(cols, row)) for row in cur.fetchall()]
        if not rows:
            catalog = get_catalog()
            hint_key = {
                "vendedor": "vendedores",
                "cliente": "clientes",
                "produto": "produtos",
                "estado": "estados",
                "tipo_pagador": "pagadores",
                "linha_produto": "linhas",
            }[field]
            options = ", ".join(catalog[hint_key][:12])
            return f"Nada encontrado para {tipo}='{nome}'. Exemplos: {options}"

        names = [r["nome"] for r in rows]
        placeholders = ",".join("?" * len(names))
        extra_sql = f"""
            SELECT motivo_perda, COUNT(*) AS qtd, ROUND(SUM(valor_perdido), 2) AS valor
            FROM negocios
            WHERE {field} IN ({placeholders}) AND status = 'Perdido' AND motivo_perda != ''
            GROUP BY motivo_perda
            ORDER BY valor DESC
            LIMIT 5
        """
        with self.lock:
            cur = self.conn.execute(extra_sql, names)
            losses = [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]
        payload = {"perfil": rows, "principais_perdas": losses}
        preview = json.dumps(payload, ensure_ascii=False, indent=2)
        self._log("perfil_entidade", {"tipo": tipo, "nome": nome}, preview)
        return preview

    def consultar_negocio(self, codigo: str) -> str:
        """Retorna o registro completo de um negócio pelo código, ex: FH-2024-00123."""
        with self.lock:
            cur = self.conn.execute(
                "SELECT * FROM negocios WHERE negocio LIKE ? LIMIT 5",
                (f"%{codigo.strip()}%",),
            )
            cols = [d[0] for d in cur.description]
            rows = [dict(zip(cols, row)) for row in cur.fetchall()]
        preview = _fmt_rows(rows)
        self._log("consultar_negocio", {"codigo": codigo}, preview)
        return preview if rows else f"Negócio '{codigo}' não encontrado."

    def listar_dimensoes(self, campo: str) -> str:
        """Lista valores distintos de um campo. campo: vendedor, cliente, produto, estado, pagador, linha, ano, motivo_perda, etapa_perda, status."""
        catalog = get_catalog()
        aliases = {
            "vendedor": "vendedores",
            "vendedores": "vendedores",
            "cliente": "clientes",
            "clientes": "clientes",
            "produto": "produtos",
            "produtos": "produtos",
            "estado": "estados",
            "estados": "estados",
            "pagador": "pagadores",
            "tipo_pagador": "pagadores",
            "linha": "linhas",
            "linha_produto": "linhas",
            "ano": "anos",
            "anos": "anos",
            "motivo_perda": "motivos_perda",
            "etapa_perda": "etapas_perda",
            "status": "status",
        }
        key = aliases.get((campo or "").strip().lower())
        if not key:
            return f"Campo inválido. Use: {', '.join(sorted(aliases))}"
        values = catalog[key]
        preview = json.dumps(values, ensure_ascii=False)
        self._log("listar_dimensoes", {"campo": campo}, preview)
        return preview
