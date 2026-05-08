# 🏥 Agentic AI Healthcare Assistant

An AI-powered healthcare assistant built using LangGraph that performs multi-step reasoning, retrieves patient data, and generates structured responses through tool-based workflows.

This project demonstrates how modern LLM-based systems can move beyond simple chat interactions into **stateful, tool-augmented agents** capable of handling real-world workflows.

---

## 📌 Project Overview

This assistant simulates a healthcare support system that can:

- Retrieve patient records from a registry
- Analyze symptoms and provide structured responses
- Maintain conversational state across interactions
- Dynamically invoke tools based on user intent

The system is designed using an **agentic architecture**, where decisions are made step-by-step using a state machine powered by LangGraph.

---

## 🧠 Architecture & Flow

**Core Flow:**

1. User submits a query (symptoms, patient lookup, etc.)
2. Agent processes input and determines next step
3. Tools are invoked as needed:
   - Patient lookup
   - Document retrieval (RAG)
   - Scheduling logic
4. State is updated across steps
5. Final response is generated and returned

---

## ⚙️ Tech Stack

- **LLM / Agent Framework:** LangGraph, LangChain
- **Model:** OpenAI (Chat-based LLM)
- **Vector Store:** FAISS
- **Frontend:** :contentReference[oaicite:0]{index=0}
- **Language:** Python

---

## 🔑 Key Features

- Stateful agent workflow using LangGraph
- Tool-based reasoning and execution
- Retrieval-Augmented Generation (RAG)
- Patient memory across sessions
- Interactive UI for real-time querying
- Runtime performance tracking

---

## 📊 Performance & Observability

The system includes built-in runtime metrics to evaluate performance and behavior:

- ⏱️ Average latency per query
- 🔧 Tool invocation tracking (per query + total session)
- 🧮 Token usage monitoring
- ✅ Response completion tracking
- 🧠 Patient detection validation

These metrics are displayed directly in the UI to support debugging and system optimization.

---

## 🖥️ Demo

![Chat UI](chat.png)
![Conversation](conversation.png)
![Patient Snapshot](patient_snapshot.png)
![Metrics](metrics.png)

---

## 🧪 Testing

Basic unit tests are included to validate core functionality.

Run tests:

```bash
PYTHONPATH=src python -m pytest tests/
```

## 🛠️ Installation & Setup

1. Clone the repository

   ```bash
   git clone https://github.com/rico-ramos/healthcare-ai-assistant.git
   cd healthcare-ai-assistant
   ```

2. Create virtual environment

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables

   Create a .env file:

   ```bash
   cp .env.example .env
   ```

   Add your OpenAI key to `.env`:

   ```bash
   OPENAI_API_KEY=your_api_key_here
   ```

## ▶️ Running the App

    ```bash
    PYTHONPATH=src streamlit run app.py
    ```

## Project structure

```text
healthcare_ai_assistant_clean/
├── app.py                          # Streamlit UI
├── data/
│   ├── records.csv
│   └── patient_reports/
├── notebooks/
│   └── Capstone_Healthcare_Assistant_RAMOS_original.ipynb
├── scripts/
│   └── smoke_test.py               # OpenAI-free sanity check
├── src/healthcare_ai_assistant/
│   ├── config.py
│   ├── registry.py
│   ├── documents.py
│   ├── scheduling.py
│   ├── tools.py
│   ├── graph.py
│   ├── memory.py
│   ├── runner.py
│   └── cli.py
│
├── tests/
│   └── test_registry.py            # Unit test(s) for registry logic
│
├── .env.example
├── requirements.txt
└── README.md
```

## 🚧 Future Improvements

- Expand evaluation framework for response accuracy
- Add multi-patient conversational context handling
- Improve UI with agent reasoning visualization
- Integrate structured medical knowledge base

## 💡 Why This Project Matters

This project demonstrates practical implementation of:

- Agent-based system design
- LLM + tool integration
- Real-world workflow automation using AI

It reflects a shift from simple prompt-based systems to **composable, stateful AI architectures.**

## Setup

```bash
python3 -m venv .venv
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
6. Add retrieval quality metrics: `top_k_hit_rate` and cost per query.

## Demo

![Chat UI](chat.png)
![Conversation](conversation.png)
![Patient Snapshot](patient_snapshot.png)
![Metrics](metrics.png)
