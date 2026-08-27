from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any

import numpy as np
from google import genai
from google.genai import types

from rag.config import (
    BUNDLE_PATH,
    CSV_PATH,
    EMBED_BATCH,
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    INDEX_DIR,
)
from rag.store import load_bundle, load_rows


def _source_fingerprint() -> str:
    parts = []
    for path in (CSV_PATH, BUNDLE_PATH):
        stat = path.stat()
        parts.append(f"{path.name}:{stat.st_mtime_ns}:{stat.st_size}")
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]


def _brl(value: float) -> str:
    return f"R$ {value:,.0f}".replace(",", ".")


def _deal_chunk(row: dict[str, Any]) -> str:
    if row["status"] == "Ganho":
        extra = (
            f"Receita ganha {_brl(row['receita_ganha'])}. "
            f"Glosado {_brl(row['valor_glosado'])}, recuperado {_brl(row['valor_recuperado'])}, "
            f"glosa não recuperada {_brl(row['glosa_nao_recuperada'])}. "
            f"Ciclo {row['ciclo_total_dias']:.0f} dias, consignação {row['dias_consignacao']:.0f}d, "
            f"pagamento {row['dias_pagamento']:.0f}d."
        )
    else:
        extra = (
            f"Valor perdido {_brl(row['valor_perdido'])}. "
            f"Motivo: {row.get('motivo_perda') or 'não informado'}. "
            f"Etapa da perda: {row.get('etapa_perda') or 'não informada'}."
        )
    return (
        f"Negócio {row['negocio']} | {row['status']} | {row['ano']} ({row['mes']}). "
        f"Vendedor {row['vendedor']}. Cliente {row['cliente']} ({row['tipo_pagador']}) em {row['estado']}. "
        f"Produto {row['produto']} da linha {row['linha_produto']}. Pipeline {_brl(row['valor'])}. {extra}"
    )


def _json_chunk(title: str, payload: Any) -> str:
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    return f"{title}\n{body}"


