import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build base path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ollama Settings
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-oss:20b-cloud")
INTENT_MODEL_NAME = os.environ.get("INTENT_MODEL_NAME", "llama3.2:3b")

# File Paths
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "vector_store")
HF_CACHE_DIR = os.path.join(BASE_DIR, "hf_cache")
KEYWORDS_FILE = os.path.join(BASE_DIR, "src", "config_data", "keywords.json")

# Application Settings
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
STREAM_RESPONSES = os.environ.get("STREAM_RESPONSES", "True").lower() == "true"
