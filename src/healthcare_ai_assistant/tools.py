from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from .registry import PatientRegistry
from .scheduling import book_appointment


class HealthcareTools:
    """Implementation layer used by LangGraph tool wrappers."""

    def __init__(self, registry: PatientRegistry, retriever, llm):
        self.registry = registry
        self.retriever = retriever
        self.llm = llm
        self.parser = StrOutputParser()

    def lookup_patient(self, key: str) -> dict:
        return self.registry.lookup_patient(key)

    def retrieve_medical_history(self, patient_name: str) -> dict:
        query = f"medical history diagnosis medications treatment plan for {patient_name}"
        docs = self.retriever.invoke(query)
        normalized_name = patient_name.lower().strip()
        relevant = [
            doc for doc in docs
            if doc.metadata.get("patient_name", "").lower().strip() == normalized_name
        ]
        if not relevant:
            return {
                "status": "not_found",
                "patient": patient_name,
                "summary": "No confidently matched clinical notes were found for this patient.",
            }
        context = "\n\n".join(doc.page_content for doc in relevant)
        prompt = ChatPromptTemplate.from_template(
            "You are a medical summarization assistant.\n"
            "Summarize the clinical notes for patient: {patient_name}\n"
            "Include: Diagnoses, Medications, Lab Results (if any), Vitals, Treatment Plan.\n\n"
            "Clinical Notes:\n{context}\n\nProvide a clear, structured clinical summary."
        )
        summary = (prompt | self.llm | self.parser).invoke({"patient_name": patient_name, "context": context})
        return {"status": "found", "patient": patient_name, "summary": summary}

    def book_appointment(self, patient_name: str, specialty: str, preference: str = "morning") -> dict:
        return book_appointment(patient_name, specialty, preference)

    def search_medical_info(self, topic: str) -> dict:
        docs = self.retriever.invoke(f"treatment guidelines diagnosis {topic}")
        context = "\n\n".join(doc.page_content for doc in docs)
        prompt = ChatPromptTemplate.from_template(
            "You are a clinical information assistant.\n"
            "Provide a concise summary for: {topic}\n"
            "Include: Overview, Key Treatments, Medications, Red Flags.\n\n"
            "Available context:\n{context}\n\n"
            "Use context where relevant; supplement with clinical knowledge. "
            "Respond in clear bullet points."
        )
        result = (prompt | self.llm | self.parser).invoke({"topic": topic, "context": context})
        return {"status": "found", "topic": topic, "information": result}

    def update_patient_summary(self, patient_name: str, new_summary: str) -> dict:
        return self.registry.update_patient_summary(patient_name, new_summary)
