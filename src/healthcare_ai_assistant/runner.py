from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from .config import Settings, require_openai_key
from .documents import build_retriever
from .graph import build_medical_agent
from .memory import PatientMemory
from .registry import PatientRegistry
from .tools import HealthcareTools


def _collect_token_usage(messages: list) -> dict:
    input_tokens = 0
    output_tokens = 0
    total_tokens = 0

    for message in messages:
        usage = getattr(message, "usage_metadata", None) or {}
        input_tokens += usage.get("input_tokens", 0) or 0
        output_tokens += usage.get("output_tokens", 0) or 0
        total_tokens += usage.get("total_tokens", 0) or 0

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
    }


@dataclass
class AssistantRuntime:
    agent: object
    registry: PatientRegistry
    memory: PatientMemory
    stats: dict
    last_run_metrics: dict = field(default_factory=dict)

    def run(self, query: str, verbose: bool = False) -> str:
        started_at = time.perf_counter()

        final_state = self.agent.invoke(
            {
                "messages": [HumanMessage(content=query)],
                "query": query,
                "patient_name": None,
                "tool_results": [],
                "final_response": None,
            },
            config={"recursion_limit": 15},
        )

        latency_seconds = time.perf_counter() - started_at
        messages = final_state.get("messages", [])
        response = final_state.get("final_response") or ""
        patient = final_state.get("patient_name") or ""
        tool_results = final_state.get("tool_results", [])

        tool_call_count = sum(
            len(getattr(message, "tool_calls", []) or [])
            for message in messages
        )

        token_usage = _collect_token_usage(messages)

        self.last_run_metrics = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "query": query,
            "latency_seconds": round(latency_seconds, 2),
            "tool_call_count": tool_call_count,
            "tool_result_count": len(tool_results),
            "patient_detected": patient or "None",
            "response_chars": len(response),
            "completed": bool(response.strip()),
            **token_usage,
        }

        patient_key = patient.lower().strip()
        if patient_key and patient_key not in {"unknown", "none"}:
            self.memory.save(patient, query, response)

        if verbose:
            print(response)
            print("METRICS:", self.last_run_metrics)

        return response


def create_runtime(settings: Settings) -> AssistantRuntime:
    require_openai_key(settings)
    registry = PatientRegistry(settings.records_path)
    retriever, embeddings, stats = build_retriever(settings)
    llm = ChatOpenAI(model=settings.llm_model, temperature=0, openai_api_key=settings.openai_api_key)
    healthcare_tools = HealthcareTools(registry=registry, retriever=retriever, llm=llm)
    agent = build_medical_agent(healthcare_tools=healthcare_tools, model_name=settings.llm_model)
    memory = PatientMemory(embeddings)
    return AssistantRuntime(agent=agent, registry=registry, memory=memory, stats=stats)