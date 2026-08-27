from __future__ import annotations

import json
import re
from typing import Any

from rag.store import get_catalog, load_bundle
from rag.tools import QueryTools

_META = 110_000_000


def _brl(value: float | int | None) -> str:
    number = float(value or 0)
    return f"R$ {number:,.0f}".replace(",", ".")


def _pct(value: float | int | None) -> str:
    return f"{float(value or 0):.1f}%"


def _parse_json(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _mentioned(question: str, values: list[str]) -> list[str]:
    q = question.lower()
    hits = []
    for value in values:
        if value and value.lower() in q:
            hits.append(value)
    return hits


def answer_locally(question: str, tools: QueryTools, hits: list[dict[str, Any]]) -> str:
    catalog = get_catalog()
    bundle = load_bundle()
    q = question.lower()
    tools.reset_calls()

    years = _mentioned(q, catalog["anos"])
    sellers = _mentioned(q, catalog["vendedores"])
    states = _mentioned(q, catalog["estados"])
    products = _mentioned(q, catalog["produtos"])
    lines = _mentioned(q, catalog["linhas"])
    payers = _mentioned(q, catalog["pagadores"])
    clients = _mentioned(q, catalog["clientes"])

    year = years[0] if years else None
    sections: list[str] = []

    if any(k in q for k in ("110", "meta", "cagr", "escala", "crescimento")):
        sections.append(_meta_path(tools, bundle))
    if any(k in q for k in ("dso", "capital", "ciclo", "consign", "pagamento", "caixa")):
        sections.append(_capital(tools, year, sellers))
    if any(k in q for k in ("perda", "perdid", "win rate", "convers", "cotação", "cotacao", "funil")):
        sections.append(_losses(tools, year))
    if any(k in q for k in ("glosa", "líquida", "liquida")):
        sections.append(_glosa(tools, year))
    if sellers:
        for seller in sellers[:3]:
            sections.append(_entity(tools, "vendedor", seller))
    if clients:
        for client in clients[:2]:
            sections.append(_entity(tools, "cliente", client))
    if products:
        for product in products[:2]:
            sections.append(_entity(tools, "produto", product))
    if lines:
        for line in lines[:3]:
            sections.append(_entity(tools, "linha", line))
    if states:
        for state in states[:3]:
            sections.append(_entity(tools, "estado", state))
    if payers:
        for payer in payers[:2]:
            sections.append(_entity(tools, "pagador", payer))
    if any(k in q for k in ("vendedor", "time", "comercial", "ranking")) and not sellers:
        sections.append(_ranking(tools, "vendedor", year, "Força comercial"))
    if any(k in q for k in ("produto", "mix", "linha")) and not products and not lines:
        sections.append(_ranking(tools, "linha", year, "Mix de linhas"))
        sections.append(_ranking(tools, "produto", year, "Produtos"))
    if any(k in q for k in ("cliente", "hospital", "operadora")) and not clients:
        sections.append(_ranking(tools, "cliente", year, "Clientes"))
    if any(k in q for k in ("ano", "evolu", "série", "serie", "202")) or year:
        sections.append(_years(tools, year))
    if not sections:
        sections.append(_overview(tools, bundle))
        sections.append(_losses(tools, year))

    rag_bits = []
    for hit in hits[:4]:
        rag_bits.append(f"- `{hit['kind']}` {hit['id']}")

    body = "\n\n".join(part for part in sections if part)
    return (
        f"{body}\n\n"
        f"**Recorte:** base FH Saúde 2021-2025"
        f"{' · filtro ' + ', '.join(years+sellers+states+lines) if years or sellers or states or lines else ''}.\n"
        f"**Fontes RAG:**\n" + "\n".join(rag_bits)
    )


def _overview(tools: QueryTools, bundle: dict[str, Any]) -> str:
    summary = bundle["summary"]
    years = _parse_json(tools.agregar_metricas("ano")) or []
    last = years[-1] if years else {}
    return (
        "## Visão geral da base\n"
        f"- **{summary['total_deals']} negócios** · win rate {_pct(summary['win_rate'])} "
        f"({summary['deals_ganhos']} ganhos / {summary['deals_perdidos']} perdidos)\n"
        f"- Receita ganha {_brl(summary['receita_ganha'])} · líquida {_brl(summary['receita_liquida'])}\n"
        f"- Valor perdido {_brl(summary['valor_perdido'])} · glosa não recuperada {_brl(summary['glosa_nao_recuperada'])}\n"
        f"- Ticket médio {_brl(summary['ticket_medio'])} · recuperação de glosa {_pct(summary['taxa_recuperacao_glosa'])}\n"
        f"- Último ano da base ({last.get('grupo', 'n/d')}): receita {_brl(last.get('receita_ganha'))}, "
        f"líquida {_brl(last.get('receita_liquida'))}, win rate {_pct(last.get('win_rate'))}."
    )


def _years(tools: QueryTools, year: str | None) -> str:
    rows = _parse_json(tools.agregar_metricas("ano", ano=year)) or []
    if not rows:
        return ""
    lines = ["## Evolução anual"]
    for row in rows:
        lines.append(
            f"- **{row['grupo']}**: receita {_brl(row['receita_ganha'])} · líquida {_brl(row['receita_liquida'])} · "
            f"win rate {_pct(row['win_rate'])} · perdido {_brl(row['valor_perdido'])} · DSO {row.get('dso_medio') or 0:.0f}d"
        )
    return "\n".join(lines)


def _ranking(tools: QueryTools, group: str, year: str | None, title: str) -> str:
    rows = _parse_json(tools.agregar_metricas(group, ano=year, limite=8)) or []
    if not rows:
        return ""
    lines = [f"## {title}"]
    for i, row in enumerate(rows, 1):
        lines.append(
            f"{i}. **{row['grupo']}** — {_brl(row['receita_ganha'])} líquida {_brl(row['receita_liquida'])} · "
            f"WR {_pct(row['win_rate'])} · glosa {_brl(row['glosa_nao_recuperada'])} · DSO {row.get('dso_medio') or 0:.0f}d"
        )
    return "\n".join(lines)


def _entity(tools: QueryTools, tipo: str, nome: str) -> str:
    payload = _parse_json(tools.perfil_entidade(tipo, nome)) or {}
    perfil = payload.get("perfil") or []
    perdas = payload.get("principais_perdas") or []
    if not perfil:
        return f"## {nome}\nSem dados."
    row = perfil[0]
    loss_txt = ", ".join(f"{p['motivo_perda']} ({_brl(p['valor'])})" for p in perdas[:3]) or "sem perdas relevantes"
    return (
        f"## {tipo.title()} · {row['nome']}\n"
        f"- Deals {row['deals']} · WR {_pct(row['win_rate'])} · receita {_brl(row['receita_ganha'])} · "
        f"líquida {_brl(row['receita_liquida'])}\n"
        f"- Perdido {_brl(row['valor_perdido'])} · glosa {_brl(row['glosa_nao_recuperada'])} · "
        f"DSO {row.get('dso_medio') or 0:.0f}d · ciclo {row.get('ciclo_medio') or 0:.0f}d\n"
        f"- Principais perdas: {loss_txt}."
    )


def _losses(tools: QueryTools, year: str | None) -> str:
    reasons = _parse_json(tools.agregar_metricas("motivo_perda", ano=year, status="Perdido", limite=8)) or []
    stages = _parse_json(tools.agregar_metricas("etapa_perda", ano=year, status="Perdido", limite=6)) or []
    lines = ["## Perdas e funil"]
    if stages:
        lines.append("Por etapa:")
        for row in stages:
            if not row["grupo"]:
                continue
            lines.append(f"- **{row['grupo']}**: {row['perdidos']} deals · {_brl(row['valor_perdido'])}")
    if reasons:
        lines.append("Por motivo:")
        for row in reasons:
            if not row["grupo"]:
                continue
            lines.append(f"- **{row['grupo']}**: {row['perdidos']} · {_brl(row['valor_perdido'])}")
    if stages and stages[0]["grupo"]:
        top = stages[0]
        lines.append(
            f"\nConclusão: o gargalo principal está em **{top['grupo']}** "
            f"({_brl(top['valor_perdido'])}). Ataque preço/contrato na cotação e autorização antes de empurrar volume."
        )
    return "\n".join(lines)


def _glosa(tools: QueryTools, year: str | None) -> str:
    rows = _parse_json(tools.agregar_metricas("linha", ano=year)) or []
    lines = ["## Glosa e receita líquida"]
    for row in rows:
        rec = float(row["receita_ganha"] or 0)
        glosa = float(row["glosa_nao_recuperada"] or 0)
        taxa = (glosa / rec * 100) if rec else 0
        lines.append(
            f"- **{row['grupo']}**: líquida {_brl(row['receita_liquida'])} · glosa {_brl(glosa)} ({_pct(taxa)})"
        )
    return "\n".join(lines)


def _capital(tools: QueryTools, year: str | None, sellers: list[str]) -> str:
    group = "vendedor"
    rows = _parse_json(tools.agregar_metricas(group, ano=year, limite=12)) or []
    ranked = sorted(rows, key=lambda r: float(r.get("dso_medio") or 0) * float(r.get("receita_ganha") or 0), reverse=True)
    lines = ["## Capital preso (DSO × receita)"]
    for row in ranked[:8]:
        dso = float(row.get("dso_medio") or 0)
        rec = float(row.get("receita_ganha") or 0)
        proxy = rec * dso / 365 if dso else 0
        lines.append(
            f"- **{row['grupo']}**: DSO {dso:.0f}d · ciclo {float(row.get('ciclo_medio') or 0):.0f}d · "
            f"glosa {_brl(row['glosa_nao_recuperada'])} · capital estimado {_brl(proxy)}"
        )
    if sellers:
        lines.append("Vendedores citados na pergunta entram no recorte acima.")
    return "\n".join(lines)


def _meta_path(tools: QueryTools, bundle: dict[str, Any]) -> str:
    years = _parse_json(tools.agregar_metricas("ano")) or []
    if len(years) < 2:
        return ""
    first = float(years[0]["receita_ganha"] or 0)
    last = float(years[-1]["receita_ganha"] or 0)
    n = max(len(years) - 1, 1)
    cagr = (last / first) ** (1 / n) - 1 if first else 0
    gap = _META - last
    lines = [
        "## Rota para R$ 110 milhões",
        f"- Receita ganha saiu de {_brl(first)} ({years[0]['grupo']}) para {_brl(last)} ({years[-1]['grupo']}).",
        f"- CAGR observado: {_pct(cagr * 100)} a.a.",
        f"- Distância da meta de {_brl(_META)}: {_brl(gap)} em receita ganha do último ano.",
        "- Sem dívida e sem diluição, o caminho é mix + ciclo de caixa: cortar perda em E1 Cotação, "
        "reduzir DSO dos vendedores que mais prendem capital e recuperar glosa nas linhas de maior ticket.",
    ]
    return "\n".join(lines)
