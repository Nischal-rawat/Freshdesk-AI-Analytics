"""
=========================================================
Support Intelligence Platform
Application Launcher
Version : 5.0
=========================================================
"""

import sys
from pathlib import Path

# =========================================================
# Project Paths
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# =========================================================
# Imports
# =========================================================

from classification import APP_NAME, VERSION
from pipeline import SupportIntelligencePipeline

try:
    from utils.file_picker import select_file
except Exception:
    select_file = None


# =========================================================
# Banner
# =========================================================

def banner():

    print("\n" + "=" * 80)
    print(APP_NAME)
    print(f"Version : {VERSION}")
    print("=" * 80)


# =========================================================
# File Selection
# =========================================================

def get_input_file():

    if select_file is None:
        return None

    try:

        print("\nOpening File Browser...")

        filepath = select_file()

        if filepath:

            print(f"\nSelected File:\n{filepath}")

            return filepath

    except Exception:

        pass

    print("\nNo file selected.")
    print("Using latest file from INPUT folder.")

    return None


# =========================================================
# Main
# =========================================================

def main():

    banner()

    filepath = get_input_file()

    pipeline = SupportIntelligencePipeline(filepath)

    pipeline.run()


# =========================================================
# Entry
# =========================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\nExecution cancelled by user.")

    except Exception as e:

        print("\nAPPLICATION FAILED")
        print("-" * 80)
        print(type(e).__name__)
        print(e)

        import traceback

        traceback.print_exc()