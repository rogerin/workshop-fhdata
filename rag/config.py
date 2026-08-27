from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env", override=True)

CSV_PATH = ROOT / "fh-saude-vendas - fh-saude-vendas.csv.csv"
BUNDLE_PATH = ROOT / "data_bundle.json"
INDEX_DIR = ROOT / ".rag_index"

GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or "").strip().strip('"').strip("'")

# O SDK prioriza GOOGLE_API_KEY se as duas existirem. Forçamos a chave do .env.
if GEMINI_API_KEY:
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIM = 768
EMBED_BATCH = 80

# Melhor modelo disponível, com fallbacks se a conta não tiver acesso.
CHAT_MODELS = [
    "gemini-3.1-pro-preview",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
]
