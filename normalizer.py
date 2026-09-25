import re
import pandas as pd


class TicketNormalizer:
    """
    Normalizes ticket text before classification.

    Creates:
        - Normalized Subject
        - Normalized Description
        - Combined Text
    """

    def __init__(self, df: pd.DataFrame):

        self.df = df.copy()

    # --------------------------------------------------

    def normalize(self):

        print("\n" + "=" * 70)
        print("TEXT NORMALIZATION")
        print("=" * 70)

        if "Subject" not in self.df.columns:
            raise ValueError("Column 'Subject' not found.")

        if "Description" not in self.df.columns:
            raise ValueError("Column 'Description' not found.")

        self.df["Normalized Subject"] = (
            self.df["Subject"]
            .fillna("")
            .apply(self.clean_text)
        )

        self.df["Normalized Description"] = (
            self.df["Description"]
            .fillna("")
            .apply(self.clean_text)
        )

        self.df["Combined Text"] = (
            self.df["Normalized Subject"]
            + " "
            + self.df["Normalized Description"]
        )

        print("✓ Subject normalized")

        print("✓ Description normalized")

        print("✓ Combined text generated")

        return self.df

    # --------------------------------------------------

    def clean_text(self, text):

        text = str(text)

        # lowercase
        text = text.lower()

        # remove html tags
        text = re.sub(r"<.*?>", " ", text)

        # remove urls
        text = re.sub(r"http\S+", " ", text)

        # remove email addresses
        text = re.sub(r"\S+@\S+", " ", text)

        # remove RE/FW
        text = re.sub(r"\bre:\b", " ", text)
        text = re.sub(r"\bfw:\b", " ", text)
        text = re.sub(r"\bfwd:\b", " ", text)

        # remove original message blocks
        text = re.sub(
            r"-----original message-----.*",
            " ",
            text,
            flags=re.DOTALL,
        )

        # remove punctuation
        text = re.sub(
            r"[^a-z0-9 ]",
            " ",
            text,
        )

        # remove extra spaces
        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()


# ------------------------------------------------------

if __name__ == "__main__":

    print("Run through app.py")