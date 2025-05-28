# 📊 Agentic BI for Data Analysis using Generative AI

Agentic BI is a conversational business intelligence system that allows users to interact with their data using plain English. Powered by LLMs and AI agents, it automates SQL generation, chart creation, and insight summarization.

## 🚀 Project Goals
- Let users upload datasets (CSV)
- Ask natural language questions about the data
- Automatically generate:
  - SQL queries
  - Visualizations (bar, line, pie charts)
  - AI-generated insights
- Save useful insights and dashboards

## 🏗️ System Architecture
```plaintext
User Interface (Streamlit)
        ↓
LangChain Agent Orchestrator
        ↓
 ┌──────────────┬───────────────┐
 │ SQL Agent    │ Chart Agent   │
 │ Insight Agent│ (Plotly)      │
 └──────────────┴───────────────┘
        ↓
  Local SQLite / CSV Data

🛠️ Tech Stack
Frontend: Streamlit

Backend: Python, LangChain

LLM: Mistral / Phi-2 (Ollama / Hugging Face)

Charts: Plotly, Matplotlib

Data: CSV / SQLite

Deployment: Streamlit Cloud / Docker

📁 Project Structure
agentic_bi_project/
├── app/
│   ├── agents/
│   ├── ui/
│   ├── utils/
├── data/
├── tests/
├── main.py
├── requirements.txt
└── README.md

📬 Contact
Built by Prudhvi Marpina — exploring the intersection of Data Analysis and GenAI.