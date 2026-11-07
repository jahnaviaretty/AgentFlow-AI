import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

APP_TITLE = "AgentFlow AI"
APP_DESCRIPTION = "Autonomous Multi-Agent RAG & Workflow Automation Platform"

DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
DATABASE_DIR = BASE_DIR / "database"

DATABASE_PATH = DATABASE_DIR / "agentflow.db"

DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
DATABASE_DIR.mkdir(exist_ok=True)

SUPPORTED_FILE_TYPES = ["pdf"]
MAX_FILE_SIZE_MB = 10

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")