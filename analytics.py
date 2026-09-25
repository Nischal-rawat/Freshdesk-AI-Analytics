from pathlib import Path
from typing import Dict

import pandas as pd


class AnalyticsEngine:
    """
    Analytics Engine

    Calculates all business metrics from the classified
    master dataset.

    This class DOES NOT
    -------------------
    - Generate charts
    - Format Excel
    - Create PowerPoint

    It ONLY creates summary tables.
    """

    def __init__(self, df: pd.DataFrame):

        self.df = df.copy()

        self.summary: Dict[str, pd.DataFrame] = {}

        self.kpis = {}

        self.prepare_dataset()

    # ---------------------------------------------------------

    def prepare_dataset(self):

        """
        Prepare dataframe for analytics.
        """

        if "Confidence" in self.df.columns:

            self.df["Confidence"] = pd.to_numeric(
                self.df["Confidence"],
                errors="coerce"
            ).fillna(0)

        # Replace blanks for grouping

        object_columns = self.df.select_dtypes(
            include="object"
        ).columns

        for column in object_columns:

            self.df[column] = (

                self.df[column]

                .fillna("Unknown")

                .replace("", "Unknown")

            )

    # ---------------------------------------------------------

    def run(self):

        print("\n" + "=" * 70)
        print("ANALYTICS ENGINE")
        print("=" * 70)

        self.executive_kpis()

        self.product_summary()

        self.category_summary()

        self.ticket_type_summary()

        self.priority_summary()

        self.owner_team_summary()

        self.status_summary()

        self.customer_summary()

        self.ai_summary()

        self.pareto_summary()

        self.monthly_summary()

        print("\n✓ Analytics Completed")

        return self.summary

    # ---------------------------------------------------------

    def executive_kpis(self):

        total = len(self.df)

        customer = len(

            self.df[

                self.df["Ticket Type"] != "Operational"

            ]

        )

        operational = len(

            self.df[

                self.df["Ticket Type"] == "Operational"

            ]

        )

        open_tickets = self.count_status("Open")

        pending = self.count_status("Pending")

        resolved = self.count_status("Resolved")

        closed = self.count_status("Closed")

        avg_confidence = round(

            self.df["Confidence"].mean(),

            2

        )

        products = (

            self.df["Product"]

            .replace("Unknown", pd.NA)

            .dropna()

            .nunique()

        )

        categories = (

            self.df["Category"]

            .replace("Unknown", pd.NA)

            .dropna()

            .nunique()

        )

        self.kpis = {

            "Total Tickets": total,

            "Customer Tickets": customer,

            "Operational Tickets": operational,

            "Open Tickets": open_tickets,

            "Pending Tickets": pending,

            "Resolved Tickets": resolved,

            "Closed Tickets": closed,

            "Average Confidence": avg_confidence,

            "Products Covered": products,

            "Categories Covered": categories,

        }

        self.summary["Executive KPIs"] = pd.DataFrame(

            {

                "KPI": self.kpis.keys(),

                "Value": self.kpis.values(),

            }

        )

    # ---------------------------------------------------------

    def count_status(self, status):

        if "Status" not in self.df.columns:

            return 0

        return len(

            self.df[

                self.df["Status"]

                .astype(str)

                .str.lower()

                == status.lower()

            ]

        )

    # ---------------------------------------------------------

    def percentage_table(self, column):

        summary = (

            self.df

            .groupby(column)

            .size()

            .reset_index(name="Tickets")

        )

        summary["Percent"] = (

            summary["Tickets"]

            / summary["Tickets"].sum()

            * 100

        ).round(2)

        summary = summary.sort_values(

            "Tickets",

            ascending=False

        )

        return summary.reset_index(drop=True)

    # ---------------------------------------------------------

    def product_summary(self):

        if "Product" not in self.df.columns:
            return

        summary = self.percentage_table("Product")

        if "Confidence" in self.df.columns:

            confidence = (

                self.df

                .groupby("Product")["Confidence"]

                .mean()

                .round(2)

                .reset_index(name="Average Confidence")

            )

            summary = summary.merge(

                confidence,

                on="Product",

                how="left"

            )

        self.summary["Products"] = summary

    # ---------------------------------------------------------

    def category_summary(self):

        if "Category" not in self.df.columns:
            return

        summary = self.percentage_table("Category")

        if "Confidence" in self.df.columns:

            confidence = (

                self.df

                .groupby("Category")["Confidence"]

                .mean()

                .round(2)

                .reset_index(name="Average Confidence")

            )

            summary = summary.merge(

                confidence,

                on="Category",

                how="left"

            )

        self.summary["Categories"] = summary

    # ---------------------------------------------------------

    def ticket_type_summary(self):

        if "Ticket Type" not in self.df.columns:
            return

        summary = self.percentage_table("Ticket Type")

        self.summary["Ticket Types"] = summary

    # ---------------------------------------------------------

    def priority_summary(self):

        if "Business Priority" not in self.df.columns:
            return

        summary = self.percentage_table(

            "Business Priority"

        )

        self.summary["Priority"] = summary

    # ---------------------------------------------------------

    def owner_team_summary(self):

        if "Owner Team" not in self.df.columns:
            return

        summary = self.percentage_table(

            "Owner Team"

        )

        self.summary["Owner Teams"] = summary

    # ---------------------------------------------------------

    def status_summary(self):

        if "Status" not in self.df.columns:
            return

        summary = self.percentage_table(

            "Status"

        )

        self.summary["Status"] = summary

    # ---------------------------------------------------------

    def customer_summary(self):

        possible_columns = [

            "Institution",

            "University",

            "Company",

            "Organization",

            "Requester Company",

            "Company Name",

            "Requester",

        ]

        customer_column = None

        for column in possible_columns:

            if column in self.df.columns:

                customer_column = column

                break

        if customer_column is None:

            return

        summary = (

            self.df

            .groupby(customer_column)

            .agg(

                Tickets=("Ticket ID", "count"),

                Average_Confidence=(

                    "Confidence",

                    "mean",

                ),

            )

            .reset_index()

        )

        summary["Average_Confidence"] = (

            summary["Average_Confidence"]

            .round(2)

        )

        summary = summary.sort_values(

            "Tickets",

            ascending=False

        )

        self.summary["Customers"] = summary

    # ---------------------------------------------------------

    def print_summary(self):

        print("\n")

        print("=" * 70)

        print("EXECUTIVE SUMMARY")

        print("=" * 70)

        for key, value in self.kpis.items():

            print(f"{key:<30} {value}")

        print("\nTop Products")

        if "Products" in self.summary:

            print(

                self.summary["Products"]

                .head(10)

            )

        print("\nTop Categories")

        if "Categories" in self.summary:

            print(

                self.summary["Categories"]

                .head(10)

            )

        print("\nTop Customers")

        if "Customers" in self.summary:

            print(

                self.summary["Customers"]

                .head(10)

            )
                # ---------------------------------------------------------

    def ai_summary(self):
        """
        AI Feature Breakdown
        """

        if "Product" not in self.df.columns:
            return

        ai_products = [
            "AI Studio",
            "Ask AI",
            "Rewrite with AI",
            "Citation Checker",
            "Grammar Checker",
            "Plagiarism Checker",
            "Paraphraser",
        ]

        ai_summary = []

        for product in ai_products:

            count = self.df[
                self.df["Product"]
                .astype(str)
                .str.contains(product, case=False, na=False)
            ].shape[0]

            ai_summary.append(
                {
                    "AI Feature": product,
                    "Tickets": count,
                }
            )

        self.summary["AI"] = pd.DataFrame(ai_summary)

    # ---------------------------------------------------------

    def pareto_summary(self):
        """
        Pareto analysis based on Category
        """

        if "Category" not in self.df.columns:
            return

        pareto = (
            self.df.groupby("Category")
            .size()
            .reset_index(name="Tickets")
            .sort_values("Tickets", ascending=False)
        )

        pareto["Percent"] = (
            pareto["Tickets"] / pareto["Tickets"].sum() * 100
        ).round(2)

        pareto["Cumulative %"] = (
            pareto["Percent"].cumsum()
        ).round(2)

        self.summary["Pareto"] = pareto

    # ---------------------------------------------------------

    def monthly_summary(self):
        """
        Monthly Ticket Trend
        """

        possible_columns = [
            "Created At",
            "Created at",
            "Created Date",
            "Created Time",
            "Created",
        ]

        date_column = None

        for column in possible_columns:

            if column in self.df.columns:

                date_column = column

                break

        if date_column is None:

            return

        dates = pd.to_datetime(
            self.df[date_column],
            errors="coerce"
        )

        monthly = (
            dates.dt.to_period("M")
            .value_counts()
            .sort_index()
            .reset_index()
        )

        monthly.columns = [
            "Month",
            "Tickets",
        ]

        monthly["Growth %"] = (
            monthly["Tickets"]
            .pct_change()
            .fillna(0)
            * 100
        ).round(2)

        self.summary["Monthly Trend"] = monthly

    # ---------------------------------------------------------

    def save(self):
        """
        Save all summary tables into one workbook.
        """

        output_folder = Path("output")

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
            output_folder /
            "Executive_Dashboard.xlsx"
        )

        with pd.ExcelWriter(
            output_file,
            engine="openpyxl"
        ) as writer:

            for sheet, dataframe in self.summary.items():

                dataframe.to_excel(
                    writer,
                    sheet_name=sheet[:31],
                    index=False
                )

        print("\n✓ Executive Dashboard Saved")

        print(output_file)

    # ---------------------------------------------------------

    def execute(self):
        """
        Complete Analytics Pipeline
        """

        self.run()

        self.print_summary()

        self.save()

        return self.summary