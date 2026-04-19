from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import chromadb

BASE_DIR = Path(__file__).resolve().parent.parent
REG_DIR = BASE_DIR / "data" / "regulations"
CHROMA_DIR = BASE_DIR / "artifacts" / "chroma_db"
COLLECTION_NAME = "lending_regulations"


def get_chroma_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
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


if __name__ == "__main__":
    ingest_regulations()