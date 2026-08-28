from __future__ import annotations

import re
from typing import Any

from rag.store import get_catalog, load_bundle

PERSONAS: list[dict[str, str]] = [
    {
        "id": "ceo",
        "role": "CEO",
        "name": "Helena Vasconcelos",
        "title": "Estratégia & escala",
        "initials": "HV",
        "color": "#2AC59E",
        "soft": "rgba(42, 197, 158, 0.14)",
        "icon": "crown",
        "signature": "A meta não vale se o caixa quebrar no meio do caminho.",
        "focus": "R$ 110M em 5 anos, sem dívida e sem diluição. Capital de giro define a velocidade.",
    },
    {
        "id": "cfo",
        "role": "CFO",
        "name": "Eduardo Câmara",
        "title": "Finanças & caixa",
        "initials": "EC",
        "color": "#52E1B9",
        "soft": "rgba(82, 225, 185, 0.14)",
        "icon": "wallet",
        "signature": "Receita que não vira caixa é vaidade.",
        "focus": "DSO, glosa e receita líquida. Operadora verticalizada é o pior pagador.",
    },
    {
        "id": "coo",
        "role": "COO",
        "name": "Marina Teles",
        "title": "Operações & esteira",
        "initials": "MT",
        "color": "#E2B93B",
        "soft": "rgba(226, 185, 59, 0.16)",
        "icon": "sliders",
        "signature": "Ciclo curto bate headcount novo.",
        "focus": "Funil E1→E4, consignação e faturamento em 15 dias após a cirurgia.",
    },
    {
        "id": "chro",
        "role": "CHRO",
        "name": "Rafael Queiroz",
        "title": "Força comercial",
        "initials": "RQ",
        "color": "#FF6568",
        "soft": "rgba(255, 101, 104, 0.14)",
        "icon": "users",
        "signature": "Quem vende mais nem sempre gera mais.",
        "focus": "Premiar qualidade (ciclo curto, pouca glosa), não ranking de receita bruta.",
    },
    {
        "id": "cmo",
        "role": "CMO",
        "name": "Beatriz Lins",
        "title": "Produtos & mercado",
        "initials": "BL",
        "color": "#C2EAE8",
        "soft": "rgba(194, 234, 232, 0.16)",
        "icon": "target",
        "signature": "Pacote ganha de preço avulso.",
        "focus": "Bundling, mix AL/RN e fidelização médica contra perda por preço.",
    },
]

_LEAD_KEYS = {
    "ceo": ("meta", "110", "ceo", "crescimento", "escala", "estado", "nordeste", "estratégia", "estrategia"),
    "cfo": ("glosa", "dso", "caixa", "capital", "cfo", "pagador", "líquida", "liquida", "receita"),
    "coo": ("perda", "funil", "estoque", "ciclo", "coo", "cirurgia", "cotação", "cotacao", "operação", "operacao"),
    "chro": ("vendedor", "time", "comercial", "ranking", "chro", "equipe", "turnover"),
    "cmo": ("produto", "mix", "preço", "preco", "cmo", "linha", "portfólio", "portfolio", "cliente"),
}


def _brl(value: float | int | None) -> str:
    return f"R$ {float(value or 0):,.0f}".replace(",", ".")


def _pct(value: float | int | None) -> str:
    return f"{float(value or 0):.1f}%"


def _share(part: float, total: float) -> str:
    if not total:
        return "n/d"
    return f"{part / total * 100:.1f}%"


def _mentions(question: str, value: str) -> bool:
    q = (question or "").lower()
    token = str(value).lower().strip()
    if not token:
        return False
    if len(token) <= 3:
        return re.search(rf"(?<!\w){re.escape(token)}(?!\w)", q) is not None
    return token in q


def _lead_id(question: str) -> str:
    q = (question or "").lower()
    for persona_id, keys in _LEAD_KEYS.items():
        if any(key in q for key in keys):
            return persona_id
    return "ceo"


def _subject(question: str) -> str:
    catalog = get_catalog()
    q = (question or "").lower()
    bits = []
    for field, key in (
        ("vendedores", "vendedores"),
        ("clientes", "clientes"),
        ("produtos", "produtos"),
        ("linhas", "linhas"),
        ("estados", "estados"),
        ("anos", "anos"),
    ):
        for value in catalog[key]:
            if _mentions(question, value):
                bits.append(str(value))
    if bits:
        return ", ".join(bits[:3])
    clean = (question or "").strip()
    if len(clean) > 72:
        return clean[:69] + "…"
    return clean or "este recorte da base"


