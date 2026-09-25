"""
=========================================================
Support Intelligence Platform
Configuration
Version : 5.0
=========================================================
"""

from pathlib import Path

# =========================================================
# APPLICATION
# =========================================================

APP_NAME = "Support Intelligence Platform"
VERSION = "5.0"

# =========================================================
# FEATURE FLAGS
# =========================================================

# Legacy keyword matcher (False)
# New modular classification engine (True)
USE_V2_CLASSIFIER = False

# Future enhancements
USE_ML_CLASSIFIER = False
USE_V2_HEALTH_SCORE = False
USE_SMART_RECOMMENDATIONS = False
USE_EXPLAINABLE_AI = False

# =========================================================
# PROJECT PATHS
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent

SRC_DIR = ROOT_DIR / "src"
INPUT_DIR = ROOT_DIR / "input"
OUTPUT_DIR = ROOT_DIR / "output"
RULES_DIR = ROOT_DIR / "rules"
LOG_DIR = ROOT_DIR / "logs"
ASSETS_DIR = ROOT_DIR / "assets"

# =========================================================
# OUTPUT FILES
# =========================================================

MASTER_DATASET = OUTPUT_DIR / "master_dataset.xlsx"
DASHBOARD_FILE = OUTPUT_DIR / "Support_Intelligence_Dashboard.xlsx"

# =========================================================
# SETTINGS
# =========================================================

CONFIDENCE_THRESHOLD = 0.50
AUTO_SAVE = True
MAX_UNKNOWN_PERCENT = 0.10

# =========================================================
# CREATE REQUIRED FOLDERS
# =========================================================

REQUIRED_FOLDERS = [
    INPUT_DIR,
    OUTPUT_DIR,
    RULES_DIR,
    LOG_DIR,
    ASSETS_DIR,
]

for folder in REQUIRED_FOLDERS:
    try:
        folder.mkdir(parents=True, exist_ok=True)
    except (OSError, PermissionError):
        pass
