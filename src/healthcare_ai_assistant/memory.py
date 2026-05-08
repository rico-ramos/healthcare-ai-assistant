from __future__ import annotations

from datetime import datetime

from langchain_community.vectorstores import FAISS


class PatientMemory:
    """Per-patient in-memory FAISS index for session Q/A recall."""

    def __init__(self, embeddings):
        self._stores: dict = {}
        self._embeddings = embeddings

    def save(self, patient_name: str, query: str, response: str) -> None:
        key = patient_name.lower().strip()
        text = f"[Session] Q: {query} | A: {response[:400]}"
        metadata = [{"patient": patient_name, "ts": datetime.now().isoformat()}]
        if key not in self._stores:
            self._stores[key] = FAISS.from_texts([text], self._embeddings, metadatas=metadata)
        else:
            self._stores[key].add_texts([text], metadatas=metadata)

    def retrieve(self, patient_name: str, query: str, k: int = 3) -> str:
        key = patient_name.lower().strip()
        if key not in self._stores:
            return f'No prior session history found for "{patient_name}".'
        docs = self._stores[key].similarity_search(query, k=k)
        return "\n\n".join(f"[{i + 1}] {doc.page_content}" for i, doc in enumerate(docs))

    def count_for(self, patient_name: str) -> int:
        key = patient_name.lower().strip()
        if key not in self._stores:
            return 0
        return len(self._stores[key].index_to_docstore_id)
