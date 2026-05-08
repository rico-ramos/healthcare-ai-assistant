from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"


@dataclass(frozen=True)
class Settings:
    """Centralized runtime configuration."""

    data_dir: Path = DEFAULT_DATA_DIR
    records_path: Path = DEFAULT_DATA_DIR / "records.csv"
    reports_dir: Path = DEFAULT_DATA_DIR / "patient_reports"
    openai_api_key: str | None = None
    llm_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-large"
    retriever_k: int = 4
    chunk_size: int = 800
    chunk_overlap: int = 160


def load_settings() -> Settings:
    """Load settings from .env / environment variables."""

    load_dotenv()
    data_dir = Path(os.getenv("DATA_DIR", str(DEFAULT_DATA_DIR))).resolve()
    return Settings(
        data_dir=data_dir,
        records_path=Path(os.getenv("RECORDS_PATH", str(data_dir / "records.csv"))).resolve(),
        reports_dir=Path(os.getenv("REPORTS_DIR", str(data_dir / "patient_reports"))).resolve(),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        llm_model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"),
        retriever_k=int(os.getenv("RETRIEVER_K", "4")),
        chunk_size=int(os.getenv("CHUNK_SIZE", "800")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "160")),
    )


def require_openai_key(settings: Settings) -> None:
    if not settings.openai_api_key or settings.openai_api_key.startswith("your_"):
        raise RuntimeError("OPENAI_API_KEY is not set. Copy .env.example to .env and add your key.")
