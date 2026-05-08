from __future__ import annotations

import json
import operator
from typing import Annotated, List, Optional, TypedDict

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from .tools import HealthcareTools

SYSTEM_PROMPT = """You are a clinical AI assistant for a healthcare platform. You help staff retrieve patient records, review medical histories, schedule appointments, search treatment guidelines, and update patient summaries.

Guidelines:
- Call lookup_patient_tool first when given a partial or unverified name.
- Use the full name returned by lookup_patient_tool for all subsequent patient tools.
- Never fabricate clinical data. If a tool returns no result, say so clearly.
- Respond in a clear, professional tone appropriate for clinical staff.
- When booking appointments, confirm specialty and timing if the query is ambiguous.
- This project is educational and should not replace clinician judgment."""


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    query: str
    patient_name: Optional[str]
    tool_results: Annotated[list, operator.add]
    final_response: Optional[str]


def build_medical_agent(healthcare_tools: HealthcareTools, model_name: str):
    @tool
    def lookup_patient_tool(name: str) -> dict:
        """Look up basic patient demographic information by name."""
        return healthcare_tools.lookup_patient(name)

    @tool
    def medical_history_tool(patient_name: str) -> dict:
        """Retrieve clinical summaries and history from patient records."""
        return healthcare_tools.retrieve_medical_history(patient_name)

    @tool
    def book_appointment_tool(patient_name: str, specialty: str, preference: str = "morning") -> dict:
        """Schedule a new appointment for a patient with a given specialty and time preference."""
        return healthcare_tools.book_appointment(patient_name, specialty, preference)

    @tool
    def medical_info_search_tool(topic: str) -> dict:
        """Search medical information for general guidelines and treatment information."""
        return healthcare_tools.search_medical_info(topic)

    @tool
    def update_summary_tool(patient_name: str, new_summary: str) -> dict:
        """Update the clinical summary for a patient in the registry."""
        return healthcare_tools.update_patient_summary(patient_name, new_summary)

    tools = [lookup_patient_tool, medical_history_tool, book_appointment_tool, medical_info_search_tool, update_summary_tool]
    tool_node = ToolNode(tools)
    model = ChatOpenAI(model=model_name, temperature=0).bind_tools(tools)

    def agent_node(state: AgentState) -> dict:
        messages = state["messages"]
        if not any(isinstance(message, SystemMessage) for message in messages):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        response = model.invoke(messages)
        return {"messages": [response]}

    synthesis_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a clinical documentation assistant. Compose a single, clear, professional response for clinical staff from the conversation below.\n\nRules:\n- Synthesize all tool results into one coherent reply\n- Present medical history in readable clinical format\n- Confirm appointment details explicitly if one was booked\n- Present treatment guidance as labelled bullet points\n- If a tool returned an error or no data, state that plainly\n- Include a brief educational-use note when giving general medical guidance"),
        ("human", "Original query: {query}\n\nConversation:\n{messages}"),
    ])

    def synthesize_node(state: AgentState) -> dict:
        message_log = "\n".join(f"[{type(m).__name__}] {getattr(m, 'content', '')}" for m in state["messages"])
        chain = synthesis_prompt | ChatOpenAI(model=model_name, temperature=0)
        response = chain.invoke({"query": state.get("query", ""), "messages": message_log})
        return {"final_response": response.content}

    def route_after_agent(state: AgentState) -> str:
        last_message = state["messages"][-1]
        return "tools" if getattr(last_message, "tool_calls", None) else "synthesize"

    def capture_patient_node(state: AgentState) -> dict:
        if not state.get("messages"):
            return {}
        raw_content = getattr(state["messages"][-1], "content", "")
        data = None
        if isinstance(raw_content, str):
            try:
                data = json.loads(raw_content)
            except Exception:
                return {}
        elif isinstance(raw_content, dict):
            data = raw_content
        if not isinstance(data, dict):
            return {}
        candidate = data.get("name") or data.get("patient")
        if isinstance(candidate, str) and candidate.strip():
            return {"patient_name": candidate.strip(), "tool_results": [data]}
        return {"tool_results": [data]}

    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.add_node("capture_patient", capture_patient_node)
    graph.add_node("synthesize", synthesize_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", route_after_agent, {"tools": "tools", "synthesize": "synthesize"})
    graph.add_edge("tools", "capture_patient")
    graph.add_edge("capture_patient", "agent")
    graph.add_edge("synthesize", END)
    return graph.compile()