def build_board(question: str) -> list[dict[str, Any]]:
    bundle = load_bundle()
    summary = bundle["summary"]
    cycles = bundle["cycles"]
    sellers = bundle["sellers"]
    stages = bundle["loss_stages"]
    reasons = bundle["loss_reasons"]
    states = bundle["states"]
    payers = bundle["payers"]
    lines = bundle["lines"]
    products = bundle["products"]
    by_name = {row["vendedor"]: row for row in sellers}
    top_seller = sellers[0]
    efficient = by_name.get("Tatiana Coelho") or by_name.get("Joana Rios") or sellers[-1]
    top_state = states[0]
    top_payer = payers[0]
    top_line = lines[0]
    top_product = products[0]
    top_loss = reasons[0]
    top_stage = stages[0]
    last_year = bundle["years"][-1]
    tema = _subject(question)
    lead = _lead_id(question)

    tips = {
        "ceo": (
            f"Olhando «{tema}», eu não aprovo crescimento que ignore o teto de caixa. "
            f"O OKR é {_brl(110_000_000)} em 5 anos, sem dívida e sem diluição. "
            f"2025 já está em {_brl(last_year['receita_ganha'])} com win rate {_pct(last_year['win_rate'])}. "
            f"{top_state['estado']} concentra {_share(top_state['receita_ganha'], summary['receita_ganha'])} da receita "
            f"e o ciclo ainda é {cycles['ciclo_total']:.0f} dias. Minha dica: só escale o que couber no giro — "
            f"senão a empresa quebra antes dos R$ 70M."
        ),
        "cfo": (
            f"Em «{tema}» eu olho caixa, não top line. DSO {cycles['pagamento']:.0f} dias, "
            f"glosa não recuperada {_brl(summary['glosa_nao_recuperada'])} e receita líquida "
            f"{_brl(summary['receita_liquida'])}. {top_payer['tipo']} paga em "
            f"{top_payer['dias_pagamento_medio']:.0f} dias e leva {_brl(top_payer['glosa_nao_recuperada'])} de glosa perdida. "
            f"Minha dica: recuse volume que alonga DSO. Receita que não vira caixa é vaidade."
        ),
        "coo": (
            f"«{tema}» cai na esteira, não no slide. Cirurgia→faturamento {cycles['cirurgia_faturamento']:.0f}d, "
            f"consignação {cycles['consignacao']:.0f}d. {top_stage['etapa']} já queima "
            f"{_brl(top_stage['valor_perdido'])} ({top_stage['percentual_valor']}% das perdas). "
            f"Minha dica: SLA de cotação em 24h, estoque do que some em E1 e NF em 15 dias após a cirurgia. "
            f"Contratar gente sem enxugar ciclo só multiplica custo fixo."
        ),
        "chro": (
            f"Sobre «{tema}»: não me peçam para premiar {top_seller['vendedor']} só pelos "
            f"{_brl(top_seller['receita_ganha'])}. WR {_pct(top_seller['win_rate'])} e glosa perdida "
            f"{_pct(top_seller['taxa_glosa_perdida'])}. O modelo é {efficient['vendedor']} "
            f"(glosa {_pct(efficient['taxa_glosa_perdida'])}). "
            f"Minha dica: recorte o time por capital preso e win rate. Reter qualidade, não o Top 3 de volume."
        ),
        "cmo": (
            f"Em «{tema}» o mercado já nos disse o preço. «{top_loss['motivo']}» queimou "
            f"{_brl(top_loss['valor_perdido'])} ({top_loss['percentual_valor']}% das perdas). "
            f"{top_line['linha']} puxa {_brl(top_line['receita_ganha'])} e {top_product['produto']} "
            f"é âncora ({_brl(top_product['receita_ganha'])}). "
            f"Minha dica: pare de vender item avulso. Empacote implante + consumo, fidelize o corpo clínico "
            f"e use AL/RN para diluir a dependência de PE."
        ),
    }

    board = []
    for persona in PERSONAS:
        item = dict(persona)
        item["tip"] = tips[persona["id"]]
        item["lead"] = persona["id"] == lead
        board.append(item)
    return board


def public_personas() -> list[dict[str, str]]:
    return [
        {
            "id": p["id"],
            "role": p["role"],
            "name": p["name"],
            "title": p["title"],
            "initials": p["initials"],
            "color": p["color"],
            "icon": p["icon"],
            "signature": p["signature"],
            "focus": p["focus"],
        }
        for p in PERSONAS
    ]
