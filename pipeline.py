"""
=========================================================
Support Intelligence Platform
Pipeline
Version : 5.0
=========================================================
"""

from time import perf_counter

from loader import FreshdeskLoader
from validator import DatasetValidator
from cleaner import DatasetCleaner
from normalizer import TicketNormalizer
from classifier_factory import get_classifier

classifier = get_classifier()

from analytics import AnalyticsEngine
from insights import InsightsEngine
from recommendation_engine import RecommendationEngine
from health_engine import HealthEngine
from renewal_risk_engine import RenewalRiskEngine
from voc_engine import VoiceOfCustomerEngine
from dashboard_builder import DashboardBuilder


class SupportIntelligencePipeline:

    def __init__(self, filepath=None):

        self.filepath = filepath

        self.df = None

        self.master_df = None

        self.analytics = None
        self.insights = None
        self.recommendations = None
        self.health = None
        self.renewal = None
        self.voc = None

    # ==========================================================
    # Helper
    # ==========================================================

    def step(self, number, total, title):

        print("\n" + "=" * 80)
        print(f"[{number}/{total}] {title}")
        print("=" * 80)

    # ==========================================================
    # Run
    # ==========================================================

    def run(self):

        total_steps = 11

        start = perf_counter()

        # ------------------------------------------------------
        # Load
        # ------------------------------------------------------

        self.step(1, total_steps, "Loading Dataset")

        loader = FreshdeskLoader(self.filepath)

        self.df = loader.load()

        # ------------------------------------------------------
        # Validate
        # ------------------------------------------------------

        self.step(2, total_steps, "Validating Dataset")

        DatasetValidator(self.df).validate()

        # ------------------------------------------------------
        # Clean
        # ------------------------------------------------------

        self.step(3, total_steps, "Cleaning Dataset")

        cleaner = DatasetCleaner(self.df)

        self.df = cleaner.clean()

        # ------------------------------------------------------
        # Normalize
        # ------------------------------------------------------

        self.step(4, total_steps, "Normalizing Text")

        normalizer = TicketNormalizer(self.df)

        self.df = normalizer.normalize()

        # ------------------------------------------------------
        # Classification
        # ------------------------------------------------------

        self.step(5, total_steps, "Classifying Tickets")

        classifier = TicketClassifier(self.df)

        self.master_df = classifier.classify()

        classifier.summary()

        classifier.save_master_dataset()

        # ------------------------------------------------------
        # Analytics
        # ------------------------------------------------------

        self.step(6, total_steps, "Analytics Engine")

        self.analytics = AnalyticsEngine(self.master_df)

        self.analytics.execute()

        # ------------------------------------------------------
        # Insights
        # ------------------------------------------------------

        self.step(7, total_steps, "Executive Insights")

        self.insights = InsightsEngine(self.analytics)

        self.insights.execute()

        # ------------------------------------------------------
        # Recommendations
        # ------------------------------------------------------

        self.step(8, total_steps, "Recommendation Engine")

        self.recommendations = RecommendationEngine(self.analytics)

        self.recommendations.execute()

        # ------------------------------------------------------
        # Customer Health
        # ------------------------------------------------------

        self.step(9, total_steps, "Customer Health")

        self.health = HealthEngine(self.master_df)

        self.health.execute()

        # ------------------------------------------------------
        # Renewal Risk
        # ------------------------------------------------------

        self.step(10, total_steps, "Renewal Risk")

        self.renewal = RenewalRiskEngine(self.health.results)

        self.renewal.execute()

        # ------------------------------------------------------
        # Voice of Customer
        # ------------------------------------------------------

        self.step(11, total_steps, "Voice of Customer")

        self.voc = VoiceOfCustomerEngine(

            self.analytics,

            self.insights,

            self.recommendations,

            self.health,

            self.renewal

        )

        self.voc.execute()

        # ------------------------------------------------------
        # Dashboard
        # ------------------------------------------------------

        print("\n" + "=" * 80)
        print("Building Executive Dashboard")
        print("=" * 80)

        DashboardBuilder(

            self.analytics,

            self.insights,

            self.recommendations,

            self.health,

            self.renewal,

            self.voc

        ).execute()

        # ------------------------------------------------------
        # Summary
        # ------------------------------------------------------

        elapsed = perf_counter() - start

        print("\n" + "=" * 80)
        print("PIPELINE COMPLETE")
        print("=" * 80)

        print(f"Tickets Processed : {len(self.master_df):,}")

        print(f"Insights          : {len(self.insights.insights):,}")

        print(f"Recommendations   : {len(self.recommendations.generated):,}")

        print(f"Customers         : {len(self.health.results):,}")

        print(f"Execution Time    : {elapsed:.2f} sec")

        print("=" * 80)

        return True