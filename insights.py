from pathlib import Path
import pandas as pd


class InsightsEngine:
    """
    Executive Insights Engine

    Converts analytics into
    actionable business insights.
    """

    def __init__(self, analytics):

        self.analytics = analytics

        self.summary = analytics.summary

        self.kpis = analytics.kpis

        self.insights = []

    # ---------------------------------------------------------

    def execute(self):

        print("\n" + "=" * 70)
        print("EXECUTIVE INSIGHTS")
        print("=" * 70)

        self.executive_summary()

        self.product_insights()

        self.category_insights()

        print(f"\n✓ Generated {len(self.insights)} insights")

        return self.insights

    # ---------------------------------------------------------

    def add_insight(

        self,

        category,

        priority,

        finding,

        recommendation,

        owner,

    ):

        self.insights.append(

            {

                "Category": category,

                "Priority": priority,

                "Finding": finding,

                "Recommendation": recommendation,

                "Owner": owner,

            }

        )

    # ---------------------------------------------------------

    def executive_summary(self):

        total = self.kpis.get(

            "Total Tickets",

            0,

        )

        avg = self.kpis.get(

            "Average Confidence",

            0,

        )

        self.add_insight(

            "Executive",

            "Info",

            f"{total:,} tickets analysed.",

            "Use this dashboard as the baseline for operational reviews.",

            "Management",

        )

        self.add_insight(

            "Executive",

            "Info",

            f"Average classification confidence is {avg:.2f}%",

            "Improve keyword rules for higher accuracy over time.",

            "Support Operations",

        )

    # ---------------------------------------------------------

    def product_insights(self):

        if "Products" not in self.summary:

            return

        products = self.summary["Products"]

        if len(products) == 0:

            return

        top = products.iloc[0]

        self.add_insight(

            "Product",

            "High",

            f"{top['Product']} generated the highest ticket volume ({int(top['Tickets'])} tickets).",

            "Prioritize recurring issues before the next product release.",

            "Product Team",

        )

    # ---------------------------------------------------------

    def category_insights(self):

        if "Categories" not in self.summary:

            return

        categories = self.summary["Categories"]

        if len(categories) == 0:

            return

        top = categories.iloc[0]

        recommendation = {

            "Authentication":
                "Review login flow, SSO configuration and failed login events.",

            "Billing":
                "Review invoicing workflow and payment communication.",

            "Product Bug":
                "Prioritize defect fixes before introducing new features.",

            "Performance":
                "Investigate slow endpoints and optimize performance.",

            "Enhancement":
                "Review feature requests during product planning.",

        }.get(

            top["Category"],

            "Review recurring customer issues.",

        )

        owner = {

            "Authentication": "Engineering",

            "Billing": "Finance",

            "Product Bug": "Engineering",

            "Performance": "Engineering",

            "Enhancement": "Product",

        }.get(

            top["Category"],

            "Support",

        )

        self.add_insight(

            "Support",

            "High",

            f"{top['Category']} is the largest support category ({int(top['Tickets'])} tickets).",

            recommendation,

            owner,

        )

    # ---------------------------------------------------------

    def customer_insights(self):

        if "Customers" not in self.summary:
            return

        customers = self.summary["Customers"]

        if len(customers) == 0:
            return

        top = customers.iloc[0]

        customer_name = str(top.iloc[0])

        tickets = int(top["Tickets"])

        self.add_insight(

            "Customer Success",

            "High",

            f"{customer_name} generated the highest support volume ({tickets} tickets).",

            "Review account health, adoption, onboarding quality and schedule a proactive customer success meeting.",

            "Customer Success",

        )

        high_volume = customers[customers["Tickets"] >= 20]

        if len(high_volume) > 1:

            self.add_insight(

                "Customer Success",

                "Medium",

                f"{len(high_volume)} customers generated more than 20 tickets.",

                "Review these accounts for adoption issues, renewal risk and recurring problems.",

                "Customer Success",

            )

    # ---------------------------------------------------------

    def engineering_insights(self):

        if "Owner Teams" not in self.summary:
            return

        teams = self.summary["Owner Teams"]

        engineering = teams[

            teams["Owner Team"]

            .str.contains(

                "Engineering",

                case=False,

                na=False

            )

        ]

        if len(engineering):

            tickets = int(engineering.iloc[0]["Tickets"])

            self.add_insight(

                "Engineering",

                "High",

                f"Engineering owns {tickets} classified tickets.",

                "Prioritize recurring defects and investigate root causes before the next release.",

                "Engineering",

            )

    # ---------------------------------------------------------

    def ai_insights(self):

        if "AI" not in self.summary:
            return

        ai = self.summary["AI"]

        if len(ai) == 0:
            return

        ai = ai.sort_values(

            "Tickets",

            ascending=False

        )

        top = ai.iloc[0]

        self.add_insight(

            "AI",

            "Medium",

            f"{top['AI Feature']} generated {int(top['Tickets'])} AI-related tickets.",

            "Review prompts, model responses and customer workflows related to this feature.",

            "AI Team",

        )

    # ---------------------------------------------------------

    def priority_insights(self):

        if "Priority" not in self.summary:
            return

        priority = self.summary["Priority"]

        p1 = priority[

            priority["Business Priority"] == "P1"

        ]

        if len(p1):

            count = int(p1.iloc[0]["Tickets"])

            self.add_insight(

                "Operations",

                "High",

                f"There are {count} P1 business priority tickets.",

                "Review open P1 tickets daily until resolved.",

                "Support Operations",

            )

    # ---------------------------------------------------------

    def operational_insights(self):

        total = self.kpis.get(

            "Total Tickets",

            0

        )

        operational = self.kpis.get(

            "Operational Tickets",

            0

        )

        if total == 0:
            return

        percentage = round(

            operational / total * 100,

            2

        )

        self.add_insight(

            "Operations",

            "Low",

            f"{percentage}% of all tickets are operational.",

            "Investigate automation opportunities for repetitive operational work.",

            "Support Operations",

        )

    # ---------------------------------------------------------

    def workload_insights(self):

        if "Owner Teams" not in self.summary:
            return

        teams = self.summary["Owner Teams"]

        if len(teams) == 0:
            return

        top = teams.iloc[0]

        self.add_insight(

            "Workload",

            "Medium",

            f"{top['Owner Team']} currently owns the highest workload ({int(top['Tickets'])} tickets).",

            "Review workload distribution and resource allocation.",

            "Support Management",

        )

    # ---------------------------------------------------------

    def save_excel(self):

        """
        Save insights to Excel.
        """

        output_folder = Path("output")

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = output_folder / "Executive_Insights.xlsx"

        insights_df = pd.DataFrame(self.insights)

        with pd.ExcelWriter(
            output_file,
            engine="openpyxl"
        ) as writer:

            insights_df.to_excel(
                writer,
                sheet_name="Executive Insights",
                index=False
            )

        print(f"\n✓ Executive Insights saved : {output_file}")

    # ---------------------------------------------------------

    def save_text(self):

        """
        Save insights to text report.
        """

        output_folder = Path("output")

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = output_folder / "Executive_Insights.txt"

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write("=" * 80 + "\n")
            f.write("EXECUTIVE INSIGHTS REPORT\n")
            f.write("=" * 80 + "\n\n")

            for i, insight in enumerate(self.insights, start=1):

                f.write(f"{i}. {insight['Category']}\n")
                f.write(f"Priority       : {insight['Priority']}\n")
                f.write(f"Finding        : {insight['Finding']}\n")
                f.write(f"Recommendation : {insight['Recommendation']}\n")
                f.write(f"Owner          : {insight['Owner']}\n")
                f.write("-" * 80 + "\n")

        print(f"✓ Executive text report saved : {output_file}")

    # ---------------------------------------------------------

    def print_report(self):

        """
        Print insights to console.
        """

        print("\n" + "=" * 80)
        print("EXECUTIVE INSIGHTS SUMMARY")
        print("=" * 80)

        for i, insight in enumerate(self.insights, start=1):

            print(f"\n{i}. [{insight['Priority']}] {insight['Category']}")

            print(f"Finding       : {insight['Finding']}")

            print(f"Recommendation: {insight['Recommendation']}")

            print(f"Owner         : {insight['Owner']}")

        print("\n" + "=" * 80)

        print(f"Total Insights Generated : {len(self.insights)}")

    # ---------------------------------------------------------

    def execute(self):

        """
        Execute complete insights pipeline.
        """

        print("\n" + "=" * 70)
        print("EXECUTIVE INSIGHTS ENGINE")
        print("=" * 70)

        self.executive_summary()

        self.product_insights()

        self.category_insights()

        self.customer_insights()

        self.engineering_insights()

        self.ai_insights()

        self.priority_insights()

        self.operational_insights()

        self.workload_insights()

        self.print_report()

        self.save_excel()

        self.save_text()

        print("\n✓ Insights Engine Completed")

        return pd.DataFrame(self.insights)