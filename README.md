\# AgentFlow AI 🤖



\### Autonomous Multi-Agent RAG \& Workflow Automation Platform



AgentFlow AI is a Python-based application that uses a multi-agent workflow to process user queries, retrieve relevant information from uploaded PDF documents, generate answers, and evaluate response relevance.



The project combines \*\*LangGraph, Retrieval-Augmented Generation (RAG), TF-IDF retrieval, Python, and Streamlit\*\* to demonstrate an intelligent document question-answering workflow.



\## 🚀 Features



\- \*\*PDF Document Upload:\*\* Upload PDF documents and extract their text.

\- \*\*Multi-Agent Workflow:\*\* Coordinate Planner, Researcher, Executor, and Evaluator agents using LangGraph.

\- \*\*Document Question Answering:\*\* Ask questions based on uploaded PDF content.

\- \*\*RAG Pipeline:\*\* Split document text into chunks and retrieve relevant context using TF-IDF similarity.

\- \*\*Answer Generation:\*\* Extract relevant information and prepare answers from retrieved document content.

\- \*\*Response Evaluation:\*\* Evaluate answer relevance using a scoring mechanism.

\- \*\*Workflow History:\*\* Store and review previous queries and responses using SQLite.

\- \*\*Interactive Interface:\*\* Use a Streamlit-based dashboard to interact with the application.



\## 🧠 System Architecture



The application follows a multi-stage workflow:



1\. \*\*Planner Agent\*\* – Analyzes the user query and creates an execution plan.

2\. \*\*Researcher Agent\*\* – Retrieves relevant information from uploaded documents.

3\. \*\*Executor Agent\*\* – Processes the retrieved context and generates an answer.

4\. \*\*Evaluator Agent\*\* – Evaluates the relevance of the generated response.

5\. \*\*Database\*\* – Stores uploaded document information and workflow history.



\### Workflow



User Query → Planner → Researcher → Executor → Evaluator → Final Answer



\## 🛠️ Technology Stack



| Category | Technologies |

|---|---|

| Programming Language | Python |

| Frontend | Streamlit |

| Agent Orchestration | LangGraph |

| RAG | TF-IDF, Scikit-learn |

| PDF Processing | PyPDF |

| Database | SQLite |

| Data Processing | Python |

| Environment Management | Python Virtual Environment |



\## 📂 Project Structure



```text

AgentFlow-AI/

│

├── agents/

│   ├── planner.py

│   ├── researcher.py

│   ├── executor.py

│   ├── evaluator.py

│   └── workflow.py

│

├── database/

│   └── db\_manager.py

│

├── evaluation/

│   └── metrics.py

│

├── rag/

│   ├── document\_loader.py

│   └── vector\_store.py

│

├── tools/

│   ├── api\_tools.py

│   └── python\_tools.py

│

├── utils/

│   └── logger.py

│

├── app.py

├── config.py

├── requirements.txt

└── README.md

```



\## ⚙️ Installation and Setup



\### 1. Clone the repository



```bash

git clone https://github.com/jahnaviaretty/AgentFlow-AI.git

```



\### 2. Navigate to the project directory



```bash

cd AgentFlow-AI

```



\### 3. Create a virtual environment



```bash

python -m venv .venv

```



\### 4. Activate the environment



\*\*Windows:\*\*



```bash

.venv\\Scripts\\activate

```



\### 5. Install dependencies



```bash

pip install -r requirements.txt

```



\### 6. Run the application



```bash

streamlit run app.py

```



The application will open in your browser.



\## 💡 How to Use



1\. Launch the Streamlit application.

2\. Upload a PDF document.

3\. Enter a question related to the uploaded document.

4\. Run the AgentFlow workflow.

5\. Review the generated plan, retrieved context, and answer.

6\. View the evaluation score and workflow history.



\## 🎯 Project Objective



The objective of AgentFlow AI is to explore how multiple specialized agents can work together to automate document-based question answering and information processing.



This project demonstrates practical implementation of agent orchestration, document processing, retrieval techniques, workflow automation, and response evaluation.



\## 👩‍💻 Author



\*\*Jahnavi Aretty\*\*



B.Tech – Computer Science and Engineering (Data Science)



GitHub: \[jahnaviaretty](https://github.com/jahnaviaretty)



\---



⭐ If you find this project interesting, consider giving it a star!s

\## 📸 Application Screenshots



\### Dashboard

!\[Dashboard](screenshots/dashboard.png)



\### PDF Upload

!\[PDF Upload](screenshots/pdf-upload.png)



\### Generated Answer

!\[Generated Answer](screenshots/answer.png)



\### Answer Evaluation

!\[Evaluation](screenshots/answer2.png)



\### Workflow History

!\[Workflow History](screenshots/workflow.png)