def build_chunks() -> list[dict[str, str]]:
    rows = load_rows()
    bundle = load_bundle()
    chunks: list[dict[str, str]] = []

    chunks.append(
        {
            "id": "kpis-globais",
            "kind": "kpi",
            "text": _json_chunk(
                "KPIs globais da FH Saúde (base completa 2021-2025). Meta estratégica: R$ 110 milhões em 5 anos, sem dívida e sem diluição.",
                bundle["summary"],
            ),
        }
    )
    chunks.append(
        {
            "id": "ciclos",
            "kind": "kpi",
            "text": _json_chunk(
                "Ciclo operacional médio dos negócios ganhos: cotação→autorização, cirurgia→faturamento, consignação, DSO (dias de pagamento) e ciclo total.",
                bundle["cycles"],
            ),
        }
    )

    for item in bundle["years"]:
        chunks.append(
            {
                "id": f"ano-{item['ano']}",
                "kind": "ano",
                "text": _json_chunk(f"Resumo anual {item['ano']} da FH Saúde.", item),
            }
        )
    for item in bundle["payers"]:
        chunks.append(
            {
                "id": f"pagador-{item['tipo']}",
                "kind": "pagador",
                "text": _json_chunk(f"Perfil do tipo de pagador {item['tipo']}.", item),
            }
        )
    for item in bundle["states"]:
        chunks.append(
            {
                "id": f"estado-{item['estado']}",
                "kind": "estado",
                "text": _json_chunk(f"Performance comercial no estado {item['estado']}.", item),
            }
        )
    for item in bundle["lines"]:
        chunks.append(
            {
                "id": f"linha-{item['linha']}",
                "kind": "linha",
                "text": _json_chunk(f"Linha de produto {item['linha']}.", item),
            }
        )
    for item in bundle["products"]:
        chunks.append(
            {
                "id": f"produto-{item['produto']}",
                "kind": "produto",
                "text": _json_chunk(f"Produto {item['produto']} ({item['linha']}).", item),
            }
        )
    for item in bundle["sellers"]:
        chunks.append(
            {
                "id": f"vendedor-{item['vendedor']}",
                "kind": "vendedor",
                "text": _json_chunk(
                    f"Perfil comercial do vendedor {item['vendedor']}, incluindo receita, win rate, glosa e principais motivos de perda.",
                    item,
                ),
            }
        )
    for item in bundle["top_clients"]:
        chunks.append(
            {
                "id": f"cliente-{item['cliente']}",
                "kind": "cliente",
                "text": _json_chunk(
                    f"Cliente {item['cliente']} ({item['tipo']}, {item['estado']}).",
                    item,
                ),
            }
        )
    for item in bundle["loss_reasons"]:
        chunks.append(
            {
                "id": f"perda-{item['motivo'][:40]}",
                "kind": "perda",
                "text": _json_chunk(f"Motivo de perda: {item['motivo']}.", item),
            }
        )
    for item in bundle["loss_stages"]:
        chunks.append(
            {
                "id": f"etapa-perda-{item['etapa']}",
                "kind": "etapa",
                "text": _json_chunk(f"Perdas na etapa {item['etapa']}.", item),
            }
        )

    by_month = bundle["months"]
    for start in range(0, len(by_month), 6):
        slice_ = by_month[start : start + 6]
        label = f"{slice_[0]['mes']} a {slice_[-1]['mes']}"
        chunks.append(
            {
                "id": f"meses-{slice_[0]['mes']}",
                "kind": "mes",
                "text": _json_chunk(f"Série mensal de receita e win rate ({label}).", slice_),
            }
        )

    by_seller: dict[str, list] = {}
    by_loss: dict[str, list] = {}
    for row in rows:
        by_seller.setdefault(row["vendedor"], []).append(row)
        if row["status"] == "Perdido" and row.get("motivo_perda"):
            by_loss.setdefault(row["motivo_perda"], []).append(row)

    for seller, deals in by_seller.items():
        wins = sorted(
            (d for d in deals if d["status"] == "Ganho"),
            key=lambda d: d["receita_ganha"],
            reverse=True,
        )[:4]
        losses = sorted(
            (d for d in deals if d["status"] == "Perdido"),
            key=lambda d: d["valor_perdido"],
            reverse=True,
        )[:4]
        sample = "\n".join(_deal_chunk(d) for d in wins + losses)
        chunks.append(
            {
                "id": f"amostras-{seller}",
                "kind": "amostra",
                "text": f"Amostras de negócios do vendedor {seller} (maiores ganhos e perdas).\n{sample}",
            }
        )

    for motivo, deals in by_loss.items():
        sample = "\n".join(
            _deal_chunk(d)
            for d in sorted(deals, key=lambda d: d["valor_perdido"], reverse=True)[:5]
        )
        chunks.append(
            {
                "id": f"casos-{motivo[:32]}",
                "kind": "caso",
                "text": f"Casos ilustrativos do motivo de perda '{motivo}'.\n{sample}",
            }
        )
    return chunks


_TOKEN = re.compile(r"[a-zA-ZÀ-ÿ0-9_]+")


def _tokens(text: str) -> list[str]:
    return [tok.lower() for tok in _TOKEN.findall(text) if len(tok) > 1]


def _tfidf_matrix(texts: list[str]) -> tuple[np.ndarray, dict[str, int], dict[str, int]]:
    docs = [_tokens(text) for text in texts]
    df: dict[str, int] = {}
    for doc in docs:
        for tok in set(doc):
            df[tok] = df.get(tok, 0) + 1
    vocab = {tok: idx for idx, tok in enumerate(sorted(df))}
    n_docs = max(len(texts), 1)
    matrix = np.zeros((len(texts), len(vocab)), dtype=np.float32)
    for i, doc in enumerate(docs):
        counts: dict[str, int] = {}
        for tok in doc:
            counts[tok] = counts.get(tok, 0) + 1
        peak = max(counts.values()) if counts else 1
        for tok, freq in counts.items():
            tf = 0.5 + 0.5 * (freq / peak)
            idf = float(np.log((n_docs + 1) / (df[tok] + 1)) + 1)
            matrix[i, vocab[tok]] = tf * idf
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms, vocab, df


def _tfidf_query(query: str, vocab: dict[str, int], df: dict[str, int], n_docs: int) -> np.ndarray:
    vec = np.zeros(len(vocab), dtype=np.float32)
    counts: dict[str, int] = {}
    for tok in _tokens(query):
        if tok in vocab:
            counts[tok] = counts.get(tok, 0) + 1
    peak = max(counts.values()) if counts else 1
    for tok, freq in counts.items():
        tf = 0.5 + 0.5 * (freq / peak)
        idf = float(np.log((n_docs + 1) / (df[tok] + 1)) + 1)
        vec[vocab[tok]] = tf * idf
    norm = np.linalg.norm(vec)
    return vec / norm if norm else vec


