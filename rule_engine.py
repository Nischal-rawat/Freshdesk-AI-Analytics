from pathlib import Path
import pandas as pd


class RuleEngine:

    def __init__(self, df):

        self.df = df.copy()

        self.config_path = Path("config")

        self.products = pd.read_csv(self.config_path / "products.csv")
        self.categories = pd.read_csv(self.config_path / "issue_categories.csv")
        self.ticket_types = pd.read_csv(self.config_path / "ticket_types.csv")
        self.spam = pd.read_csv(self.config_path / "spam_keywords.csv")

    def classify(self):

        # Create output columns
        self.df["Product"] = ""
        self.df["Category"] = ""
        self.df["Subcategory"] = ""
        self.df["Ticket Type"] = ""
        self.df["Spam Classification"] = ""

        for index, row in self.df.iterrows():

            text = (
                str(row.get("Subject", "")) + " " +
                str(row.get("Description", ""))
            ).lower()

            self.df.at[index, "Product"] = self.lookup_product(text)
            self.df.at[index, "Category"] = self.lookup_category(text)
            self.df.at[index, "Subcategory"] = self.lookup_subcategory(text)
            self.df.at[index, "Ticket Type"] = self.lookup_ticket_type(text)
            self.df.at[index, "Spam Classification"] = self.lookup_spam(text)

        return self.df

    def lookup_product(self, text):

        for _, row in self.products.iterrows():
            if row["Keyword"].lower() in text:
                return row["Product"]

        return "Unknown"

    def lookup_category(self, text):

        for _, row in self.categories.iterrows():
            if row["Keyword"].lower() in text:
                return row["Category"]

        return "Other"

    def lookup_subcategory(self, text):

        for _, row in self.categories.iterrows():
            if row["Keyword"].lower() in text:
                return row["Subcategory"]

        return "Other"

    def lookup_ticket_type(self, text):

        for _, row in self.ticket_types.iterrows():
            if row["Keyword"].lower() in text:
                return row["Ticket Type"]

        return "Support"

    def lookup_spam(self, text):

        for _, row in self.spam.iterrows():
            if row["Keyword"].lower() in text:
                return row["Classification"]

        return "Customer"