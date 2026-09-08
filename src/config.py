"""Configuration manager for OpsPulse AI."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RUNBOOKS_DIR = DATA_DIR / "runbooks"

class AppConfig:
    """Application configuration and SLA thresholds."""
    APP_NAME: str = os.getenv("APP_NAME", "OpsPulse AI")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() in ("true", "1", "yes")

    # SLA Thresholds (Target MTTR in minutes)
    SLA_THRESHOLDS = {
        "P1 - Critical": int(os.getenv("SLA_P1_CRITICAL_MINUTES", "30")),
        "P2 - High": int(os.getenv("SLA_P2_HIGH_MINUTES", "120")),
        "P3 - Medium": int(os.getenv("SLA_P3_MEDIUM_MINUTES", "480")),
        "P4 - Low": int(os.getenv("SLA_P4_LOW_MINUTES", "1440")),
    }

    # API Keys (Loaded safely from environment; never hardcoded)
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")

    # AI Model Settings
    DEFAULT_AI_MODEL: str = os.getenv("DEFAULT_AI_MODEL", "gpt-4o-mini")

    # ML Model Settings & Anomaly Contamination
    DEFAULT_ANOMALY_CONTAMINATION: float = float(os.getenv("DEFAULT_ANOMALY_CONTAMINATION", "0.08"))
    MIN_ANOMALY_CONTAMINATION: float = float(os.getenv("MIN_ANOMALY_CONTAMINATION", "0.01"))
    MAX_ANOMALY_CONTAMINATION: float = float(os.getenv("MAX_ANOMALY_CONTAMINATION", "0.25"))
    current_contamination: float = DEFAULT_ANOMALY_CONTAMINATION

    def set_anomaly_contamination(self, value: float) -> None:
        """Update the active Isolation Forest contamination parameter at runtime."""
        clamped = max(self.MIN_ANOMALY_CONTAMINATION, min(self.MAX_ANOMALY_CONTAMINATION, float(value)))
        self.current_contamination = round(clamped, 3)

    # Paths
    SAMPLE_DATA_PATH = DATA_DIR / "sample_incidents.csv"
    RUNBOOKS_PATH = RUNBOOKS_DIR

config = AppConfig()

