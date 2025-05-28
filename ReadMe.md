# 📊 Agentic BI: Conversational Data Analysis with Generative AI

## ✨ Unleash Your Data with Natural Language

Agentic BI is an innovative conversational business intelligence system that empowers users to interact with their data effortlessly using plain English. Built with the power of Large Language Models (LLMs) and specialized AI agents, it streamlines the entire data analysis workflow by automating SQL generation, chart creation, and insightful summarization.

Say goodbye to complex SQL queries and manual chart building. Just ask, and Agentic BI delivers the answers and visualizations you need to make informed decisions.

## 🚀 Key Features

* **Effortless Data Uploads**: Easily upload your datasets in CSV format.
* **Natural Language Querying**: Ask questions about your data using everyday English, just like you're talking to a data analyst.
* **Automated SQL Generation**: The system intelligently converts your natural language questions into precise SQL queries, ready for execution.
* **Dynamic Visualizations**: Automatically generates relevant charts (bar, line, pie) using Plotly based on your query results, providing interactive data exploration.
* **AI-Powered Insights**: Get clear, simple explanations of your data's key trends, comparisons, and outliers, tailored for non-technical audiences.
* **Save & Organize**: Save useful insights and dashboards for future reference and dashboard creation.

## 🏗️ System Architecture

The Agentic BI system leverages a modular architecture orchestrated by LangChain, connecting the user interface to specialized AI agents.

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

* User Interface (Streamlit): Provides an intuitive web interface for uploading data and interacting with the system.
* LangChain Agent Orchestrator: The core intelligence that directs user queries to the appropriate specialized agents.
* SQL Agent: Responsible for translating natural language questions into executable SQL queries against the loaded data.
* Chart Agent: Generates Plotly Express code snippets to visualize the SQL query results.
* Insight Agent: Interprets the query results and charts, providing human-readable insights and explanations.
* Local SQLite / CSV Data: Data is processed either in-memory (for CSVs) or using a local SQLite database, allowing for flexible data handling.

🛠️ Tech Stack
- Frontend: Streamlit
- Backend: Python, LangChain
- LLM: Mistral / Phi-2 (via Ollama / Hugging Face)
- Charts: Plotly, Matplotlib
- Data: CSV / SQLite
- Deployment: Streamlit Cloud / Docker

🚀 Getting Started
Follow these steps to set up and run Agentic BI on your local machine.

Prerequisites
Python 3.9+
Git
Docker (Optional, for running Ollama)
1. Clone the Repository
First, clone the project from GitHub:
git clone [https://github.com/https://github.com/prudhvi-marpina/agentic_bi_project.git](https://github.com/https://github.com/prudhvi-marpina/agentic_bi_project/agentic_bi_project.git)
cd agentic_bi_project

2. Set up Virtual Environment & Install Dependencies
It's highly recommended to use a virtual environment to manage dependencies:

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt

3. Set up your LLM (Ollama)
This project uses Ollama to run local LLMs (Mistral/Phi-2).

  1. Download and Install Ollama: Follow the instructions on the Ollama website to install it for your operating system.
  2. Pull the Mistral Model: Once Ollama is installed and running, open your terminal and pull the mistral model:
    ollama pull mistral

4. Run the Streamlit Application
With your virtual environment activated and Ollama running, you can now launch the Agentic BI application:
    streamlit run main.py

👨‍💻 How to Use
  1. Upload Your Data: On the left sidebar, click the "📁 Upload your CSV file" button and select your dataset.
  2. Ask a Question: Once your data is loaded, type your natural language question into the "Type your question here" text box.
  3. Explore Insights: The system will automatically generate the SQL query, execute it, display the results, create a relevant chart, and provide an AI-generated insight summary.
  4. Save Queries: Use the "💾 Save this query" button to store your successful queries and insights for later reference.
  5. Review History: See your "Previous Questions" and their corresponding SQL and insights.

📁 Project Structure

agentic_bi_project/
├── app/
│   ├── agents/          # Contains the SQL, Chart, and Insight AI agents
│   ├── ui/              # (Placeholder for UI specific components, if any are factored out)
│   ├── utils/           # Utility functions, including the agent runner
├── data/                # Directory for sample data or uploaded data (if not ignored)
├── saved_queries/       # Directory where saved queries and insights are stored
├── tests/               # Unit and integration tests
├── main.py              # The main Streamlit application file
├── requirements.txt     # List of Python dependencies
└── README.md            # This README file

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

📄 License
This project is open-source. Please add a license (e.g., MIT, Apache 2.0) to your repository.

📬 Contact
Built by Prudhvi Marpina — exploring the intersection of Data Analysis and Generative AI.