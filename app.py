
import sys
import json
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from config import APP_TITLE, APP_DESCRIPTION, UPLOAD_DIR
from database.db_manager import (
    initialize_database,
    save_document,
    save_workflow,
    get_workflow_history
)
from agents.workflow import build_workflow


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_database()


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0B1020, #111A32);
    color: #F4F5FF;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #10172B;
    border-right: 1px solid #283451;
}

[data-testid="stSidebar"] * {
    color: #E5E9F5;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

h1, h2, h3 {
    color: #F5F3FF !important;
}

p, label, li {
    color: #C7D0E5;
}

.hero {
    padding: 28px;
    border-radius: 20px;
    background: linear-gradient(120deg, #29205A, #172B50);
    border: 1px solid #51438A;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 34px;
    font-weight: 800;
    color: white;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 15px;
    color: #D2D0F4;
}

.metric-card {
    background: #18233B;
    border: 1px solid #30405F;
    border-radius: 16px;
    padding: 20px;
    min-height: 115px;
}

.metric-label {
    color: #AAB8D4;
    font-size: 13px;
}

.metric-value {
    color: #FFFFFF;
    font-size: 29px;
    font-weight: 800;
    margin-top: 7px;
}

.agent-card {
    background: #18233B;
    border: 1px solid #30405F;
    border-radius: 14px;
    padding: 17px;
    min-height: 115px;
}

.agent-name {
    color: white;
    font-size: 16px;
    font-weight: 700;
}

.agent-description {
    color: #AAB8D4;
    font-size: 12px;
}

.stButton > button {
    background: linear-gradient(100deg, #7655E8, #4778E8);
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 11px 22px;
    font-weight: 700;
    transition: 0.2s;
}

.stButton > button:hover {
    border: 1px solid #B8A7FF;
    box-shadow: 0 4px 18px #7655E855;
}

.stTextArea textarea {
    background: #18233B !important;
    color: #FFFFFF !important;
    border: 1px solid #6555A8 !important;
    border-radius: 12px !important;
    caret-color: white;
}

.stTextArea textarea::placeholder {
    color: #AAB8D4 !important;
    opacity: 1;
}

[data-testid="stFileUploader"] {
    background: #18233B;
    border: 1px dashed #7663D9;
    border-radius: 14px;
    padding: 15px;
}

[data-testid="stFileUploader"] section {
    background: transparent;
}

[data-testid="stExpander"] {
    background: #18233B;
    border: 1px solid #30405F;
    border-radius: 12px;
}

[data-testid="stMetric"] {
    background: #18233B;
    border: 1px solid #30405F;
    border-radius: 12px;
    padding: 15px;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: #18233B;
    border-color: #30405F !important;
    border-radius: 16px;
}

hr {
    border-color: #30405F;
}

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #7655E8, #4778E8);
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# WORKFLOW
# --------------------------------------------------

@st.cache_resource
def load_workflow():
    return build_workflow()


workflow = load_workflow()


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

PAGES = [
    "🏠 Dashboard",
    "💬 Ask Questions",
    "📚 Workflow History",
    "ℹ️ About"
]


def open_questions_page():
    st.session_state["navigation"] = "💬 Ask Questions"


if "navigation" not in st.session_state:
    st.session_state["navigation"] = "🏠 Dashboard"


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("# 🤖 AgentFlow")
    st.caption("AI-powered document workspace")

    st.divider()

    page = st.radio(
        "WORKSPACE",
        PAGES,
        key="navigation",
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### 🟢 System Status")
    st.caption("Application: Online")
    st.caption("Workflow: Ready")
    st.caption("Database: Connected")

    st.divider()

    st.caption("Powered by Python · Streamlit · LangGraph")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "🏠 Dashboard":

    history = get_workflow_history(limit=50)

    st.markdown("""
    <div class="hero">
        <div class="hero-title">Welcome to AgentFlow AI ✨</div>
        <div class="hero-subtitle">
            Your intelligent document assistant.
            Upload PDFs, ask questions and explore information
            through a multi-agent workflow.
        </div>
    </div>
    """, unsafe_allow_html=True)

    completed = sum(
        1 for item in history
        if item["status"] == "Completed"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Workflows</div>
            <div class="metric-value">{len(history)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">AI Agents</div>
            <div class="metric-value">04</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Completed Workflows</div>
            <div class="metric-value">{completed}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.subheader("⚡ Your AI Team")
    st.caption("Four specialized agents working together.")

    agents = [
        ("📋", "Planner Agent", "Creates a step-by-step task plan."),
        ("🔍", "Research Agent", "Retrieves relevant PDF information."),
        ("🧠", "Execution Agent", "Extracts answers and performs tasks."),
        ("📊", "Evaluator Agent", "Evaluates response relevance.")
    ]

    cols = st.columns(4)

    for col, agent in zip(cols, agents):
        with col:
            st.markdown(f"""
            <div class="agent-card">
                <div style="font-size:25px">{agent[0]}</div>
                <div class="agent-name">{agent[1]}</div>
                <div class="agent-description">{agent[2]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.subheader("🚀 Get Started")

    with st.container(border=True):
        st.subheader("Turn your documents into answers")
        st.write(
            "Upload a PDF document, enter your question, "
            "and let AgentFlow process it through its AI workflow."
        )

        st.button(
            "💬 Start Asking Questions",
            type="primary",
            on_click=open_questions_page
        )

    if history:
        st.write("")
        st.subheader("🕘 Recent Activity")

        for item in history[:3]:
            st.write(
                f"**Workflow #{item['id']}** — "
                f"{item['user_query']}"
            )
            st.caption(
                f"{item['status']} · {item['created_at']}"
            )


# --------------------------------------------------
# ASK QUESTIONS
# --------------------------------------------------

elif page == "💬 Ask Questions":

    st.title("💬 Ask Your Documents")
    st.caption(
        "Upload your PDF and ask questions in natural language."
    )

    st.write("")

    with st.container(border=True):

        st.subheader("📄 Upload Your Document")

        uploaded_file = st.file_uploader(
            "Choose a PDF document",
            type=["pdf"],
            max_upload_size=10,
            help="Maximum supported file size: 10 MB"
        )

        document_path = ""

        if uploaded_file is not None:

            if uploaded_file.size > 10 * 1024 * 1024:
                st.error("File size must not exceed 10 MB.")

            else:
                safe_filename = Path(uploaded_file.name).name
                document_path = str(UPLOAD_DIR / safe_filename)

                with open(document_path, "wb") as file:
                    file.write(uploaded_file.getbuffer())

                st.success(
                    f"Document ready: {safe_filename}"
                )

    st.write("")

    with st.container(border=True):

        st.subheader("✨ What would you like to know?")

        query = st.text_area(
            "Your question",
            placeholder="Example: What certifications are listed in my resume?",
            height=130,
            label_visibility="collapsed"
        )

        run_button = st.button(
            "🚀 Run AgentFlow",
            type="primary",
            use_container_width=True
        )

    if run_button:

        if not query.strip():
            st.warning("Please enter a question.")

        elif not uploaded_file:
            st.warning("Please upload a PDF document.")

        elif uploaded_file.size > 10 * 1024 * 1024:
            st.warning("Please upload a PDF smaller than 10 MB.")

        else:

            try:

                with st.spinner(
                    "🤖 Your AI agents are processing the document..."
                ):

                    save_document(Path(document_path).name)

                    initial_state = {
                        "query": query.strip(),
                        "document_path": document_path,
                        "plan": [],
                        "retrieved_context": [],
                        "result": "",
                        "evaluation": {}
                    }

                    final_state = workflow.invoke(initial_state)

                    history_id = save_workflow(
                        query.strip(),
                        final_state["result"],
                        "Completed",
                        final_state["evaluation"]
                    )

                st.success("AgentFlow completed successfully!")

                st.write("")
                st.subheader("💡 AgentFlow Answer")

                with st.container(border=True):
                    st.write(final_state["result"])

                st.write("")
                st.subheader("📊 Response Evaluation")

                evaluation = final_state["evaluation"]
                score = evaluation.get("score", 0)

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Relevance Score", f"{score}%")
                    st.progress(
                        max(0, min(score, 100)) / 100
                    )

                with col2:
                    st.metric(
                        "Evaluation Status",
                        evaluation.get("status", "Not available")
                    )
                    st.caption(evaluation.get("feedback", ""))

                with st.expander("📋 View Generated Plan"):
                    for number, step in enumerate(
                        final_state["plan"], start=1
                    ):
                        st.write(f"{number}. {step}")

                with st.expander("🔍 View Retrieved Document Context"):

                    if final_state["retrieved_context"]:

                        for number, item in enumerate(
                            final_state["retrieved_context"], start=1
                        ):
                            st.markdown(f"**Retrieved Chunk {number}**")
                            st.write(item["chunk"])
                            st.caption(
                                f"Similarity score: {item['score']}"
                            )

                    else:
                        st.info("No document context was retrieved.")

                st.caption(
                    f"Saved successfully · Workflow ID: {history_id}"
                )

            except Exception as error:
                st.error(f"Workflow failed: {error}")


# --------------------------------------------------
# WORKFLOW HISTORY
# --------------------------------------------------

elif page == "📚 Workflow History":

    st.title("📚 Workflow History")
    st.caption("Explore your previous AgentFlow sessions.")

    history = get_workflow_history(limit=50)

    if history:

        st.markdown(f"**{len(history)} workflows found**")

        for item in history:

            evaluation = None

            if item.get("evaluation"):
                try:
                    evaluation = json.loads(item["evaluation"])
                except (json.JSONDecodeError, TypeError):
                    evaluation = None

            score = (
                evaluation.get("score")
                if isinstance(evaluation, dict)
                else None
            )

            title_text = (
                f"Workflow #{item['id']} · {item['status']}"
            )

            if score is not None:
                title_text += f" · {score}%"

            with st.expander(title_text):

                st.markdown("**💬 Question**")
                st.write(item["user_query"])

                st.markdown("**💡 AgentFlow Answer**")
                st.write(
                    item["agent_response"] or "No answer saved."
                )

                if evaluation:

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("Relevance Score", f"{score}%")

                    with col2:
                        st.metric(
                            "Status",
                            evaluation.get("status", "Not available")
                        )

                    st.write("**Feedback**")
                    st.write(
                        evaluation.get("feedback", "Not available")
                    )

                else:
                    st.info(
                        "Evaluation details are unavailable "
                        "for this older workflow."
                    )

                st.caption(f"Created at: {item['created_at']}")

    else:
        st.info("No workflow history available yet.")


# --------------------------------------------------
# ABOUT
# --------------------------------------------------

elif page == "ℹ️ About":

    st.title("ℹ️ About AgentFlow AI")

    st.markdown("""
    <div class="hero">
        <div class="hero-title">AgentFlow AI 🤖</div>
        <div class="hero-subtitle">
            Autonomous Multi-Agent RAG & Workflow Automation Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("About the Project")

    st.write(
        "AgentFlow AI is a document question-answering and "
        "workflow application built with Python, Streamlit "
        "and LangGraph."
    )

    st.subheader("Core Technologies")

    technologies = [
        "Python",
        "Streamlit",
        "LangGraph",
        "SQLite",
        "Scikit-learn",
        "TF-IDF Retrieval",
        "PyPDF"
    ]

    cols = st.columns(3)

    for index, technology in enumerate(technologies):
        with cols[index % 3]:
            st.markdown(f"""
            <div class="agent-card">
                <div class="agent-name">✦ {technology}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.subheader("The Four Agents")

    st.markdown("""
    - **Planner:** Creates the task plan.
    - **Researcher:** Loads PDFs and retrieves relevant text.
    - **Executor:** Generates extractive answers.
    - **Evaluator:** Estimates response relevance.
    """)

    st.caption(
        "Built with Python, Streamlit, LangGraph and SQLite."
    )
