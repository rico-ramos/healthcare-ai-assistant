from healthcare_ai_assistant.config import load_settings
from healthcare_ai_assistant.registry import PatientRegistry
from healthcare_ai_assistant.scheduling import book_appointment

settings = load_settings()
registry = PatientRegistry(settings.records_path)
print(registry.lookup_patient("Anjali"))
print(book_appointment("Anjali Mehra", "pulmonology"))
print("Smoke test complete. OpenAI-dependent RAG/agent tests require OPENAI_API_KEY.")
