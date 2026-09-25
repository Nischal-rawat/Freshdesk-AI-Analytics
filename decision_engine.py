from pathlib import Path
import pandas as pd


class DecisionEngine:
    """
    Decision Intelligence Engine

    Converts all analytical outputs into
    executive business decisions.

    Outputs

        Decision_Report.xlsx
        Executive_Brief.txt
        Daily_Action_List.xlsx
    """

    def __init__(

        self,

        analytics,

        insights,

        recommendations,

        health,

        renewal,

        voc

    ):

        self.analytics = analytics

        self.insights = insights

        self.recommendations = recommendations

        self.health = health

        self.renewal = renewal

        self.voc = voc

        self.decisions = []

    # ---------------------------------------------------------

    def execute(self):

        print("\n" + "=" * 70)
        print("DECISION ENGINE")
        print("=" * 70)

        self.executive_summary()

        self.portfolio_summary()

        self.top_priorities()

        print(

            f"\nGenerated {len(self.decisions)} decisions"

        )

        return pd.DataFrame(self.decisions)

    # ---------------------------------------------------------

    def add_decision(

        self,

        category,

        priority,

        title,

        observation,

        business_impact,

        owner,

        recommendation

    ):

        self.decisions.append(

            {

                "Category": category,

                "Priority": priority,

                "Title": title,

                "Observation": observation,

                "Business Impact": business_impact,

                "Owner": owner,

                "Recommendation": recommendation

            }

        )

    # ---------------------------------------------------------

    def executive_summary(self):

        total = self.analytics.kpis.get(

            "Total Tickets",

            0

        )

        confidence = self.analytics.kpis.get(

            "Average Confidence",

            0

        )

        avg_health = round(

            self.health.results["Health Score"].mean(),

            1

        )

        avg_risk = round(

            self.renewal.results["Risk Score"].mean(),

            1

        )

        self.add_decision(

            "Executive",

            "P1",

            "Portfolio Summary",

            (

                f"{total:,} tickets analysed. "

                f"Portfolio Health = {avg_health}. "

                f"Renewal Risk = {avg_risk}."

            ),

            "Provides an executive overview of the customer portfolio.",

            "Leadership",

            "Review portfolio health during weekly business reviews."

        )

        self.add_decision(

            "Executive",

            "P2",

            "Classification Quality",

            (

                f"Average classification confidence is "

                f"{confidence:.1f}%."

            ),

            "Measures confidence in automated intelligence.",

            "Support Operations",

            "Continue improving keyword library and classification rules."

        )

    # ---------------------------------------------------------

    def portfolio_summary(self):

        healthy = len(

            self.health.results[

                self.health.results["Health Status"]

                .isin(

                    [

                        "Healthy",

                        "Excellent"

                    ]

                )

            ]

        )

        risk = len(

            self.renewal.results[

                self.renewal.results["Risk Level"]

                .isin(

                    [

                        "Critical",

                        "High"

                    ]

                )

            ]

        )

        self.add_decision(

            "Customer Success",

            "P1",

            "Portfolio Health",

            (

                f"{healthy} customers are healthy while "

                f"{risk} customers require immediate attention."

            ),

            "Highlights portfolio health distribution.",

            "Customer Success",

            "Focus proactive engagement on high-risk accounts."

        )

    # ---------------------------------------------------------

    def top_priorities(self):

        if len(

            self.recommendations.generated

        ) == 0:

            return

        priorities = [

            r

            for r in self.recommendations.generated

            if r["Priority"] == "P1"

        ]

        self.add_decision(

            "Executive",

            "P1",

            "Top Priorities",

            (

                f"{len(priorities)} high-priority "

                f"initiatives require execution."

            ),

            "Represents highest business value.",

            "Leadership",

            "Review progress weekly until completed."

        )
    # ---------------------------------------------------------

    def product_decisions(self):

        if "Categories" not in self.analytics.summary:

            return

        categories = self.analytics.summary["Categories"]

        if len(categories) == 0:

            return

        top = categories.iloc[0]

        category = str(top["Category"])

        tickets = int(top["Tickets"])

        actions = {

            "AI Issue":
                (
                    "Improve AI onboarding, prompt guidance and in-product education.",
                    "Product"
                ),

            "Product Usage":
                (
                    "Improve feature discoverability and contextual help.",
                    "Product"
                ),

            "Authentication":
                (
                    "Simplify login, SSO and account activation.",
                    "Engineering"
                ),

            "Billing":
                (
                    "Clarify subscription plans and billing workflow.",
                    "Finance"
                ),

            "Product Bug":
                (
                    "Prioritize recurring defects before new features.",
                    "Engineering"
                )

        }

        recommendation, owner = actions.get(

            category,

            (

                "Review recurring customer feedback.",

                "Product"

            )

        )

        self.add_decision(

            "Product",

            "P1",

            "Largest Product Opportunity",

            f"{category} generated {tickets} customer tickets.",

            "Largest source of customer friction.",

            owner,

            recommendation

        )

    # ---------------------------------------------------------

    def engineering_decisions(self):

        engineering = self.health.results[

            self.health.results["Top Driver"]

            == "Product Bugs"

        ]

        if len(engineering) == 0:

            self.add_decision(

                "Engineering",

                "P3",

                "Engineering Stability",

                "No customers are primarily affected by recurring product defects.",

                "Indicates healthy platform stability.",

                "Engineering",

                "Continue preventive maintenance and monitoring."

            )

            return

        self.add_decision(

            "Engineering",

            "P1",

            "Recurring Product Defects",

            f"{len(engineering)} customers have Product Bugs as their primary driver.",

            "Engineering effort should focus on high-impact recurring issues.",

            "Engineering",

            "Prioritize recurring bugs before introducing additional functionality."

        )

    # ---------------------------------------------------------

    def customer_success_decisions(self):

        high_risk = self.renewal.results[

            self.renewal.results["Risk Level"]

            .isin(

                [

                    "Critical",

                    "High"

                ]

            )

        ]

        self.add_decision(

            "Customer Success",

            "P1",

            "High Risk Accounts",

            f"{len(high_risk)} customers require proactive engagement.",

            "Potential impact on renewals and customer satisfaction.",

            "Customer Success",

            "Schedule customer reviews for all high-risk accounts."

        )

        watch = self.health.results[

            self.health.results["Health Status"]

            == "Watch"

        ]

        if len(watch):

            self.add_decision(

                "Customer Success",

                "P2",

                "Watch Accounts",

                f"{len(watch)} customers require monitoring.",

                "Early intervention may prevent health deterioration.",

                "Customer Success",

                "Review adoption and recent support interactions."

            )

    # ---------------------------------------------------------

    def renewal_decisions(self):

        average_probability = round(

            self.renewal.results[

                "Renewal Probability %"

            ].mean(),

            1

        )

        self.add_decision(

            "Renewal",

            "P1",

            "Portfolio Renewal Outlook",

            f"Average renewal probability is {average_probability}%.",

            "Provides an overall view of renewal readiness.",

            "Customer Success",

            "Review accounts with the lowest renewal probability."

        )

    # ---------------------------------------------------------

    def customer_briefs(self):

        customer_column = self.health.results.columns[0]

        top_risk = self.renewal.results.head(10)

        for _, row in top_risk.iterrows():

            customer = row[customer_column]

            self.add_decision(

                "Customer Brief",

                row["Priority"],

                customer,

                (

                    f"Health Score: {row['Health Score']}, "

                    f"Risk: {row['Risk Level']}, "

                    f"Driver: {row['Top Driver']}."

                ),

                "Executive summary for customer review.",

                row["Current Owner"],

                row["Recommended Action"]

            )

    # ---------------------------------------------------------

    def next_best_actions(self):

        actions = self.recommendations.generated

        if len(actions) == 0:

            return

        top_actions = [

            action

            for action in actions

            if action["Priority"] == "P1"

        ][:5]

        for action in top_actions:

            self.add_decision(

                "Next Best Action",

                action["Priority"],

                action["Title"],

                action["Finding"],

                "Highest-value initiative based on platform intelligence.",

                action["Owner"],

                action["Recommendation"]

            )
    # ---------------------------------------------------------

    def ceo_report(self):

        avg_health = round(

            self.health.results["Health Score"].mean(),

            1

        )

        avg_risk = round(

            self.renewal.results["Risk Score"].mean(),

            1

        )

        total_recommendations = len(

            self.recommendations.generated

        )

        self.add_decision(

            "CEO",

            "P1",

            "Executive Portfolio Review",

            (

                f"Portfolio Health = {avg_health}, "

                f"Renewal Risk = {avg_risk}, "

                f"{total_recommendations} strategic recommendations generated."

            ),

            "High-level business summary for executive leadership.",

            "Executive Leadership",

            "Review strategic initiatives during monthly business reviews."

        )

    # ---------------------------------------------------------

    def daily_action_list(self):

        actions = []

        for decision in self.decisions:

            if decision["Priority"] == "P1":

                actions.append(

                    {

                        "Owner": decision["Owner"],

                        "Category": decision["Category"],

                        "Title": decision["Title"],

                        "Action": decision["Recommendation"]

                    }

                )

        return pd.DataFrame(actions)

    # ---------------------------------------------------------

    def save(self):

        output = Path("output")

        output.mkdir(

            parents=True,

            exist_ok=True

        )

        decision_df = pd.DataFrame(self.decisions)

        action_df = self.daily_action_list()

        # --------------------------------------------
        # Excel Report
        # --------------------------------------------

        decision_file = (

            output /

            "Decision_Report.xlsx"

        )

        with pd.ExcelWriter(

            decision_file,

            engine="openpyxl"

        ) as writer:

            decision_df.to_excel(

                writer,

                sheet_name="Executive Decisions",

                index=False

            )

            action_df.to_excel(

                writer,

                sheet_name="Daily Actions",

                index=False

            )

        print(

            f"\n✓ Saved : {decision_file}"

        )

        # --------------------------------------------
        # Executive Brief
        # --------------------------------------------

        brief_file = (

            output /

            "Executive_Brief.txt"

        )

        with open(

            brief_file,

            "w",

            encoding="utf-8"

        ) as f:

            f.write("=" * 80 + "\n")

            f.write("EXECUTIVE DECISION BRIEF\n")

            f.write("=" * 80 + "\n\n")

            for item in self.decisions:

                f.write(

                    f"[{item['Priority']}] "

                    f"{item['Category']}\n"

                )

                f.write(

                    f"Title : {item['Title']}\n"

                )

                f.write(

                    f"Observation : "

                    f"{item['Observation']}\n"

                )

                f.write(

                    f"Business Impact : "

                    f"{item['Business Impact']}\n"

                )

                f.write(

                    f"Owner : "

                    f"{item['Owner']}\n"

                )

                f.write(

                    f"Recommendation : "

                    f"{item['Recommendation']}\n"

                )

                f.write(

                    "-" * 80 + "\n"

                )

        print(

            f"✓ Saved : {brief_file}"

        )

        # --------------------------------------------
        # Daily Action List
        # --------------------------------------------

        action_file = (

            output /

            "Daily_Action_List.xlsx"

        )

        action_df.to_excel(

            action_file,

            index=False

        )

        print(

            f"✓ Saved : {action_file}"

        )

    # ---------------------------------------------------------

    def print_summary(self):

        print("\n" + "=" * 70)

        print("DECISION ENGINE SUMMARY")

        print("=" * 70)

        print(

            f"\nTotal Decisions : "

            f"{len(self.decisions)}"

        )

        decision_df = pd.DataFrame(self.decisions)

        if not decision_df.empty:

            print("\nPriority Distribution")

            print(

                decision_df["Priority"]

                .value_counts()

            )

            print("\nCategory Distribution")

            print(

                decision_df["Category"]

                .value_counts()

            )

    # ---------------------------------------------------------

    def statistics(self):

        decision_df = pd.DataFrame(self.decisions)

        if decision_df.empty:

            return {}

        return {

            "Total Decisions":

                len(decision_df),

            "P1 Decisions":

                len(

                    decision_df[

                        decision_df["Priority"]

                        == "P1"

                    ]

                ),

            "P2 Decisions":

                len(

                    decision_df[

                        decision_df["Priority"]

                        == "P2"

                    ]

                ),

            "Categories":

                decision_df["Category"]

                .nunique()

        }

    # ---------------------------------------------------------

    def execute(self):

        print("\n" + "=" * 70)

        print("DECISION ENGINE")

        print("=" * 70)

        self.executive_summary()

        self.portfolio_summary()

        self.top_priorities()

        self.product_decisions()

        self.engineering_decisions()

        self.customer_success_decisions()

        self.renewal_decisions()

        self.customer_briefs()

        self.next_best_actions()

        self.ceo_report()

        self.print_summary()

        self.save()

        print("\n✓ Decision Engine Completed")

        return pd.DataFrame(self.decisions)