from pathlib import Path
import pandas as pd


class RenewalRiskEngine:
    """
    Renewal Risk Engine

    Uses Customer Health data to
    identify customers requiring
    proactive Customer Success action.

    Output

        output/Renewal_Risk.xlsx
    """

    def __init__(self, health_df):

        self.df = health_df.copy()

        self.results = pd.DataFrame()

    # ---------------------------------------------------------

    def execute(self):

        print("\n" + "=" * 70)
        print("RENEWAL RISK ENGINE")
        print("=" * 70)

        self.results = self.calculate_risk()

        self.print_summary()

        self.save()

        print("\n✓ Renewal Risk Engine Completed")

        return self.results

    # ---------------------------------------------------------

    def calculate_risk(self):

        results = []

        customer_column = self.df.columns[0]

        for _, row in self.df.iterrows():

            score = row["Health Score"]

            tickets = row["Tickets"]

            driver = row["Top Driver"]

            status = row["Health Status"]

            owner = row["Owner"]

            confidence = row["Confidence"]

            # ------------------------------------------
            # Base Risk Score
            # ------------------------------------------

            risk_score = 100 - score

            # ------------------------------------------
            # Ticket Volume Penalty
            # ------------------------------------------

            if tickets > 100:

                risk_score += 20

            elif tickets > 50:

                risk_score += 10

            elif tickets > 20:

                risk_score += 5

            # ------------------------------------------
            # Driver Penalty
            # ------------------------------------------

            penalties = {

                "Product Bugs": 15,

                "Authentication": 12,

                "AI Support": 8,

                "Billing": 10,

                "Product Usage": 6

            }

            risk_score += penalties.get(driver, 5)

            risk_score = max(

                0,

                min(100, round(risk_score))

            )            # -------------------------------------------------
            # Renewal Risk Level
            # -------------------------------------------------

            if risk_score >= 80:

                risk_level = "Critical"

            elif risk_score >= 65:

                risk_level = "High"

            elif risk_score >= 45:

                risk_level = "Medium"

            else:

                risk_level = "Low"

            # -------------------------------------------------
            # Renewal Probability
            # -------------------------------------------------

            renewal_probability = max(

                5,

                min(100, 100 - risk_score)

            )

            # -------------------------------------------------
            # Action Priority
            # -------------------------------------------------

            if risk_level == "Critical":

                priority = "P1"

            elif risk_level == "High":

                priority = "P1"

            elif risk_level == "Medium":

                priority = "P2"

            else:

                priority = "P3"

            # -------------------------------------------------
            # Executive Recommendation
            # -------------------------------------------------

            recommendations = {

                "Product Bugs":

                    "Review recurring defects before renewal discussions.",

                "Authentication":

                    "Schedule onboarding review and investigate login friction.",

                "AI Support":

                    "Arrange AI enablement session and provide workflow guidance.",

                "Billing":

                    "Review subscription, entitlement and renewal terms.",

                "Product Usage":

                    "Conduct adoption review and feature enablement session."

            }

            next_action = recommendations.get(

                driver,

                "Schedule Customer Success review."

            )

            # -------------------------------------------------
            # Escalation Owner
            # -------------------------------------------------

            if risk_level == "Critical":

                escalation = "Director Customer Success"

            elif risk_level == "High":

                escalation = "Customer Success Manager"

            elif risk_level == "Medium":

                escalation = "Customer Success Manager"

            else:

                escalation = "Customer Success Associate"

            # -------------------------------------------------
            # Executive Summary
            # -------------------------------------------------

            summary = (

                f"{driver} is the primary renewal "

                f"risk driver with a "

                f"{risk_level.lower()} renewal risk."

            )

            # -------------------------------------------------
            # Suggested Timeline
            # -------------------------------------------------

            if risk_level == "Critical":

                timeline = "Immediate"

            elif risk_level == "High":

                timeline = "Within 7 Days"

            elif risk_level == "Medium":

                timeline = "Within 30 Days"

            else:

                timeline = "Quarterly Review"

            # -------------------------------------------------

            results.append(

                {

                    customer_column:

                        row[customer_column],

                    "Health Score":

                        score,

                    "Risk Score":

                        risk_score,

                    "Risk Level":

                        risk_level,

                    "Renewal Probability %":

                        renewal_probability,

                    "Priority":

                        priority,

                    "Health Status":

                        status,

                    "Top Driver":

                        driver,

                    "Tickets":

                        tickets,

                    "Confidence":

                        confidence,

                    "Current Owner":

                        owner,

                    "Escalation Owner":

                        escalation,

                    "Executive Summary":

                        summary,

                    "Recommended Action":

                        next_action,

                    "Timeline":

                        timeline

                }

            )

        results = pd.DataFrame(results)

        results = results.sort_values(

            [

                "Risk Score",

                "Health Score"

            ],

            ascending=[

                False,

                True

            ]

        )

        return results
    # ---------------------------------------------------------

    def print_summary(self):

        if len(self.results) == 0:

            return

        print("\n" + "=" * 70)
        print("RENEWAL RISK SUMMARY")
        print("=" * 70)

        print(f"\nCustomers Analysed : {len(self.results):,}")

        print(
            f"Average Risk Score : "
            f"{round(self.results['Risk Score'].mean(),1)}"
        )

        print(
            f"Average Renewal Probability : "
            f"{round(self.results['Renewal Probability %'].mean(),1)}%"
        )

        print("\nRisk Distribution")

        distribution = (

            self.results["Risk Level"]

            .value_counts()

            .sort_index()

        )

        print(distribution)

        print("\nTop 10 Highest Renewal Risks")

        columns = [

            self.results.columns[0],

            "Risk Score",

            "Risk Level",

            "Priority",

            "Top Driver"

        ]

        print(

            self.results

            .head(10)[columns]

        )

    # ---------------------------------------------------------

    def save(self):

        output = Path("output")

        output.mkdir(

            parents=True,

            exist_ok=True

        )

        output_file = (

            output /

            "Renewal_Risk.xlsx"

        )

        summary = pd.DataFrame({

            "Metric": [

                "Customers Analysed",

                "Average Risk Score",

                "Average Renewal Probability",

                "Critical Risk",

                "High Risk",

                "Medium Risk",

                "Low Risk"

            ],

            "Value": [

                len(self.results),

                round(

                    self.results["Risk Score"].mean(),

                    1

                ),

                round(

                    self.results["Renewal Probability %"].mean(),

                    1

                ),

                len(

                    self.results[

                        self.results["Risk Level"]

                        == "Critical"

                    ]

                ),

                len(

                    self.results[

                        self.results["Risk Level"]

                        == "High"

                    ]

                ),

                len(

                    self.results[

                        self.results["Risk Level"]

                        == "Medium"

                    ]

                ),

                len(

                    self.results[

                        self.results["Risk Level"]

                        == "Low"

                    ]

                )

            ]

        })

        executive = self.results[

            [

                self.results.columns[0],

                "Risk Score",

                "Risk Level",

                "Priority",

                "Executive Summary",

                "Timeline"

            ]

        ]

        action_plan = self.results[

            [

                self.results.columns[0],

                "Priority",

                "Recommended Action",

                "Current Owner",

                "Escalation Owner",

                "Timeline"

            ]

        ]

        high_risk = self.results[

            self.results["Risk Level"]

            .isin(

                [

                    "Critical",

                    "High"

                ]

            )

        ]

        with pd.ExcelWriter(

            output_file,

            engine="openpyxl"

        ) as writer:

            summary.to_excel(

                writer,

                sheet_name="Executive Summary",

                index=False

            )

            self.results.to_excel(

                writer,

                sheet_name="Renewal Risk",

                index=False

            )

            executive.to_excel(

                writer,

                sheet_name="Executive View",

                index=False

            )

            high_risk.to_excel(

                writer,

                sheet_name="High Risk",

                index=False

            )

            action_plan.to_excel(

                writer,

                sheet_name="Action Plan",

                index=False

            )

        print(f"\n✓ Saved : {output_file}")

    # ---------------------------------------------------------

    def statistics(self):

        return {

            "Customers":

                len(self.results),

            "Average Risk":

                round(

                    self.results["Risk Score"].mean(),

                    2

                ),

            "Average Renewal Probability":

                round(

                    self.results["Renewal Probability %"].mean(),

                    2

                ),

            "Critical":

                len(

                    self.results[

                        self.results["Risk Level"]

                        == "Critical"

                    ]

                ),

            "High":

                len(

                    self.results[

                        self.results["Risk Level"]

                        == "High"

                    ]

                ),

            "Medium":

                len(

                    self.results[

                        self.results["Risk Level"]

                        == "Medium"

                    ]

                ),

            "Low":

                len(

                    self.results[

                        self.results["Risk Level"]

                        == "Low"

                    ]

                )

        }