from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REGULATIONS_DIR = DATA_DIR / "regulations"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
CHROMA_DIR = ARTIFACTS_DIR / "chroma_db"
MODEL_BUNDLE_PATH = ARTIFACTS_DIR / "model_bundle.joblib"
METRICS_PATH = ARTIFACTS_DIR / "metrics.json"

HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct:cerebras")

RISK_THRESHOLDS = {
    "approve": 0.20,
    "review": 0.50,
}
