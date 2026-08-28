from __future__ import annotations

import json
import threading
from typing import Any

from rag.config import CHAT_MODELS, GEMINI_API_KEY
from google import genai
from google.genai import types

from rag.index import LocalIndex
from rag.local_analyst import answer_locally
from rag.c_suite import build_board
from rag.store import SQL_SCHEMA, build_sqlite, get_catalog, load_bundle, load_rows
from rag.tools import QueryTools

SYSTEM_PROMPT = """Você é a MESA C-SUITE da FH Saúde (distribuidora de materiais médicos no Nordeste).
Responda SEMPRE em português brasileiro.

Formato OBRIGATÓRIO de toda resposta:
1) Um bloco curto **Síntese da base** (números exatos da pergunta, 4–8 linhas).
2) Depois, exatamente estas cinco cadeiras, nesta ordem, cada uma com UMA dica acionável ligada à pergunta:
### CEO · Estratégia
### CFO · Finanças e caixa
### COO · Operações
### CHRO · Força comercial
### CMO · Produtos e mercado

Cada dica deve:
- Falar na primeira pessoa da cadeira ("Do meu lado…") ou no tom de diretriz daquela cadeira.
- Usar 1–2 números reais da base (nunca inventar).
- Terminar com uma ação concreta desta semana / deste trimestre.
- NÃO repetir o mesmo conselho nas cinco cadeiras. Cada um vê o mesmo fato pelo seu OKR.

Lentes fixas da empresa:
- CEO: R$ 110M em 5 anos sem dívida e sem diluição. Capital de giro define a velocidade. PE concentra ~76% da receita.
- CFO: DSO ~125d, glosa não recuperada, receita líquida = receita ganha − glosa não recuperada. Operadora verticalizada é o pior pagador.
- COO: Funil E1 Cotação → E2 Autorização → E3 Cirurgia → E4 Faturamento. Gargalo cirurgia→faturamento ~58d, consignação ~40d. Perda dominante em E1.
- CHRO: Não ranquear vendedor por receita bruta. Premiar quem consome menos capital (ciclo curto, pouca glosa). Reter qualidade, turnover < 15%.
- CMO: Perda por preço é o maior buraco. Bundling de pacotes cirúrgicos, mix AL/RN, fidelização médica.

Regras de dado:
- Use as ferramentas para números exatos.
- Formate dinheiro em R$ com milhar. Percentuais com 1 casa.
- Se faltar filtro, assuma 2021-2025 e diga isso.

{schema}

Catálogo resumido da base:
{catalog}
"""


