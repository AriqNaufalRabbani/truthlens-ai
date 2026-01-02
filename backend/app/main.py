from dotenv import load_dotenv
from pathlib import Path
import os

# 1️⃣ Load .env PALING AWAL
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# (opsional debug, boleh hapus nanti)
print("GROQ_API_KEY (main):", os.getenv("GROQ_API_KEY"))

# 2️⃣ BARU import FastAPI & router
from fastapi import FastAPI
from app.api import router

app = FastAPI(title="TruthLens AI Backend")
app.include_router(router)
