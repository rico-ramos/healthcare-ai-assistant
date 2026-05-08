from pathlib import Path

from healthcare_ai_assistant.registry import PatientRegistry


def test_lookup_patient_by_partial_name():
    records_path = Path("data/records.csv")
    registry = PatientRegistry(records_path)

    result = registry.lookup_patient("Anjali")

    assert result["status"] == "found"
    assert result["name"] == "Anjali Mehra"