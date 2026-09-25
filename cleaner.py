from pathlib import Path
import pandas as pd


class DatasetCleaner:

    def __init__(self, df):
        self.df = df.copy()

        self.report = []

    def clean(self):

        print("\n" + "=" * 70)
        print("DATA CLEANING")
        print("=" * 70)

        self.remove_unnamed_columns()

        self.remove_empty_columns()

        self.trim_text_columns()

        self.standardize_status()

        self.standardize_priority()

        self.remove_duplicate_rows()

        self.save_clean_dataset()

        self.print_summary()

        return self.df

    # --------------------------------------------------------

    def remove_unnamed_columns(self):

        before = len(self.df.columns)

        self.df = self.df.loc[
            :,
            ~self.df.columns.str.startswith("Unnamed")
        ]

        removed = before - len(self.df.columns)

        self.report.append(
            ("Unnamed Columns Removed", removed)
        )

    # --------------------------------------------------------

    def remove_empty_columns(self):

        before = len(self.df.columns)

        self.df = self.df.dropna(axis=1, how="all")

        removed = before - len(self.df.columns)

        self.report.append(
            ("Empty Columns Removed", removed)
        )

    # --------------------------------------------------------

    def trim_text_columns(self):

        text_columns = self.df.select_dtypes(
            include="object"
        ).columns

        for column in text_columns:

            self.df[column] = (
                self.df[column]
                .astype(str)
                .str.strip()
            )

        self.report.append(
            ("Text Columns Trimmed", len(text_columns))
        )

    # --------------------------------------------------------

    def standardize_status(self):

        if "Status" not in self.df.columns:
            return

        self.df["Status"] = (
            self.df["Status"]
            .astype(str)
            .str.strip()
            .str.title()
        )

        self.report.append(
            ("Status Standardized", 1)
        )

    # --------------------------------------------------------

    def standardize_priority(self):

        if "Priority" not in self.df.columns:
            return

        self.df["Priority"] = (
            self.df["Priority"]
            .astype(str)
            .str.strip()
            .str.title()
        )

        self.report.append(
            ("Priority Standardized", 1)
        )

    # --------------------------------------------------------

    def remove_duplicate_rows(self):

        before = len(self.df)

        self.df = self.df.drop_duplicates()

        removed = before - len(self.df)

        self.report.append(
            ("Duplicate Rows Removed", removed)
        )

    # --------------------------------------------------------

    def save_clean_dataset(self):

        output = Path("output/cleaned")

        output.mkdir(
            parents=True,
            exist_ok=True
        )

        filename = output / "cleaned_freshdesk.xlsx"

        self.df.to_excel(
            filename,
            index=False
        )

        self.report.append(
            ("Clean Dataset Saved", filename)
        )

    # --------------------------------------------------------

    def print_summary(self):

        print("\nCleaning Summary")
        print("-" * 50)

        for item in self.report:

            print(f"{item[0]:30} : {item[1]}")

        print("\nFinal Dataset")

        print(f"Rows    : {len(self.df):,}")

        print(f"Columns : {len(self.df.columns)}")