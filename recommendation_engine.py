from pathlib import Path
import operator

import pandas as pd


class RecommendationEngine:
    """
    Recommendation Engine

    Reads analytics output,
    evaluates business rules,
    and generates
    executive recommendations.
    """

    def __init__(self, analytics):

        self.analytics = analytics

        self.summary = analytics.summary

        self.kpis = analytics.kpis

        self.metrics = {}

        self.rules = None

        self.recommendations = None

        self.impact = None

        self.generated = []

        self.load_rules()

        self.build_metrics()

    # ----------------------------------------------------------

    def load_rules(self):

        config = Path("config")

        file = config / "recommendation_rules.xlsx"

        if not file.exists():

            raise FileNotFoundError(
                "recommendation_rules.xlsx not found."
            )

        self.rules = pd.read_csv(
            file,
            sheet_name="Rules"
        )

        self.recommendations = pd.read_csv(
            file,
            sheet_name="Recommendations"
        )

        self.impact = pd.read_csv(
            file,
            sheet_name="Impact"
        )

        print("\nRecommendation Rules Loaded")

        print(f"Rules             : {len(self.rules)}")

        print(f"Recommendations   : {len(self.recommendations)}")

    # ----------------------------------------------------------

    def build_metrics(self):

        """
        Converts analytics
        into a metrics dictionary.
        """

        total = self.kpis.get(
            "Total Tickets",
            1
        )

        self.metrics["Total Tickets"] = total

        self.metrics["Avg Confidence"] = self.kpis.get(
            "Average Confidence",
            0
        )

        # ------------------------------------------

        if "Categories" in self.summary:

            categories = self.summary["Categories"]

            for _, row in categories.iterrows():

                metric = f"{row['Category']} %"

                value = round(

                    row["Tickets"]

                    / total

                    * 100,

                    2

                )

                self.metrics[metric] = value

        # ------------------------------------------

        if "Products" in self.summary:

            products = self.summary["Products"]

            unknown = products[

                products["Product"] == "Unknown"

            ]

            if len(unknown):

                value = round(

                    unknown.iloc[0]["Tickets"]

                    / total

                    * 100,

                    2

                )

                self.metrics["Unknown Product %"] = value

            else:

                self.metrics["Unknown Product %"] = 0

        print("\nBusiness Metrics")

        for key, value in self.metrics.items():

            print(f"{key:<35} {value}")

    # ----------------------------------------------------------

    def compare(

        self,

        actual,

        operator_symbol,

        threshold

    ):

        operations = {

            ">": operator.gt,

            "<": operator.lt,

            ">=": operator.ge,

            "<=": operator.le,

            "==": operator.eq,

            "!=": operator.ne,

        }

        if operator_symbol not in operations:

            return False

        return operations[operator_symbol](

            actual,

            threshold

        )

    # ----------------------------------------------------------

    def execute(self):

        print("\n" + "=" * 70)

        print("RECOMMENDATION ENGINE")

        print("=" * 70)

        self.evaluate_rules()

        self.create_outputs()

        print(

            f"\nGenerated {len(self.generated)} recommendations"

        )

        return pd.DataFrame(self.generated)

    # ----------------------------------------------------------

    def evaluate_rules(self):

        enabled_rules = self.rules[

            self.rules["Enabled"] == True

        ]

        for _, rule in enabled_rules.iterrows():

            metric = rule["Metric"]

            operator_symbol = rule["Operator"]

            threshold = rule["Threshold"]

            recommendation_id = rule["Recommendation ID"]

            actual = self.metrics.get(

                metric,

                None

            )

            if actual is None:

                continue

            triggered = self.compare(

                actual,

                operator_symbol,

                threshold

            )

            if not triggered:

                continue

            recommendation = self.recommendations[

                self.recommendations["Recommendation ID"]

                == recommendation_id

            ]

            if len(recommendation) == 0:

                continue

            impact = self.impact[

                self.impact["Recommendation ID"]

                == recommendation_id

            ]

            rec = recommendation.iloc[0]

            if len(impact):

                imp = impact.iloc[0]

            else:

                imp = {}

            self.generated.append(

                {

                    "Recommendation ID": recommendation_id,

                    "Metric": metric,

                    "Actual": actual,

                    "Threshold": threshold,

                    "Title": rec["Title"],

                    "Owner": rec["Owner"],

                    "Priority": rec["Priority"],

                    "Effort": rec["Effort"],

                    "Expected Benefit":

                        rec["Expected Benefit"],

                    "Business Impact":

                        imp.get(

                            "Business Impact",

                            ""

                        ),

                    "Estimated Ticket Reduction":

                        imp.get(

                            "Estimated Ticket Reduction",

                            ""

                        ),

                    "Estimated Adoption Improvement":

                        imp.get(

                            "Estimated Adoption Improvement",

                            ""

                        ),

                    "Status":

                        "Proposed"

                }

            )

        print(

            f"\nTriggered Rules : {len(self.generated)}"

        )

    # ----------------------------------------------------------

    def create_outputs(self):

        if len(self.generated) == 0:

            print("\nNo recommendations generated.")

            return

        df = pd.DataFrame(

            self.generated

        )

        output = Path("output")

        output.mkdir(

            parents=True,

            exist_ok=True

        )

        register = output / "Recommendation_Register.xlsx"

        action = output / "Executive_Action_Plan.xlsx"

        engineering = output / "Engineering_Backlog.xlsx"

        product = output / "Product_Backlog.xlsx"

        cs = output / "Customer_Success_Action_Plan.xlsx"

        df.to_excel(

            register,

            index=False

        )

        df.to_excel(

            action,

            index=False

        )

        df[

            df["Owner"]

            == "Engineering"

        ].to_excel(

            engineering,

            index=False

        )

        df[

            df["Owner"]

            == "Product"

        ].to_excel(

            product,

            index=False

        )

        df[

            df["Owner"]

            == "Customer Success"

        ].to_excel(

            cs,

            index=False

        )

        print("\nRecommendation Register Saved")

        print(register)

        print(action)

        print(engineering)

        print(product)

        print(cs)