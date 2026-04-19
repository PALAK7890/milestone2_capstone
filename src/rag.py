from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Dict, List

import chromadb

BASE_DIR = Path(__file__).resolve().parent.parent
REG_DIR = BASE_DIR / "data" / "regulations"
CHROMA_SOURCE_DIR = BASE_DIR / "artifacts" / "chroma_db"
COLLECTION_NAME = "lending_regulations"

# Streamlit Cloud mounts the repo as read-only. ChromaDB needs write access,
# so we copy the committed DB to a writable temp directory on first use.
_WRITABLE_CHROMA_DIR: Path | None = None


def _get_chroma_dir() -> Path:
    global _WRITABLE_CHROMA_DIR
    if _WRITABLE_CHROMA_DIR is not None and _WRITABLE_CHROMA_DIR.exists():
        return _WRITABLE_CHROMA_DIR

    if CHROMA_SOURCE_DIR.exists():
        tmp_dir = Path(tempfile.gettempdir()) / "chroma_db_copy"
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir)
        shutil.copytree(CHROMA_SOURCE_DIR, tmp_dir)
        _WRITABLE_CHROMA_DIR = tmp_dir
        return _WRITABLE_CHROMA_DIR

    # Fallback: use the source path directly (works locally)
    return CHROMA_SOURCE_DIR


def get_chroma_collection():
    chroma_dir = _get_chroma_dir()
    client = chromadb.PersistentClient(path=str(chroma_dir))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return collection


def ingest_regulations():
    collection = get_chroma_collection()

    txt_files = sorted(REG_DIR.glob("*.txt"))
    if not txt_files:
        print("No regulation files found.")
        return

    existing = collection.get()
    existing_ids = set(existing.get("ids", [])) if existing else set()

    for file_path in txt_files:
        doc_id = file_path.stem
        if doc_id in existing_ids:
            continue

        text = file_path.read_text(encoding="utf-8")
        collection.add(
            ids=[doc_id],
            documents=[text],
            metadatas=[{"title": file_path.stem, "source": str(file_path.name)}],
        )

    print("Regulations ingested successfully.")


def retrieve_regulations(
    lending_query: str,
    borrower_profile: Dict,
    risk_class: str,
    recommended_action: str,
    top_k: int = 3,
) -> List[Dict[str, str]]:
    try:
        collection = get_chroma_collection()

        query_text = (
            f"{lending_query}. "
            f"Risk class: {risk_class}. "
            f"Recommended action: {recommended_action}. "
            f"Loan intent: {borrower_profile.get('loan_intent', '')}. "
            f"Default history: {borrower_profile.get('cb_person_default_on_file', '')}."
        )

        results = collection.query(query_texts=[query_text], n_results=top_k)

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        output = []
        for doc, meta in zip(documents, metadatas):
            output.append({
                "title": meta.get("title", "Untitled"),
                "source": meta.get("source", ""),
                "content": doc[:700] + ("..." if len(doc) > 700 else ""),
            })

        return output
    except Exception:
        return []


if __name__ == "__main__":
    ingest_regulations()