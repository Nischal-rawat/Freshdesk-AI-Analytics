from pathlib import Path
import pandas as pd


class VoiceOfCustomerEngine:
    """
    Voice of Customer Engine

    Generates executive observations from
    analytics, insights and recommendations.

    Output

        output/Voice_of_Customer_Report.xlsx
        output/Voice_of_Customer_Report.txt
    """

    def __init__(
        self,
        analytics,
        insights,
        recommendations,
        health,
        renewal
    ):

        self.analytics = analytics

        self.insights = insights

        self.recommendations = recommendations

        self.health = health

        self.renewal = renewal

        self.report = []

    # -----------------------------------------------------

    def execute(self):

        print("\n" + "=" * 70)
        print("VOICE OF CUSTOMER ENGINE")
        print("=" * 70)

        self.executive_summary()

        self.product_quality()

        self.support_analysis()

        self.customer_success_analysis()

        self.ai_analysis()

        self.business_summary()

        print(f"\nGenerated {len(self.report)} observations")

        return pd.DataFrame(self.report)

    # -----------------------------------------------------

    def add_observation(

        self,

        section,

        title,

        observation,

        business_impact,

        recommendation

    ):

        self.report.append(

            {

                "Section": section,

                "Title": title,

                "Observation": observation,

                "Business Impact": business_impact,

                "Recommendation": recommendation

            }

        )

    # -----------------------------------------------------

    def executive_summary(self):

        total = self.analytics.kpis.get(

            "Total Tickets",

            0

        )

        self.add_observation(

            "Executive",

            "Overall Support Demand",

            f"{total:,} tickets were analysed.",

            "Provides baseline support demand.",

            "Track trends monthly."

        )

    # -----------------------------------------------------

    def product_quality(self):

        categories = self.analytics.summary.get(

            "Categories",

            pd.DataFrame()

        )

        if len(categories) == 0:

            return

        top = categories.iloc[0]

        self.add_observation(

            "Product",

            "Largest Support Category",

            f"{top['Category']} generated {int(top['Tickets'])} tickets.",

            "Largest source of customer friction.",

            "Prioritize improvements in this area."

        )

    # -----------------------------------------------------

    def support_analysis(self):

        avg = round(

            self.health.results["Health Score"].mean(),

            1

        )

        self.add_observation(

            "Support",

            "Portfolio Health",

            f"Average customer health score is {avg}.",

            "Reflects overall customer experience.",

            "Review low-health customers first."

        )

    # -----------------------------------------------------

    def customer_success_analysis(self):

        high = len(

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

        self.add_observation(

            "Customer Success",

            "Renewal Risk",

            f"{high} customers require proactive engagement.",

            "Potential renewal risk.",

            "Prioritize executive outreach."

        )

    # -----------------------------------------------------

    def ai_analysis(self):

        ai = self.analytics.summary.get(

            "AI",

            pd.DataFrame()

        )

        if len(ai) == 0:

            return

        ai = ai.sort_values(

            "Tickets",

            ascending=False

        )

        top = ai.iloc[0]

        self.add_observation(

            "AI",

            "AI Experience",

            f"{top['AI Feature']} generated the highest AI support demand.",

            "Opportunity to improve AI adoption.",

            "Review prompts, onboarding and documentation."

        )

    # -----------------------------------------------------

    def business_summary(self):

        recommendations = len(

            self.recommendations.generated

        )

        self.add_observation(

            "Business",

            "Recommendations Generated",

            f"{recommendations} executive recommendations created.",

            "Provides actionable roadmap.",

            "Track implementation quarterly."

        )
    # -----------------------------------------------------

    def product_maturity_assessment(self):

        categories = self.analytics.summary.get(

            "Categories",

            pd.DataFrame()

        )

        if len(categories) == 0:

            return

        bugs = 0
        auth = 0
        usage = 0
        ai = 0

        for _, row in categories.iterrows():

            category = str(row["Category"])
            tickets = int(row["Tickets"])

            if category == "Product Bug":
                bugs = tickets

            elif category == "Authentication":
                auth = tickets

            elif category == "Product Usage":
                usage = tickets

            elif category == "AI Issue":
                ai = tickets

        total = max(
            self.analytics.kpis["Total Tickets"],
            1
        )

        reliability = max(
            0,
            round(100 - (bugs / total * 100))
        )

        usability = max(
            0,
            round(100 - (usage / total * 100))
        )

        discoverability = max(
            0,
            round(100 - ((usage + ai) / total * 100))
        )

        onboarding = max(
            0,
            round(100 - (auth / total * 100))
        )

        self.add_observation(

            "Product Maturity",

            "Reliability",

            f"Reliability Score : {reliability}/100",

            "Indicates engineering stability.",

            "Continue investing in quality."

        )

        self.add_observation(

            "Product Maturity",

            "Usability",

            f"Usability Score : {usability}/100",

            "Shows ease of product usage.",

            "Improve workflow guidance."

        )

        self.add_observation(

            "Product Maturity",

            "Discoverability",

            f"Discoverability Score : {discoverability}/100",

            "Measures how easily users find existing features.",

            "Improve feature discovery."

        )

        self.add_observation(

            "Product Maturity",

            "Onboarding",

            f"Onboarding Score : {onboarding}/100",

            "Measures first-time user experience.",

            "Improve onboarding journey."

        )

    # -----------------------------------------------------

    def customer_journey_analysis(self):

        health = self.health.results

        average = round(

            health["Health Score"].mean(),

            1

        )

        if average >= 85:

            stage = "Adoption"

        elif average >= 70:

            stage = "Growth"

        elif average >= 55:

            stage = "Activation"

        else:

            stage = "Onboarding"

        self.add_observation(

            "Customer Journey",

            "Journey Stage",

            f"Most customers are currently in the {stage} stage.",

            "Represents portfolio maturity.",

            "Target activities based on lifecycle stage."

        )

    # -----------------------------------------------------

    def engineering_assessment(self):

        categories = self.analytics.summary.get(

            "Categories",

            pd.DataFrame()

        )

        if len(categories) == 0:

            return

        bugs = categories[

            categories["Category"]

            == "Product Bug"

        ]

        if len(bugs):

            tickets = int(

                bugs.iloc[0]["Tickets"]

            )

        else:

            tickets = 0

        total = max(

            self.analytics.kpis["Total Tickets"],

            1

        )

        percentage = round(

            tickets / total * 100,

            2

        )

        if percentage <= 5:

            observation = (

                "Engineering quality appears healthy."

            )

            recommendation = (

                "Continue focusing on usability improvements."

            )

        else:

            observation = (

                "Product defects require attention."

            )

            recommendation = (

                "Prioritize recurring bug fixes."

            )

        self.add_observation(

            "Engineering",

            "Engineering Assessment",

            observation,

            f"{percentage}% of tickets are product defects.",

            recommendation

        )

    # -----------------------------------------------------

    def executive_recommendations(self):

        recommendations = self.recommendations.generated

        priority = [

            r

            for r in recommendations

            if r["Priority"] == "P1"

        ]

        self.add_observation(

            "Executive",

            "Priority Recommendations",

            f"{len(priority)} P1 recommendations generated.",

            "Highest-value initiatives.",

            "Track execution monthly."

        )

    # -----------------------------------------------------

    def portfolio_summary(self):

        avg_health = round(

            self.health.results["Health Score"].mean(),

            1

        )

        avg_risk = round(

            self.renewal.results["Risk Score"].mean(),

            1

        )

        self.add_observation(

            "Portfolio",

            "Portfolio Assessment",

            f"Average Health = {avg_health}, Average Risk = {avg_risk}.",

            "Overall customer portfolio status.",

            "Review customers below portfolio average."

        )    # -----------------------------------------------------

    def executive_narrative(self):

        total = self.analytics.kpis.get(
            "Total Tickets",
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

        narrative = (
            f"{total:,} customer tickets were analysed. "
            f"The portfolio health score is {avg_health}/100 "
            f"with an average renewal risk score of {avg_risk}/100. "
            f"Support demand is primarily driven by customer education, "
            f"AI adoption, onboarding and feature discoverability rather "
            f"than widespread software defects. "
            f"Investment should focus on improving customer experience, "
            f"contextual guidance and proactive Customer Success engagement."
        )

        self.add_observation(

            "Executive",

            "Executive Narrative",

            narrative,

            "Provides an executive overview.",

            "Review monthly with Product and Customer Success leadership."

        )

    # -----------------------------------------------------

    def save(self):

        output = Path("output")

        output.mkdir(

            parents=True,

            exist_ok=True

        )

        excel_file = output / "Voice_of_Customer_Report.xlsx"

        text_file = output / "Voice_of_Customer_Report.txt"

        report = pd.DataFrame(self.report)

        # ---------------- Excel ----------------

        with pd.ExcelWriter(

            excel_file,

            engine="openpyxl"

        ) as writer:

            report.to_excel(

                writer,

                sheet_name="Voice of Customer",

                index=False

            )

        # ---------------- Text ----------------

        with open(

            text_file,

            "w",

            encoding="utf-8"

        ) as f:

            f.write("=" * 80 + "\n")
            f.write("VOICE OF CUSTOMER REPORT\n")
            f.write("=" * 80 + "\n\n")

            for row in self.report:

                f.write(f"Section        : {row['Section']}\n")
                f.write(f"Title          : {row['Title']}\n")
                f.write(f"Observation    : {row['Observation']}\n")
                f.write(f"Business Impact: {row['Business Impact']}\n")
                f.write(f"Recommendation : {row['Recommendation']}\n")
                f.write("-" * 80 + "\n")

        print(f"\n✓ Saved : {excel_file}")
        print(f"✓ Saved : {text_file}")

    # -----------------------------------------------------

    def print_summary(self):

        print("\n" + "=" * 70)
        print("VOICE OF CUSTOMER SUMMARY")
        print("=" * 70)

        print(f"\nObservations Generated : {len(self.report)}")

        sections = pd.DataFrame(

            self.report

        )["Section"].value_counts()

        print("\nSections")

        print(sections)

    # -----------------------------------------------------

    def statistics(self):

        return {

            "Observations":

                len(self.report),

            "Sections":

                len(

                    pd.DataFrame(

                        self.report

                    )["Section"].unique()

                )

        }

    # -----------------------------------------------------

    def execute(self):

        print("\n" + "=" * 70)
        print("VOICE OF CUSTOMER ENGINE")
        print("=" * 70)

        self.executive_summary()

        self.product_quality()

        self.support_analysis()

        self.customer_success_analysis()

        self.ai_analysis()

        self.business_summary()

        self.product_maturity_assessment()

        self.customer_journey_analysis()

        self.engineering_assessment()

        self.executive_recommendations()

        self.portfolio_summary()

        self.executive_narrative()

        self.print_summary()

        self.save()

        print("\n✓ Voice of Customer Engine Completed")

        return pd.DataFrame(self.report)
    