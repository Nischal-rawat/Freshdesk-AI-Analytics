from pathlib import Path
import pandas as pd

from keyword_matcher import KeywordMatcher


class TicketClassifier:
    """
    Ticket Classification Engine

    Reads normalized ticket text and enriches every
    ticket with business intelligence.

    Output:
        output/master_dataset.xlsx
    """

    def __init__(self, df: pd.DataFrame):

        self.df = df.copy()

        self.matcher = KeywordMatcher()

    # -----------------------------------------------------

    def classify(self):

        print("\n" + "=" * 70)
        print("TICKET CLASSIFICATION")
        print("=" * 70)

        if "Combined Text" not in self.df.columns:
            raise ValueError(
                "Combined Text column not found. Run normalizer first."
            )

        # -------------------------------------------------
        # Create Output Columns
        # -------------------------------------------------

        text_columns = [
            "Product",
            "Category",
            "Subcategory",
            "Ticket Type",
            "Spam Classification",
            "Owner Team",
            "Business Priority",
            "Customer Impact",
            "Business Impact",
            "Matched Keywords",
        ]

        for column in text_columns:
            self.df[column] = ""

        # Confidence is numeric
        self.df["Confidence"] = 0

        # -------------------------------------------------
        # Classification
        # -------------------------------------------------

        total = len(self.df)

        for index, row in self.df.iterrows():

            result = self.matcher.match_ticket(
                row["Combined Text"]
            )

            self.df.at[index, "Product"] = result.get("Product", "")
            self.df.at[index, "Category"] = result.get("Category", "")
            self.df.at[index, "Subcategory"] = result.get("Subcategory", "")
            self.df.at[index, "Ticket Type"] = result.get("Ticket Type", "")
            self.df.at[index, "Spam Classification"] = result.get(
                "Spam Classification", ""
            )
            self.df.at[index, "Owner Team"] = result.get(
                "Owner Team", ""
            )
            self.df.at[index, "Business Priority"] = result.get(
                "Business Priority", ""
            )
            self.df.at[index, "Customer Impact"] = result.get(
                "Customer Impact", ""
            )
            self.df.at[index, "Business Impact"] = result.get(
                "Business Impact", ""
            )
            self.df.at[index, "Matched Keywords"] = result.get(
                "Matched Keywords", ""
            )

            # Always store confidence as integer
            confidence = result.get("Confidence", 0)

            try:
                confidence = int(confidence)
            except Exception:
                confidence = 0

            self.df.at[index, "Confidence"] = confidence

            if (index + 1) % 100 == 0:
                print(f"Processed {index + 1:,}/{total:,} tickets...")

        print("\n✓ Ticket classification completed")

        return self.df

    # -----------------------------------------------------

    def save_master_dataset(self):

        output_folder = Path("output")

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = output_folder / "master_dataset.xlsx"

        self.df.to_excel(
            output_file,
            index=False
        )

        print(f"\n✓ Saved : {output_file}")

    # -----------------------------------------------------

    def summary(self):

        print("\n" + "=" * 70)
        print("CLASSIFICATION SUMMARY")
        print("=" * 70)

        print(f"Tickets : {len(self.df):,}")

        print("\nProducts")
        print(
            self.df["Product"]
            .replace("", "Unknown")
            .value_counts()
            .head(10)
        )

        print("\nCategories")
        print(
            self.df["Category"]
            .replace("", "Unknown")
            .value_counts()
            .head(10)
        )

        print("\nTicket Types")
        print(
            self.df["Ticket Type"]
            .replace("", "Unknown")
            .value_counts()
            .head(10)
        )

        print("\nOwner Teams")
        print(
            self.df["Owner Team"]
            .replace("", "Unknown")
            .value_counts()
            .head(10)
        )

        print("\nAverage Confidence")

        print(
            round(
                pd.to_numeric(
                    self.df["Confidence"],
                    errors="coerce"
                ).fillna(0).mean(),
                2,
            )
        )