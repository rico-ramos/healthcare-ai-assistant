from healthcare_ai_assistant.config import load_settings
from healthcare_ai_assistant.registry import PatientRegistry


def test_lookup_patient_by_partial_name():
    registry = PatientRegistry(load_settings().records_path)
    result = registry.lookup_patient("Anjali")
    assert result["status"] == "found"
    assert result["name"] == "Anjali Mehra"
