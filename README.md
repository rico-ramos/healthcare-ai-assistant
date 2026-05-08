# Healthcare AI Assistant

An advanced AI-powered assistant for healthcare staff, featuring patient lookup, medical-history retrieval, appointment booking, and clinical guideline summarization—all built with a modular, production-ready architecture using LangGraph.

## What this project does

This assistant supports a staff-facing healthcare workflow:

- Patient lookup by name or phone
- Medical-history retrieval from patient report files
- LangGraph tool orchestration
- Appointment booking with specialty matching
- General treatment-guideline summarization
- In-memory patient session recall
- Streamlit UI for local interaction

> Educational prototype only. It is not medical advice and should not replace clinician judgment.

## Project structure

```text
healthcare_ai_assistant_clean/
├── app.py                          # Streamlit UI
├── data/
│   ├── records.csv                  # Patient registry data
│   └── patient_reports/             # Patient report source files
├── notebooks/
│   └── Capstone_Healthcare_Assistant_RAMOS_original.ipynb
├── scripts/
│   └── smoke_test.py                # OpenAI-free sanity check
├── src/healthcare_ai_assistant/
│   ├── config.py                    # Settings / environment variables
│   ├── registry.py                  # Patient lookup + summary update
│   ├── documents.py                 # Document loading, chunking, FAISS retrieval
│   ├── scheduling.py                # Appointment booking logic
│   ├── tools.py                     # Tool implementation layer
│   ├── graph.py                     # LangGraph state machine and tool wrappers
│   ├── memory.py                    # Per-patient session memory
│   ├── runner.py                    # Runtime factory and run() method
│   └── cli.py                       # Optional CLI entry point
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your OpenAI key to `.env`:

```bash
OPENAI_API_KEY=your_key_here
```

## Run the UI

```bash
PYTHONPATH=src streamlit run app.py
```

## Run from the command line

```bash
PYTHONPATH=src python -m healthcare_ai_assistant.cli "What is Anjali Mehra's diagnosis and treatment plan?"
```

## Run a smoke test without OpenAI

```bash
PYTHONPATH=src python scripts/smoke_test.py
```

This verifies patient lookup and appointment-booking logic without calling the LLM or embeddings API.

## Baseline preserved from notebook

The conversion keeps the core notebook logic intact:

- `lookup_patient`
- `retrieve_medical_history`
- `book_appointment`
- `search_medical_info`
- `update_patient_summary`
- LangGraph agent/tool loop
- Patient capture after tool execution
- Final synthesis response
- Patient session memory
- Streamlit UI

## Recommended next improvements

These are intentionally not forced into the baseline conversion:

1. Add an evaluation harness with 25-100 clinical workflow test prompts.
2. Persist FAISS indexes to disk instead of rebuilding them on startup.
3. Replace in-memory summary updates with a real database write layer.
4. Add structured output schemas for appointment and patient summary tools.
5. Add unit tests around graph routing and patient-name capture.
6. Add retrieval quality metrics: `top_k_hit_rate`, average latency, and cost per query.
