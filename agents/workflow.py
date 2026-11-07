
import sys
from pathlib import Path
from typing import TypedDict

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from langgraph.graph import StateGraph, START, END

from agents.planner import PlannerAgent
from agents.executor import ExecutionAgent
from agents.evaluator import EvaluatorAgent

from rag.document_loader import DocumentLoader
from rag.vector_store import VectorStore
from tools.python_tools import PythonTools
from utils.logger import get_logger

from database.db_manager import (
    initialize_database,
    save_document,
    save_workflow
)

logger = get_logger("AgentWorkflow")


class AgentState(TypedDict):
    query: str
    document_path: str
    plan: list
    retrieved_context: list
    result: str
    evaluation: dict


def planner_node(state):
    logger.info("Planner Agent started.")

    planner = PlannerAgent()
    plan = planner.create_plan(state["query"])

    return {"plan": plan["steps"]}


def detect_section(query):
    """Identify the resume section requested by the user."""

    query = query.lower()

    if "skill" in query or "technical" in query:
        return "skills"

    if "project" in query:
        return "projects"

    if "education" in query or "degree" in query:
        return "education"

    if "internship" in query or "experience" in query:
        return "experience"

    if "certif" in query:
        return "certificates"

    if "objective" in query or "summary" in query:
        return "objective"

    return None


def researcher_node(state):
    logger.info("Research Agent started.")

    document_path = state["document_path"]

    if not document_path:
        return {"retrieved_context": []}

    loader = DocumentLoader()
    text = loader.load_pdf(document_path)

    if not text.strip():
        return {"retrieved_context": []}

    requested_section = detect_section(state["query"])

    if requested_section:
        logger.info(
            "Section-aware retrieval selected: %s",
            requested_section
        )

        return {
            "retrieved_context": [
                {
                    "chunk": text,
                    "score": 1.0
                }
            ]
        }

    chunks = loader.split_text(
        text,
        chunk_size=100,
        overlap=20
    )

    if not chunks:
        return {"retrieved_context": []}

    store = VectorStore()
    store.add_documents(chunks)

    results = store.search(
        state["query"],
        top_k=3
    )

    return {"retrieved_context": results}


def execution_node(state):
    logger.info("Execution Agent started.")

    executor = ExecutionAgent()
    context = state["retrieved_context"]

    if context:
        result = executor.answer_from_context(
            state["query"],
            context
        )
    else:
        tool = PythonTools()
        analysis = tool.analyze_text(state["query"])

        result = (
            "No relevant information was retrieved from the PDF.\n"
            f"Query word count: {analysis['word_count']}\n"
            f"Unique words: {analysis['unique_words']}"
        )

    return {"result": result}


def evaluation_node(state):
    logger.info("Evaluator Agent started.")

    evaluator = EvaluatorAgent()

    evaluation = evaluator.evaluate(
        state["query"],
        state["result"]
    )

    return {"evaluation": evaluation}


def build_workflow():
    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("executor", execution_node)
    workflow.add_node("evaluator", evaluation_node)

    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "executor")
    workflow.add_edge("executor", "evaluator")
    workflow.add_edge("evaluator", END)

    return workflow.compile()


if __name__ == "__main__":

    initialize_database()

    app = build_workflow()

    print("\nAGENTFLOW AI - MULTI-AGENT RAG WORKFLOW")
    print("-" * 45)

    query = input("\nEnter your question: ").strip()

    if not query:
        print("Please enter a valid question.")
        sys.exit(1)

    document_path = input(
        "Enter PDF file path (or press Enter to skip): "
    ).strip().strip('"')

    if document_path and not Path(document_path).is_file():
        print("PDF file not found. Please check the file path.")
        sys.exit(1)

    if document_path:
        save_document(Path(document_path).name)

    initial_state = {
        "query": query,
        "document_path": document_path,
        "plan": [],
        "retrieved_context": [],
        "result": "",
        "evaluation": {}
    }

    final_state = app.invoke(initial_state)

    print("\nGenerated Plan:")

    for number, step in enumerate(final_state["plan"], start=1):
        print(f"{number}. {step}")

    print("\nRetrieved Context:")
    print(final_state["retrieved_context"])

    print("\nExecution Result:")
    print(final_state["result"])

    print("\nEvaluation:")
    print(final_state["evaluation"])

    history_id = save_workflow(
        query,
        final_state["result"],
        "Completed"
    )

    print("\nWorkflow completed successfully!")
    print("Workflow saved to database. ID:", history_id)
