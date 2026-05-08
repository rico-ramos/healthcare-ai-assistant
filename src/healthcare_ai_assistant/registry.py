from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


class PatientRegistry:
    """Patient lookup and in-memory summary updates backed by a CSV/XLSX file."""

    def __init__(self, records_path: Path):
        self.records_path = records_path
        self.df = self._load_dataframe(records_path)
        self.registry = self._build_registry(self.df)

    @staticmethod
    def _load_dataframe(records_path: Path) -> pd.DataFrame:
        if not records_path.exists():
            raise FileNotFoundError(f"Patient records file not found: {records_path}")
        if records_path.suffix.lower() in {".xlsx", ".xls"}:
            return pd.read_excel(records_path)
        return pd.read_csv(records_path)

    @staticmethod
    def _build_registry(df: pd.DataFrame) -> dict[str, dict[str, Any]]:
        registry: dict[str, dict[str, Any]] = {}
        for row in df.to_dict(orient="records"):
            name = row.get("Name")
            phone = row.get("Phone_number")
            if isinstance(name, str) and name.strip():
                registry[name.lower().strip()] = row
            if pd.notna(phone):
                registry[str(phone).lower().strip()] = row
        return registry

    def names(self) -> list[str]:
        names: list[str] = []
        for row in self.df.to_dict(orient="records"):
            name = row.get("Name")
            if isinstance(name, str) and name not in names:
                names.append(name)
        return names

    def lookup_patient(self, key: str) -> dict:
        key = key.lower().strip()
        matches: list[tuple[int, dict[str, Any]]] = []
        for registry_key, patient in self.registry.items():
            score = 0
            if key == registry_key:
                score = 100
            elif key in registry_key:
                score = 80
            elif registry_key in key:
                score = 70
            if score > 0:
                if registry_key.startswith(key):
                    score += 10
                score -= min(abs(len(registry_key) - len(key)), 20)
                matches.append((score, patient))
        matches.sort(key=lambda item: item[0], reverse=True)

        seen_names: set[str] = set()
        for _, patient in matches:
            name = patient.get("Name")
            if not name or name in seen_names:
                continue
            seen_names.add(name)
            return {
                "status": "found",
                "name": patient.get("Name"),
                "age": patient.get("Age"),
                "gender": patient.get("Gender"),
                "phone": str(patient.get("Phone_number")),
                "address": patient.get("Address"),
                "summary": patient.get("Summary"),
                "note": "Best match selected based on fuzzy search score",
            }
        return {"status": "not_found", "matches": []}

    def update_patient_summary(self, patient_name: str, new_summary: str) -> dict:
        key = patient_name.lower().strip()
        if key not in self.registry:
            return {"status": "not_found", "message": f"Patient {patient_name} not found."}
        self.registry[key]["Summary"] = new_summary
        return {"status": "updated", "patient": patient_name}