def _embed_batch(client: genai.Client, texts: list[str], task_type: str) -> np.ndarray:
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            result = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=texts,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=EMBEDDING_DIM,
                ),
            )
            matrix = np.array([e.values for e in result.embeddings], dtype=np.float32)
            norms = np.linalg.norm(matrix, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            return matrix / norms
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            text = str(exc)
            code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
            if code in {401, 403, 429} or "RESOURCE_EXHAUSTED" in text or "429" in text:
                break
            time.sleep(1.2 * (attempt + 1))
    raise RuntimeError(f"Falha ao gerar embeddings: {last_error}") from last_error


class LocalIndex:
    def __init__(self, client: genai.Client):
        self.client = client
        self.chunks: list[dict[str, str]] = []
        self.vectors: np.ndarray | None = None
        self.backend = EMBEDDING_MODEL
        self.vocab: dict[str, int] = {}
        self.df: dict[str, int] = {}

    @property
    def ready(self) -> bool:
        return self.vectors is not None and len(self.chunks) > 0

    def load_or_build(self, progress=None) -> None:
        INDEX_DIR.mkdir(exist_ok=True)
        meta_path = INDEX_DIR / "meta.json"
        vec_path = INDEX_DIR / "vectors.npy"
        chunks_path = INDEX_DIR / "chunks.json"
        vocab_path = INDEX_DIR / "vocab.json"
        fingerprint = _source_fingerprint()

        if meta_path.exists() and vec_path.exists() and chunks_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if meta.get("fingerprint") == fingerprint:
                self.chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
                self.vectors = np.load(vec_path)
                self.backend = meta.get("model", EMBEDDING_MODEL)
                if self.backend == "tfidf-local" and vocab_path.exists():
                    payload = json.loads(vocab_path.read_text(encoding="utf-8"))
                    self.vocab = payload["vocab"]
                    self.df = payload["df"]
                if progress:
                    progress(f"Índice local carregado ({len(self.chunks)} trechos, {self.backend}).")
                return

        self.chunks = build_chunks()
        total = len(self.chunks)
        try:
            if progress:
                progress(f"Indexando {total} trechos com {EMBEDDING_MODEL}...")
            vectors: list[np.ndarray] = []
            for start in range(0, total, EMBED_BATCH):
                batch = self.chunks[start : start + EMBED_BATCH]
                vectors.append(
                    _embed_batch(self.client, [c["text"] for c in batch], "RETRIEVAL_DOCUMENT")
                )
                if progress:
                    progress(f"Embeddings {min(start + EMBED_BATCH, total)}/{total}")
            self.vectors = np.vstack(vectors)
            self.backend = EMBEDDING_MODEL
        except Exception as exc:  # noqa: BLE001
            if progress:
                progress(f"Embeddings Gemini indisponíveis ({exc}). Usando índice TF-IDF local.")
            self.vectors, self.vocab, self.df = _tfidf_matrix([c["text"] for c in self.chunks])
            self.backend = "tfidf-local"
            vocab_path.write_text(
                json.dumps({"vocab": self.vocab, "df": self.df}, ensure_ascii=False),
                encoding="utf-8",
            )

        np.save(vec_path, self.vectors)
        chunks_path.write_text(json.dumps(self.chunks, ensure_ascii=False), encoding="utf-8")
        meta_path.write_text(
            json.dumps(
                {
                    "fingerprint": fingerprint,
                    "model": self.backend,
                    "dim": int(self.vectors.shape[1]),
                    "count": len(self.chunks),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        if progress:
            progress(f"Índice RAG pronto: {len(self.chunks)} trechos ({self.backend}).")

    def search(self, query: str, k: int = 10) -> list[dict[str, Any]]:
        if not self.ready:
            return []
        if self.backend == "tfidf-local":
            query_vec = _tfidf_query(query, self.vocab, self.df, len(self.chunks))
        else:
            query_vec = _embed_batch(self.client, [query], "RETRIEVAL_QUERY")[0]
        scores = self.vectors @ query_vec
        top = np.argsort(scores)[::-1][:k]
        hits = []
        for idx in top:
            chunk = self.chunks[int(idx)]
            hits.append(
                {
                    "id": chunk["id"],
                    "kind": chunk["kind"],
                    "score": float(scores[int(idx)]),
                    "text": chunk["text"][:1800],
                }
            )
        return hits
