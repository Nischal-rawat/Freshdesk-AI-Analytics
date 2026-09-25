"""
=========================================================
Support Intelligence Platform
Freshdesk Loader
Version : 5.0
=========================================================
"""

from pathlib import Path
import pandas as pd

try:
    from classification import INPUT_DIR
except ImportError:
    INPUT_DIR = Path("input")


class FreshdeskLoader:
    """
    Freshdesk Dataset Loader

    Features
    --------
    • Supports Excel (.xlsx/.xls)
    • Supports CSV
    • Auto-detects newest file
    • Supports user-selected file
    • Cleans dataset
    • Prints dataset summary
    """

    def __init__(self, filepath=None):

        self.filepath = Path(filepath) if filepath else None

        self.raw_folder = INPUT_DIR

        self.supported_extensions = [
            ".xlsx",
            ".xls",
            ".csv"
        ]

    # =====================================================
    # Find Latest File
    # =====================================================

    def find_latest_file(self):

        files = []

        for extension in self.supported_extensions:

            files.extend(
                self.raw_folder.glob(f"*{extension}")
            )

        if not files:

            raise FileNotFoundError(

                f"No Excel/CSV file found in\n{self.raw_folder}"

            )

        return max(

            files,

            key=lambda x: x.stat().st_mtime

        )

    # =====================================================
    # Load Dataset
    # =====================================================

    def load(self):

        if self.filepath:

            file = self.filepath

        else:

            file = self.find_latest_file()

        print("\n" + "=" * 70)
        print("FRESHDESK DATASET LOADER")
        print("=" * 70)
        print(f"Source File : {file.name}")

        suffix = file.suffix.lower()

        if suffix in [".xlsx", ".xls"]:

            return self.load_excel(file)

        elif suffix == ".csv":

            return self.load_csv(file)

        else:

            raise ValueError(

                f"Unsupported file type : {suffix}"

            )

    # =====================================================
    # Excel Loader
    # =====================================================

    def load_excel(self, file):

        workbook = pd.read_csv

        print("\nAvailable Worksheets")

        for sheet in workbook.sheet_names:

            print(f"   • {sheet}")

        preferred = [

            "Raw data cleaned",

            "Raw Data Cleaned",

            "Raw Data",

            "Tickets",

            "Sheet1"

        ]

        selected = None

        for sheet in preferred:

            if sheet in workbook.sheet_names:

                selected = sheet

                break

        if selected is None:

            selected = workbook.sheet_names[0]

        print(f"\nReading Worksheet : {selected}")

        df = pd.read_csv(

            file,

            sheet_name=selected

        )

        return self.post_process(df)

    # =====================================================
    # CSV Loader
    # =====================================================

    def load_csv(self, file):

        try:

            df = pd.read_csv(

                file,

                encoding="utf-8"

            )

        except UnicodeDecodeError:

            df = pd.read_csv(

                file,

                encoding="latin1"

            )

        return self.post_process(df)

    # =====================================================
    # Cleanup
    # =====================================================

    def post_process(self, df):

        df.columns = (

            df.columns

            .astype(str)

            .str.strip()

        )

        df.dropna(

            how="all",

            inplace=True

        )

        df.reset_index(

            drop=True,

            inplace=True

        )

        print("\nDataset Summary")
        print("-" * 50)
        print(f"Rows            : {len(df):,}")
        print(f"Columns         : {len(df.columns)}")
        print(
            f"Memory Usage    : {round(df.memory_usage(deep=True).sum()/1024/1024,2)} MB"
        )

        print("\nColumns Detected")

        for col in df.columns:

            print(f"   • {col}")

        return df

    # =====================================================
    # Preview
    # =====================================================

    def preview(self, rows=5):

        df = self.load()

        print("\nPreview")
        print("-" * 50)

        print(df.head(rows))

        return df