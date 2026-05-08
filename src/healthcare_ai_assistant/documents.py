from __future__ import annotations

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import Settings


def _patient_name_from_filename(path: Path) -> str:
    explicit = {
        "sample_patient": "Rebeca Nagle",
        "sample_report_anjali": "Anjali Mehra",
        "sample_report_david": "David Thompson",
        "sample_report_ramesh": "Ramesh Kulkarni",
    }
    stem = path.stem.lower()
    if stem in explicit:
        return explicit[stem]
    stem = stem.replace("sample_report_", "").replace("_", " ").replace("-", " ")
    return " ".join(part.capitalize() for part in stem.split())


def load_patient_documents(reports_dir: Path):
    if not reports_dir.exists():
        raise FileNotFoundError(f"Patient reports directory not found: {reports_dir}")
    paths = sorted(list(reports_dir.glob("*.pdf")) + list(reports_dir.glob("*.txt")) + list(reports_dir.glob("*.md")))
    if not paths:
        raise FileNotFoundError(f"No .pdf, .txt, or .md patient reports found in {reports_dir}")

    docs = []
    for path in paths:
        loader = PyPDFLoader(str(path)) if path.suffix.lower() == ".pdf" else TextLoader(str(path), encoding="utf-8")
        patient_docs = loader.load()
        patient_name = _patient_name_from_filename(path)
        for doc in patient_docs:
            doc.metadata["patient_name"] = patient_name
            doc.metadata["source_file"] = path.name
        docs.extend(patient_docs)
    return docs


def split_documents(docs, settings: Settings):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        add_start_index=True,
    )
    return splitter.split_documents(docs)


def build_vectorstore(settings: Settings):
    docs = load_patient_documents(settings.reports_dir)
    splits = split_documents(docs, settings)
    embeddings = OpenAIEmbeddings(model=settings.embedding_model, openai_api_key=settings.openai_api_key)
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore, embeddings, {"documents": len(docs), "chunks": len(splits)}


def build_retriever(settings: Settings):
    vectorstore, embeddings, stats = build_vectorstore(settings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": settings.retriever_k})
    return retriever, embeddings, stats
