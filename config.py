import os
from dotenv import load_dotenv

load_dotenv()


APP_NAME = os.getenv("APP_NAME", "BrandForge AI")
APP_VERSION = os.getenv("APP_VERSION", "3.0.0")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4").strip()
OPENAI_BASE_URL = os.getenv(
    "OPENAI_BASE_URL",
    "https://api.openai.com/v1",
).rstrip("/")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "").strip()
TAVILY_BASE_URL = os.getenv(
    "TAVILY_BASE_URL",
    "https://api.tavily.com",
).rstrip("/")

OPENAI_IMAGE_MODEL = os.getenv(
    "OPENAI_IMAGE_MODEL",
    "gpt-image-1",
).strip()

ENABLE_IMAGE_GENERATION = (
    os.getenv("ENABLE_IMAGE_GENERATION", "true").lower()
    in {"1", "true", "yes", "on"}
)

FRONTEND_ORIGINS = [
    item.strip()
    for item in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if item.strip()
]


def ai_enabled() -> bool:
    return bool(OPENAI_API_KEY)


def research_enabled() -> bool:
    return bool(TAVILY_API_KEY)
