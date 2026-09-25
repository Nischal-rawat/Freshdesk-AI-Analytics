from pathlib import Path
import pandas as pd


class HealthEngine:
    """
    Customer Health Engine

    Calculates customer health using
    weighted business metrics.

    Output

        output/Customer_Health.xlsx
    """

    def __init__(self, master_df):

        self.df = master_df.copy()

        self.customer_column = None

        self.results = pd.DataFrame()

    # ---------------------------------------------------------

    def execute(self):

        print("\n" + "=" * 70)
        print("CUSTOMER HEALTH ENGINE")
        print("=" * 70)

        self.customer_column = self.find_customer_column()

        if self.customer_column is None:

            print("No customer column found.")

            return pd.DataFrame()

        self.results = self.calculate_health()

        self.print_summary()

        self.save()

        print("\n✓ Customer Health Engine Completed")

        return self.results

    # ---------------------------------------------------------

    def find_customer_column(self):

        possible_columns = [

            "Institution",

            "University",

            "Company",

            "Organization",

            "Requester Company",

            "Company Name"

        ]

        for column in possible_columns:

            if column in self.df.columns:

                return column

        return None

    # ---------------------------------------------------------

    def calculate_component_scores(
        self,
        customer_df
    ):

        scores = {}

        total = len(customer_df)

        # ------------------------------------------
        # Support Health
        # ------------------------------------------

        support = 100

        if total > 100:

            support -= 40

        elif total > 50:

            support -= 30

        elif total > 20:

            support -= 15

        elif total > 10:

            support -= 8

        scores["Support Health"] = max(0, support)

        # ------------------------------------------
        # Product Quality
        # ------------------------------------------

        product = 100

        bugs = len(

            customer_df[
                customer_df["Category"]
                == "Product Bug"
            ]

        )

        auth = len(

            customer_df[
                customer_df["Category"]
                == "Authentication"
            ]

        )

        performance = len(

            customer_df[
                customer_df["Category"]
                == "Performance"
            ]

        )

        product -= bugs * 5

        product -= auth * 2

        product -= performance * 2

        scores["Product Quality"] = max(0, product)

        # ------------------------------------------
        # AI Experience
        # ------------------------------------------

        ai = 100

        ai_issues = len(

            customer_df[
                customer_df["Category"]
                == "AI Issue"
            ]

        )

        ai -= ai_issues

        scores["AI Experience"] = max(0, ai)

        # ------------------------------------------
        # Adoption
        # Placeholder
        # ------------------------------------------

        scores["Adoption"] = 80

        # ------------------------------------------
        # Renewal
        # Placeholder
        # ------------------------------------------

        scores["Renewal"] = 85

        # ------------------------------------------
        # Engagement
        # Placeholder
        # ------------------------------------------

        scores["Engagement"] = 75

        return scores

    # ---------------------------------------------------------

    def calculate_health(self):

        results = []

        customers = (

            self.df[self.customer_column]

            .fillna("Unknown")

            .unique()

        )

        for customer in customers:

            customer_df = self.df[

                self.df[self.customer_column]

                == customer

            ]

            component_scores = self.calculate_component_scores(

                customer_df

            )
                        # -------------------------------------------------
            # Overall Health Score
            # -------------------------------------------------

            score = round(

                component_scores["Support Health"] * 0.30 +

                component_scores["Product Quality"] * 0.20 +

                component_scores["AI Experience"] * 0.10 +

                component_scores["Adoption"] * 0.20 +

                component_scores["Renewal"] * 0.10 +

                component_scores["Engagement"] * 0.10

            )

            score = max(0, min(100, score))

            # -------------------------------------------------
            # Health Status
            # -------------------------------------------------

            if score >= 90:

                status = "Excellent"

            elif score >= 80:

                status = "Healthy"

            elif score >= 70:

                status = "Good"

            elif score >= 60:

                status = "Watch"

            elif score >= 40:

                status = "At Risk"

            else:

                status = "Critical"

            # -------------------------------------------------
            # Category Counts
            # -------------------------------------------------

            bugs = len(

                customer_df[
                    customer_df["Category"]
                    == "Product Bug"
                ]

            )

            auth = len(

                customer_df[
                    customer_df["Category"]
                    == "Authentication"
                ]

            )

            ai = len(

                customer_df[
                    customer_df["Category"]
                    == "AI Issue"
                ]

            )

            billing = len(

                customer_df[
                    customer_df["Category"]
                    == "Billing"
                ]

            )

            usage = len(

                customer_df[
                    customer_df["Category"]
                    == "Product Usage"
                ]

            )

            # -------------------------------------------------
            # Root Cause
            # -------------------------------------------------

            issue_counts = {

                "Product Bugs": bugs,

                "Authentication": auth,

                "AI Support": ai,

                "Billing": billing,

                "Product Usage": usage

            }

            top_driver = max(

                issue_counts,

                key=issue_counts.get

            )

            # -------------------------------------------------
            # Recommendation
            # -------------------------------------------------

            recommendations = {

                "Product Bugs":

                    "Prioritize recurring defects and review engineering backlog.",

                "Authentication":

                    "Improve onboarding, login experience and SSO configuration.",

                "AI Support":

                    "Create AI tutorials, examples and contextual guidance.",

                "Billing":

                    "Improve subscription, entitlement and billing communication.",

                "Product Usage":

                    "Improve feature discoverability and onboarding."

            }

            owners = {

                "Product Bugs": "Engineering",

                "Authentication": "Engineering",

                "AI Support": "Product",

                "Billing": "Finance",

                "Product Usage": "Customer Success"

            }

            recommendation = recommendations.get(

                top_driver,

                "Review customer support history."

            )

            owner = owners.get(

                top_driver,

                "Support"

            )

            # -------------------------------------------------
            # Confidence
            # -------------------------------------------------

            confidence = round(

                (

                    component_scores["Support Health"]

                    +

                    component_scores["Product Quality"]

                    +

                    component_scores["AI Experience"]

                ) / 3,

                1

            )

            # -------------------------------------------------
            # Risk
            # -------------------------------------------------

            if score >= 80:

                risk = "Low"

            elif score >= 60:

                risk = "Medium"

            else:

                risk = "High"

            # -------------------------------------------------

            results.append(

                {

                    self.customer_column: customer,

                    "Tickets": len(customer_df),

                    "Health Score": score,

                    "Health Status": status,

                    "Support Health":

                        component_scores["Support Health"],

                    "Product Quality":

                        component_scores["Product Quality"],

                    "AI Experience":

                        component_scores["AI Experience"],

                    "Adoption":

                        component_scores["Adoption"],

                    "Renewal":

                        component_scores["Renewal"],

                    "Engagement":

                        component_scores["Engagement"],

                    "Top Driver": top_driver,

                    "Risk": risk,

                    "Confidence": confidence,

                    "Owner": owner,

                    "Recommended Action":

                        recommendation

                }

            )

        results = pd.DataFrame(results)

        results = results.sort_values(

            "Health Score",

            ascending=True

        )

        return results
        # ---------------------------------------------------------

    def print_summary(self):

        if len(self.results) == 0:

            return

        print("\n" + "=" * 70)
        print("CUSTOMER HEALTH SUMMARY")
        print("=" * 70)

        print(f"\nCustomers Analysed : {len(self.results):,}")

        print(
            f"Average Health Score : "
            f"{round(self.results['Health Score'].mean(),1)}"
        )

        print("\nHealth Distribution")

        distribution = (

            self.results["Health Status"]

            .value_counts()

            .sort_index()

        )

        print(distribution)

        print("\nTop 10 Highest Risk Customers")

        risk = self.results.sort_values(

            "Health Score"

        ).head(10)

        columns = [

            self.customer_column,

            "Health Score",

            "Health Status",

            "Risk",

            "Top Driver"

        ]

        print(risk[columns])

    # ---------------------------------------------------------

    def save(self):

        output = Path("output")

        output.mkdir(

            parents=True,

            exist_ok=True

        )

        output_file = (

            output /

            "Customer_Health.xlsx"

        )

        summary = pd.DataFrame({

            "Metric": [

                "Customers Analysed",

                "Average Health Score",

                "Healthy Customers",

                "Watch Customers",

                "At Risk Customers",

                "Critical Customers"

            ],

            "Value": [

                len(self.results),

                round(

                    self.results["Health Score"].mean(),

                    1

                ),

                len(

                    self.results[

                        self.results["Health Status"]

                        == "Healthy"

                    ]

                ),

                len(

                    self.results[

                        self.results["Health Status"]

                        == "Watch"

                    ]

                ),

                len(

                    self.results[

                        self.results["Health Status"]

                        == "At Risk"

                    ]

                ),

                len(

                    self.results[

                        self.results["Health Status"]

                        == "Critical"

                    ]

                )

            ]

        })

        high_risk = self.results[

            self.results["Risk"] == "High"

        ]

        csm_actions = self.results[

            [

                self.customer_column,

                "Health Score",

                "Health Status",

                "Top Driver",

                "Recommended Action",

                "Owner"

            ]

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

                sheet_name="Customer Health",

                index=False

            )

            high_risk.to_excel(

                writer,

                sheet_name="High Risk",

                index=False

            )

            csm_actions.to_excel(

                writer,

                sheet_name="CSM Action Plan",

                index=False

            )

        print(f"\n✓ Saved : {output_file}")

    # ---------------------------------------------------------

    def health_statistics(self):

        stats = {

            "Customers":

                len(self.results),

            "Average Score":

                round(

                    self.results["Health Score"].mean(),

                    2

                ),

            "Highest Score":

                self.results["Health Score"].max(),

            "Lowest Score":

                self.results["Health Score"].min(),

            "High Risk":

                len(

                    self.results[

                        self.results["Risk"]

                        == "High"

                    ]

                ),

            "Healthy":

                len(

                    self.results[

                        self.results["Health Status"]

                        == "Healthy"

                    ]

                )

        }

        return stats