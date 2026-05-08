from __future__ import annotations

import random
from datetime import datetime, timedelta

DOCTOR_DB = {
    "general": [{"name": "Dr. Priya Sharma", "hospital": "City Health Clinic"}],
    "nephrology": [{"name": "Dr. Anand Mehta", "hospital": "Apollo Hospital"}],
    "endocrinology": [{"name": "Dr. Sunita Rao", "hospital": "Fortis Hospital"}],
    "cardiology": [{"name": "Dr. Vikram Nair", "hospital": "Max Hospital"}],
    "pulmonology": [{"name": "Dr. Kavita Joshi", "hospital": "Columbia Asia"}],
    "family medicine": [{"name": "Dr. Megana Lanoi", "hospital": "Bridport Family Medicine"}],
}

SPEC_MAP = {
    "nephrologist": "nephrology", "kidney": "nephrology", "renal": "nephrology",
    "diabetologist": "endocrinology", "diabetes": "endocrinology", "endocrinologist": "endocrinology",
    "cardiologist": "cardiology", "heart": "cardiology",
    "pulmonologist": "pulmonology", "lung": "pulmonology",
    "family": "family medicine", "primary care": "family medicine",
}


def book_appointment(patient_name: str, specialty: str, preference: str = "morning") -> dict:
    spec_key = specialty.lower().strip()
    resolved_spec = spec_key
    for keyword, mapping in SPEC_MAP.items():
        if keyword in spec_key:
            resolved_spec = mapping
            break
    match = DOCTOR_DB.get(resolved_spec)
    if not match:
        for key in DOCTOR_DB:
            if key in spec_key or spec_key in key:
                match = DOCTOR_DB[key]
                resolved_spec = key
                break
    if not match:
        match = DOCTOR_DB["general"]
        resolved_spec = "general"
    doctor = random.choice(match)
    date_obj = datetime.now() + timedelta(days=random.randint(2, 5))
    time_str = "10:30 AM" if "morning" in preference.lower() else "3:00 PM"
    return {
        "status": "confirmed",
        "booking_ref": f"APT-{random.randint(10000, 99999)}",
        "patient": patient_name,
        "doctor": doctor["name"],
        "hospital": doctor["hospital"],
        "specialty": resolved_spec,
        "date": date_obj.strftime("%A, %d %B %Y"),
        "time": time_str,
    }