class ChatEngine:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY ausente no .env")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_id = "analista-local"
        self.gemini_ok = False
        self._index_status = "carregando CSV e SQLite"
        self._ready = False
        self._warm_lock = threading.Lock()
        self.rows = load_rows()
        self.bundle = load_bundle()
        self.conn = build_sqlite(self.rows)
        self.tools = QueryTools(self.conn)
        self.index = LocalIndex(self.client)

    @property
    def status(self) -> dict[str, Any]:
        return {
            "ready": self._ready,
            "index": self._index_status,
            "model": self.model_id,
            "deals": len(self.rows),
            "chunks": len(self.index.chunks),
            "retriever": getattr(self.index, "backend", "pendente"),
            "gemini": self.gemini_ok,
        }

    def warmup(self) -> None:
        with self._warm_lock:
            if self._ready:
                return
            self.index.load_or_build(progress=self._set_index)
            self.model_id = self._pick_model()
            self._ready = True
            self._index_status = (
                f"pronto ({len(self.index.chunks)} trechos, {self.model_id}, "
                f"retriever {self.index.backend})"
            )

    def _set_index(self, message: str) -> None:
        self._index_status = message
        print(f"[RAG] {message}", flush=True)

    def _pick_model(self) -> str:
        for model in CHAT_MODELS:
            try:
                self.client.models.generate_content(
                    model=model,
                    contents="Responda apenas: ok",
                    config=types.GenerateContentConfig(max_output_tokens=8),
                )
                self.gemini_ok = True
                print(f"[RAG] Modelo ativo: {model}", flush=True)
                return model
            except Exception as exc:  # noqa: BLE001
                print(f"[RAG] Modelo indisponível ({model}): {exc}", flush=True)
                if "429" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc):
                    break
        self.gemini_ok = False
        print("[RAG] Gemini indisponível. Chat segue com analista local sobre SQL+RAG.", flush=True)
        return "analista-local"

    def _system(self) -> str:
        catalog = get_catalog()
        compact = {
            "anos": catalog["anos"],
            "estados": catalog["estados"],
            "linhas": catalog["linhas"],
            "pagadores": catalog["pagadores"],
            "vendedores": catalog["vendedores"],
            "produtos": catalog["produtos"],
            "n_clientes": len(catalog["clientes"]),
            "motivos_perda": catalog["motivos_perda"],
        }
        return SYSTEM_PROMPT.format(
            schema=SQL_SCHEMA,
            catalog=json.dumps(compact, ensure_ascii=False, indent=2),
        )

    def ask(self, question: str, history: list[dict[str, str]] | None = None) -> dict[str, Any]:
        if not self._ready:
            self.warmup()

        self.tools.reset_calls()
        hits = self.index.search(question, k=8)
        retrieved = "\n\n".join(
            f"[{h['kind']} | {h['id']} | score={h['score']:.3f}]\n{h['text']}" for h in hits
        )

        contents: list[types.Content] = []
        for turn in (history or [])[-8:]:
            role = "user" if turn.get("role") == "user" else "model"
            text = (turn.get("content") or "").strip()
            if text:
                contents.append(types.Content(role=role, parts=[types.Part(text=text)]))

        user_blob = (
            f"Pergunta do executivo:\n{question}\n\n"
            f"Trechos recuperados pelo RAG local (use como pista, confirme números nas ferramentas):\n{retrieved}"
        )
        contents.append(types.Content(role="user", parts=[types.Part(text=user_blob)]))

        sources = [
            {"id": h["id"], "kind": h["kind"], "score": round(h["score"], 3)}
            for h in hits[:6]
        ]

        if self.gemini_ok:
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=self._system(),
                        tools=[
                            self.tools.executar_sql,
                            self.tools.agregar_metricas,
                            self.tools.perfil_entidade,
                            self.tools.consultar_negocio,
                            self.tools.listar_dimensoes,
                        ],
                        max_output_tokens=4096,
                    ),
                )
                answer = _extract_text(response)
                if answer:
                    return {
                        "answer": answer,
                        "model": self.model_id,
                        "sources": sources,
                        "tools": self.tools.calls,
                        "board": build_board(question),
                    }
            except Exception as exc:  # noqa: BLE001
                print(f"[RAG] Gemini falhou na pergunta, usando analista local: {exc}", flush=True)
                self.gemini_ok = False

        answer = answer_locally(question, self.tools, hits)
        if not self.gemini_ok:
            answer = (
                "> Gemini está com limite de billing na `GEMINI_API_KEY`. "
                "Resposta gerada pelo analista local sobre SQL + RAG da base. "
                "Quando a cota voltar, o chat usa o melhor modelo Gemini automaticamente.\n\n"
                + answer
            )
        return {
            "answer": answer,
            "model": "analista-local",
            "sources": sources,
            "tools": self.tools.calls,
            "board": build_board(question),
        }


_engine: ChatEngine | None = None
_engine_lock = threading.Lock()


def peek_engine() -> ChatEngine | None:
    return _engine


def get_engine() -> ChatEngine:
    global _engine
    with _engine_lock:
        if _engine is None:
            _engine = ChatEngine()
    _engine.warmup()
    return _engine


def _extract_text(response: Any) -> str:
    text = getattr(response, "text", None)
    if text:
        return text.strip()
    try:
        parts = response.candidates[0].content.parts
    except (AttributeError, IndexError, TypeError):
        return ""
    chunks = []
    for part in parts or []:
        value = getattr(part, "text", None)
        if value:
            chunks.append(value)
    return "\n".join(chunks).strip()
