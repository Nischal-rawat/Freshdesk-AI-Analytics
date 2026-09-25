"""
keyword_matcher.py
Part 1 - Core Configuration & Keyword Engine

Version: 5.0
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
from pathlib import Path
import re
# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
REPORT_DIR = BASE_DIR / "reports"
DASHBOARD_DIR = BASE_DIR / "dashboards"

INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)
DASHBOARD_DIR.mkdir(exist_ok=True)


# ==========================================================
# CONFIG
# ==========================================================

MATCH_THRESHOLD = 1

STOP_WORDS: Set[str] = {
    "a", "an", "the", "is", "are", "was", "were",
    "of", "to", "for", "in", "on", "at", "by",
    "with", "without", "and", "or", "if", "as",
    "be", "been", "being", "from", "into", "this",
    "that", "it", "its", "their", "there", "our",
    "your", "you", "we", "they", "them", "he",
    "she", "his", "her", "i", "me", "my", "mine",
    "do", "does", "did", "done", "can", "could",
    "will", "would", "should", "may", "might",
    "about", "after", "before", "during", "than",
    "then", "also", "very", "have", "has", "had"
}


# ==========================================================
# CATEGORY DEFINITIONS
# ==========================================================

CATEGORY_KEYWORDS: Dict[str, List[str]] = {

    "Login Issue": [
        "login",
        "log in",
        "sign in",
        "signin",
        "authentication",
        "password",
        "otp",
        "verification",
        "access denied",
        "cannot login",
        "unable to login",
        "forgot password"
    ],

    "Account Access": [
        "account locked",
        "unlock",
        "access",
        "permission",
        "role",
        "authorization",
        "admin access",
        "user access"
    ],

    "Subscription": [
        "subscription",
        "plan",
        "license",
        "renewal",
        "renew",
        "expiry",
        "expired",
        "payment",
        "invoice",
        "billing",
        "purchase"
    ],

    "Grammar Suggestions": [
        "grammar",
        "correction",
        "sentence",
        "rewrite",
        "language",
        "editing",
        "writing suggestions"
    ],

    "AI Features": [
        "ai",
        "ai studio",
        "ask ai",
        "rewrite with ai",
        "copilot",
        "assistant",
        "generate",
        "summarize",
        "paraphrase"
    ],

    "Plagiarism": [
        "plagiarism",
        "similarity",
        "duplicate",
        "turnitin",
        "originality"
    ],

    "Citation": [
        "citation",
        "reference",
        "apa",
        "mla",
        "harvard",
        "ieee",
        "vancouver"
    ],

    "DocuMark": [
        "documark",
        "document score",
        "document analysis",
        "quality score"
    ],

    "Performance": [
        "slow",
        "lag",
        "loading",
        "freeze",
        "timeout",
        "performance",
        "takes long"
    ],

    "Bug Report": [
        "bug",
        "issue",
        "unexpected",
        "error",
        "crash",
        "broken",
        "exception",
        "stack trace"
    ],

    "Feature Request": [
        "feature request",
        "enhancement",
        "improvement",
        "would like",
        "suggestion",
        "please add",
        "new feature"
    ]
}


# ==========================================================
# DATA CLASS
# ==========================================================

@dataclass
class MatchResult:
    category: str
    score: int
    matched_keywords: List[str]


# ==========================================================
# NORMALIZATION
# ==========================================================

class TextNormalizer:

    _whitespace = re.compile(r"\s+")
    _punctuation = re.compile(r"[^a-z0-9 ]")

    @staticmethod
    def normalize(text: str) -> str:
        if text is None:
            return ""

        text = text.lower()
        text = TextNormalizer._punctuation.sub(" ", text)
        text = TextNormalizer._whitespace.sub(" ", text)
        return text.strip()

    @staticmethod
    def tokenize(text: str) -> List[str]:
        normalized = TextNormalizer.normalize(text)

        return [
            token
            for token in normalized.split()
            if token not in STOP_WORDS
        ]


# ==========================================================
# KEYWORD MATCHER
# ==========================================================

class KeywordMatcher:

    def __init__(self, category_keywords: Dict[str, List[str]]):
        self.category_keywords = category_keywords

    def match(self, text: str) -> List[MatchResult]:

        normalized = TextNormalizer.normalize(text)

        results: List[MatchResult] = []

        for category, keywords in self.category_keywords.items():

            matched = []

            for keyword in keywords:

                kw = TextNormalizer.normalize(keyword)

                if kw in normalized:
                    matched.append(keyword)

            if len(matched) >= MATCH_THRESHOLD:
                results.append(
                    MatchResult(
                        category=category,
                        score=len(matched),
                        matched_keywords=matched
                    )
                )

        results.sort(
            key=lambda x: x.score,
            reverse=True
        )

        return results

    def best_match(self, text: str) -> Optional[MatchResult]:

        matches = self.match(text)

        if not matches:
            return None

        return matches[0]


# ==========================================================
# MULTI-LABEL MATCHER
# ==========================================================

class MultiLabelMatcher:

    def __init__(self):
        self.matcher = KeywordMatcher(CATEGORY_KEYWORDS)

    def predict(
        self,
        subject: str,
        description: str
    ) -> List[MatchResult]:

        combined = f"{subject} {description}"

        return self.matcher.match(combined)

    def predict_primary(
        self,
        subject: str,
        description: str
    ) -> Optional[MatchResult]:

        combined = f"{subject} {description}"

        return self.matcher.best_match(combined)
    # ==========================================================
# PART 2
# SCORING ENGINE
# ==========================================================

from collections import Counter
from typing import Iterable


class ScoreEngine:
    """
    Computes weighted confidence scores for category matches.
    """

    def __init__(
        self,
        category_keywords: Dict[str, List[str]],
        exact_weight: int = 3,
        partial_weight: int = 1,
    ):
        self.category_keywords = category_keywords
        self.exact_weight = exact_weight
        self.partial_weight = partial_weight

    def score(
        self,
        text: str,
    ) -> Dict[str, Dict]:

        normalized = TextNormalizer.normalize(text)
        tokens = set(TextNormalizer.tokenize(text))

        scores = {}

        for category, keywords in self.category_keywords.items():

            score = 0
            matched = []

            for keyword in keywords:

                keyword_norm = TextNormalizer.normalize(keyword)

                # Exact phrase match
                if keyword_norm in normalized:
                    score += self.exact_weight
                    matched.append(keyword)
                    continue

                # Partial token matching
                keyword_tokens = keyword_norm.split()

                if any(token in tokens for token in keyword_tokens):
                    score += self.partial_weight
                    matched.append(keyword)

            if score > 0:
                scores[category] = {
                    "score": score,
                    "matches": matched,
                }

        return scores

    def ranked(
        self,
        text: str,
    ) -> List[Tuple[str, Dict]]:

        scores = self.score(text)

        return sorted(
            scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True,
        )


# ==========================================================
# CONFIDENCE CALCULATOR
# ==========================================================

class ConfidenceCalculator:

    @staticmethod
    def calculate(
        category_score: int,
        max_score: int,
    ) -> float:

        if max_score == 0:
            return 0.0

        confidence = (category_score / max_score) * 100

        if confidence > 100:
            confidence = 100

        return round(confidence, 2)


# ==========================================================
# TICKET CLASSIFIER
# ==========================================================

class TicketClassifier:

    def __init__(self):

        self.engine = ScoreEngine(CATEGORY_KEYWORDS)

    def classify(
        self,
        subject: str,
        description: str,
    ) -> Dict:

        text = f"{subject} {description}"

        ranked = self.engine.ranked(text)

        if not ranked:
            return {
                "category": "Uncategorized",
                "confidence": 0,
                "matched_keywords": [],
                "all_scores": {},
            }

        top_category, details = ranked[0]

        max_score = max(v["score"] for _, v in ranked)

        confidence = ConfidenceCalculator.calculate(
            details["score"],
            max_score,
        )

        return {
            "category": top_category,
            "confidence": confidence,
            "matched_keywords": details["matches"],
            "all_scores": {
                category: value["score"]
                for category, value in ranked
            },
        }


# ==========================================================
# FREQUENCY ANALYZER
# ==========================================================

class CategoryFrequencyAnalyzer:

    def __init__(self):
        self.counter = Counter()

    def update(self, category: str):

        self.counter[category] += 1

    def update_many(
        self,
        categories: Iterable[str],
    ):

        self.counter.update(categories)

    def most_common(
        self,
        n: int = 20,
    ) -> List[Tuple[str, int]]:

        return self.counter.most_common(n)

    def as_dict(self) -> Dict[str, int]:

        return dict(self.counter)


# ==========================================================
# BULK CLASSIFIER
# ==========================================================

class BulkKeywordClassifier:

    def __init__(self):

        self.classifier = TicketClassifier()

    def classify_dataframe(
        self,
        df,
        subject_col: str = "Subject",
        description_col: str = "Description",
    ):

        categories = []
        confidences = []
        keywords = []

        for _, row in df.iterrows():

            subject = str(row.get(subject_col, ""))

            description = str(row.get(description_col, ""))

            result = self.classifier.classify(
                subject,
                description,
            )

            categories.append(result["category"])
            confidences.append(result["confidence"])
            keywords.append(", ".join(result["matched_keywords"]))

        df = df.copy()

        df["Predicted Category"] = categories
        df["Confidence"] = confidences
        df["Matched Keywords"] = keywords

        return df

    # ==========================================================
# PART 3
# RULE ENGINE + PRIORITY + ROOT CAUSE DETECTION
# ==========================================================

from dataclasses import dataclass
from typing import Dict, List, Optional


# ==========================================================
# PRIORITY RULES
# ==========================================================

PRIORITY_KEYWORDS = {

    "Critical": [
        "production down",
        "system down",
        "service unavailable",
        "outage",
        "cannot access",
        "all users",
        "security breach",
        "payment failed",
        "server error",
        "500 error",
    ],

    "High": [
        "urgent",
        "critical",
        "blocked",
        "cannot submit",
        "unable to use",
        "license expired",
        "login failed",
        "authentication",
        "timeout",
    ],

    "Medium": [
        "slow",
        "delay",
        "performance",
        "feature request",
        "enhancement",
        "improvement",
        "missing option",
    ],

    "Low": [
        "question",
        "clarification",
        "documentation",
        "feedback",
        "suggestion",
        "minor",
    ],
}


# ==========================================================
# ROOT CAUSE RULES
# ==========================================================

ROOT_CAUSE_RULES = {

    "Authentication": [
        "login",
        "password",
        "authentication",
        "signin",
        "otp",
        "access denied",
    ],

    "Licensing": [
        "license",
        "subscription",
        "expired",
        "renewal",
        "payment",
    ],

    "AI Configuration": [
        "rewrite with ai",
        "ask ai",
        "ai studio",
        "feature flag",
        "ai disabled",
    ],

    "Performance": [
        "slow",
        "lag",
        "timeout",
        "freeze",
        "loading",
    ],

    "Application Bug": [
        "bug",
        "error",
        "exception",
        "crash",
        "500",
        "unexpected",
    ],

    "Permission": [
        "permission",
        "role",
        "access",
        "admin",
        "authorization",
    ],

    "Citation Engine": [
        "citation",
        "apa",
        "mla",
        "harvard",
        "reference",
    ],

    "Grammar Engine": [
        "grammar",
        "rewrite",
        "suggestion",
        "editing",
    ],

    "Plagiarism Engine": [
        "plagiarism",
        "similarity",
        "duplicate",
    ],
}


# ==========================================================
# IMPACT DETECTION
# ==========================================================

IMPACT_KEYWORDS = {

    "Organization": [
        "everyone",
        "all users",
        "entire university",
        "whole organization",
        "institution",
        "campus",
    ],

    "Department": [
        "team",
        "department",
        "faculty",
        "group",
    ],

    "Single User": [
        "my account",
        "my login",
        "my profile",
        "i cannot",
        "personal",
    ],
}


# ==========================================================
# RULE RESULT
# ==========================================================

@dataclass
class RuleResult:

    priority: str
    impact: str
    probable_root_cause: str


# ==========================================================
# PRIORITY DETECTOR
# ==========================================================

class PriorityDetector:

    def predict(self, text: str) -> str:

        text = TextNormalizer.normalize(text)

        for level in ("Critical", "High", "Medium", "Low"):

            for keyword in PRIORITY_KEYWORDS[level]:

                if TextNormalizer.normalize(keyword) in text:
                    return level

        return "Medium"


# ==========================================================
# ROOT CAUSE DETECTOR
# ==========================================================

class RootCauseDetector:

    def detect(self, text: str) -> str:

        text = TextNormalizer.normalize(text)

        scores = {}

        for cause, keywords in ROOT_CAUSE_RULES.items():

            score = 0

            for keyword in keywords:

                keyword = TextNormalizer.normalize(keyword)

                if keyword in text:
                    score += 1

            scores[cause] = score

        best = max(scores, key=scores.get)

        if scores[best] == 0:
            return "Unknown"

        return best


# ==========================================================
# IMPACT DETECTOR
# ==========================================================

class ImpactDetector:

    def detect(self, text: str) -> str:

        text = TextNormalizer.normalize(text)

        scores = {}

        for impact, keywords in IMPACT_KEYWORDS.items():

            score = 0

            for keyword in keywords:

                if TextNormalizer.normalize(keyword) in text:
                    score += 1

            scores[impact] = score

        best = max(scores, key=scores.get)

        if scores[best] == 0:
            return "Single User"

        return best


# ==========================================================
# MASTER RULE ENGINE
# ==========================================================

class RuleEngine:

    def __init__(self):

        self.priority = PriorityDetector()
        self.root = RootCauseDetector()
        self.impact = ImpactDetector()

    def evaluate(
        self,
        subject: str,
        description: str,
    ) -> RuleResult:

        text = f"{subject} {description}"

        return RuleResult(
            priority=self.priority.predict(text),
            impact=self.impact.detect(text),
            probable_root_cause=self.root.detect(text),
        )


# ==========================================================
# ENRICH CLASSIFICATION
# ==========================================================

class EnhancedTicketClassifier(TicketClassifier):

    def __init__(self):

        super().__init__()

        self.rules = RuleEngine()

    def classify(
        self,
        subject: str,
        description: str,
    ) -> Dict:

        result = super().classify(
            subject,
            description,
        )

        rules = self.rules.evaluate(
            subject,
            description,
        )

        result["priority"] = rules.priority
        result["impact"] = rules.impact
        result["probable_root_cause"] = rules.probable_root_cause

        return result
    # ==========================================================
# PART 4
# DATAFRAME PIPELINE + TREND ANALYSIS + SUMMARY
# ==========================================================

import pandas as pd
from collections import Counter, defaultdict
from typing import Dict, List


# ==========================================================
# ANALYTICS ENGINE
# ==========================================================

class TicketAnalytics:

    def __init__(self):

        self.classifier = EnhancedTicketClassifier()

    # ------------------------------------------------------

    def process_dataframe(
        self,
        df: pd.DataFrame,
        subject_col: str = "Subject",
        description_col: str = "Description",
    ) -> pd.DataFrame:

        output = df.copy()

        categories = []
        confidence = []
        keywords = []
        priorities = []
        impacts = []
        root_causes = []

        for _, row in output.iterrows():

            subject = str(row.get(subject_col, ""))

            description = str(row.get(description_col, ""))

            result = self.classifier.classify(
                subject,
                description,
            )

            categories.append(result["category"])
            confidence.append(result["confidence"])
            keywords.append(", ".join(result["matched_keywords"]))
            priorities.append(result["priority"])
            impacts.append(result["impact"])
            root_causes.append(result["probable_root_cause"])

        output["Predicted Category"] = categories
        output["Confidence"] = confidence
        output["Matched Keywords"] = keywords
        output["Priority"] = priorities
        output["Impact"] = impacts
        output["Root Cause"] = root_causes

        return output


# ==========================================================
# SUMMARY ANALYTICS
# ==========================================================

class SummaryAnalyzer:

    @staticmethod
    def category_summary(df: pd.DataFrame):

        return (
            df["Predicted Category"]
            .value_counts()
            .rename_axis("Category")
            .reset_index(name="Tickets")
        )

    # ------------------------------------------------------

    @staticmethod
    def priority_summary(df: pd.DataFrame):

        return (
            df["Priority"]
            .value_counts()
            .rename_axis("Priority")
            .reset_index(name="Tickets")
        )

    # ------------------------------------------------------

    @staticmethod
    def root_cause_summary(df: pd.DataFrame):

        return (
            df["Root Cause"]
            .value_counts()
            .rename_axis("Root Cause")
            .reset_index(name="Tickets")
        )

    # ------------------------------------------------------

    @staticmethod
    def impact_summary(df: pd.DataFrame):

        return (
            df["Impact"]
            .value_counts()
            .rename_axis("Impact")
            .reset_index(name="Tickets")
        )


# ==========================================================
# TREND ANALYZER
# ==========================================================

class TrendAnalyzer:

    @staticmethod
    def monthly_ticket_trend(
        df: pd.DataFrame,
        date_column: str = "Created At",
    ):

        data = df.copy()

        data[date_column] = pd.to_datetime(
            data[date_column],
            errors="coerce",
        )

        data["Month"] = data[date_column].dt.to_period("M")

        return (
            data.groupby("Month")
            .size()
            .reset_index(name="Tickets")
        )

    # ------------------------------------------------------

    @staticmethod
    def monthly_category_trend(
        df: pd.DataFrame,
        date_column="Created At",
    ):

        data = df.copy()

        data[date_column] = pd.to_datetime(
            data[date_column],
            errors="coerce",
        )

        data["Month"] = data[date_column].dt.to_period("M")

        pivot = pd.pivot_table(
            data,
            index="Month",
            columns="Predicted Category",
            aggfunc="size",
            fill_value=0,
        )

        return pivot.reset_index()


# ==========================================================
# RECURRING ISSUE DETECTOR
# ==========================================================

class RecurringIssueDetector:

    @staticmethod
    def recurring_keywords(df):

        counter = Counter()

        for value in df["Matched Keywords"]:

            if pd.isna(value):
                continue

            for word in str(value).split(","):

                word = word.strip()

                if word:
                    counter[word] += 1

        recurring = pd.DataFrame(
            counter.items(),
            columns=["Keyword", "Frequency"],
        )

        recurring = recurring.sort_values(
            "Frequency",
            ascending=False,
        )

        return recurring

    # ------------------------------------------------------

    @staticmethod
    def recurring_categories(df):

        return (
            df["Predicted Category"]
            .value_counts()
            .rename_axis("Category")
            .reset_index(name="Frequency")
        )


# ==========================================================
# CUSTOMER LEVEL ANALYTICS
# ==========================================================

class CustomerAnalytics:

    @staticmethod
    def tickets_per_customer(
        df,
        customer_column="Company",
    ):

        return (
            df.groupby(customer_column)
            .size()
            .reset_index(name="Tickets")
            .sort_values(
                "Tickets",
                ascending=False,
            )
        )

    # ------------------------------------------------------

    @staticmethod
    def category_per_customer(
        df,
        customer_column="Company",
    ):

        return pd.crosstab(
            df[customer_column],
            df["Predicted Category"],
        )

    # ------------------------------------------------------

    @staticmethod
    def priority_per_customer(
        df,
        customer_column="Company",
    ):

        return pd.crosstab(
            df[customer_column],
            df["Priority"],
        )


# ==========================================================
# EXECUTIVE DASHBOARD DATA
# ==========================================================

class ExecutiveDashboard:

    @staticmethod
    def build(df):

        dashboard = {}

        dashboard["Total Tickets"] = len(df)

        dashboard["Average Confidence"] = round(
            df["Confidence"].mean(),
            2,
        )

        dashboard["Critical Tickets"] = len(
            df[df["Priority"] == "Critical"]
        )

        dashboard["High Priority Tickets"] = len(
            df[df["Priority"] == "High"]
        )

        dashboard["Unique Categories"] = (
            df["Predicted Category"]
            .nunique()
        )

        dashboard["Top Category"] = (
            df["Predicted Category"]
            .value_counts()
            .idxmax()
        )

        dashboard["Top Root Cause"] = (
            df["Root Cause"]
            .value_counts()
            .idxmax()
        )

        dashboard["Top Impact"] = (
            df["Impact"]
            .value_counts()
            .idxmax()
        )

        return dashboard

    # ==========================================================
# PART 5
# EXPORT ENGINE + REPORT GENERATION + MAIN PIPELINE
# ==========================================================

import os
from datetime import datetime
import pandas as pd


# ==========================================================
# EXPORT ENGINE
# ==========================================================

class ExportEngine:

    @staticmethod
    def export_excel(
        processed_df: pd.DataFrame,
        output_file: str = "Freshdesk_AI_Analytics.xlsx",
    ):

        category_summary = SummaryAnalyzer.category_summary(processed_df)
        priority_summary = SummaryAnalyzer.priority_summary(processed_df)
        root_summary = SummaryAnalyzer.root_cause_summary(processed_df)
        impact_summary = SummaryAnalyzer.impact_summary(processed_df)

        recurring_keywords = (
            RecurringIssueDetector.recurring_keywords(processed_df)
        )

        recurring_categories = (
            RecurringIssueDetector.recurring_categories(processed_df)
        )

        customer_summary = (
            CustomerAnalytics.tickets_per_customer(processed_df)
            if "Company" in processed_df.columns
            else pd.DataFrame()
        )

        from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

        processed_df = processed_df.copy()

        MAX_EXCEL_CELL = 32767

        for column in processed_df.columns:

            processed_df[column] = processed_df[column].apply(

                lambda x: (
                    ILLEGAL_CHARACTERS_RE.sub("", x)[:MAX_EXCEL_CELL]
                    if isinstance(x, str)
                    else x
                )

            )

        with pd.ExcelWriter(
            output_file,
            engine="openpyxl",
        ) as writer:

            processed_df.to_excel(
                writer,
                sheet_name="Processed Tickets",
                index=False,
            )

            category_summary.to_excel(
                writer,
                sheet_name="Category Summary",
                index=False,
            )

            priority_summary.to_excel(
                writer,
                sheet_name="Priority Summary",
                index=False,
            )

            root_summary.to_excel(
                writer,
                sheet_name="Root Cause Summary",
                index=False,
            )

            impact_summary.to_excel(
                writer,
                sheet_name="Impact Summary",
                index=False,
            )

            recurring_keywords.to_excel(
                writer,
                sheet_name="Recurring Keywords",
                index=False,
            )

            recurring_categories.to_excel(
                writer,
                sheet_name="Recurring Categories",
                index=False,
            )

            if not customer_summary.empty:

                customer_summary.to_excel(
                    writer,
                    sheet_name="Customer Summary",
                    index=False,
                )

        return output_file

# ==========================================================
# REPORT GENERATOR
# ==========================================================

class ExecutiveReport:

    @staticmethod
    def generate(df):

        dashboard = ExecutiveDashboard.build(df)

        report = []

        report.append("=" * 70)
        report.append("FRESHDESK AI ANALYTICS REPORT")
        report.append("=" * 70)

        report.append(
            f"Generated : {datetime.now().strftime('%d-%b-%Y %H:%M')}"
        )

        report.append("")
        report.append(f"Total Tickets          : {dashboard['Total Tickets']}")
        report.append(f"Critical Tickets       : {dashboard['Critical Tickets']}")
        report.append(f"High Priority Tickets  : {dashboard['High Priority Tickets']}")
        report.append(f"Top Category           : {dashboard['Top Category']}")
        report.append(f"Top Root Cause         : {dashboard['Top Root Cause']}")
        report.append(f"Top Impact             : {dashboard['Top Impact']}")
        report.append(f"Average Confidence     : {dashboard['Average Confidence']} %")

        report.append("")
        report.append("=" * 70)

        return "\n".join(report)

    @staticmethod
    def save(report_text, filename="Executive_Report.txt"):

        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_text)

        return filename


# ==========================================================
# MAIN PIPELINE
# ==========================================================

class FreshdeskAnalyticsPipeline:

    def __init__(self):

        self.analytics = TicketAnalytics()

    def run(
        self,
        input_file,
        output_excel="Freshdesk_AI_Analytics.xlsx",
    ):

        print("=" * 70)
        print("Loading dataset...")
        print("=" * 70)

        df = pd.read_csv(input_file)

        print(f"Loaded {len(df)} tickets")

        processed = self.analytics.process_dataframe(df)

        print("Classification Complete")

        ExportEngine.export_excel(
            processed,
            output_excel,
        )

        report = ExecutiveReport.generate(processed)

        ExecutiveReport.save(report)

        print("")
        print(report)
        print("")
        print(f"Excel Report : {output_excel}")
        print("Executive_Report.txt generated")

        return processed


# ==========================================================
# COMMAND LINE EXECUTION
# ==========================================================


   

        # ==========================================================
# PART 6
# HYBRID MACHINE LEARNING CLASSIFIER
# TF-IDF + Naive Bayes + Rule Engine
# ==========================================================

from typing import List, Dict
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


# ==========================================================
# ML CLASSIFIER
# ==========================================================

class TicketMLClassifier:

    def __init__(self):

        self.pipeline = Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        stop_words="english",
                        ngram_range=(1,2),
                        min_df=2
                    )
                ),
                (
                    "classifier",
                    MultinomialNB()
                )
            ]
        )

        self.is_trained = False

    # ------------------------------------------------------

    def train(
        self,
        dataframe: pd.DataFrame,
        text_column="Combined Text",
        label_column="Predicted Category"
    ):

        data = dataframe.copy()

        X = data[text_column]

        y = data[label_column]

        self.pipeline.fit(X, y)

        self.is_trained = True

    # ------------------------------------------------------

    def predict(
        self,
        text: str
    ):

        if not self.is_trained:
            raise RuntimeError("ML model has not been trained.")

        return self.pipeline.predict([text])[0]

    # ------------------------------------------------------

    def predict_probability(
        self,
        text: str
    ):

        if not self.is_trained:
            raise RuntimeError("ML model has not been trained.")

        probabilities = self.pipeline.predict_proba([text])[0]

        labels = self.pipeline.classes_

        return dict(zip(labels, probabilities))

    # ------------------------------------------------------

    def evaluate(
        self,
        dataframe,
        text_column="Combined Text",
        label_column="Predicted Category"
    ):

        data = dataframe.copy()

        X_train, X_test, y_train, y_test = train_test_split(
            data[text_column],
            data[label_column],
            test_size=0.20,
            random_state=42
        )

        self.pipeline.fit(X_train, y_train)

        predictions = self.pipeline.predict(X_test)

        print("="*60)
        print("MODEL ACCURACY")
        print("="*60)

        print(
            accuracy_score(
                y_test,
                predictions
            )
        )

        print()

        print(classification_report(
            y_test,
            predictions
        ))

        return confusion_matrix(
            y_test,
            predictions
        )


# ==========================================================
# HYBRID CLASSIFIER
# ==========================================================

class HybridClassifier:

    def __init__(self):

        self.rule_engine = EnhancedTicketClassifier()

        self.ml_engine = TicketMLClassifier()

    # ------------------------------------------------------

    def train(
        self,
        dataframe
    ):

        data = dataframe.copy()

        data["Combined Text"] = (
            data["Subject"].fillna("")
            + " "
            + data["Description"].fillna("")
        )

        self.ml_engine.train(data)

    # ------------------------------------------------------

    def classify(
        self,
        subject,
        description
    ):

        text = subject + " " + description

        # ---------------------------
        # Rule Engine
        # ---------------------------

        rule_prediction = self.rule_engine.classify(
            subject,
            description
        )

        # ---------------------------
        # ML Prediction
        # ---------------------------

        if self.ml_engine.is_trained:

            ml_prediction = self.ml_engine.predict(text)

            probabilities = self.ml_engine.predict_probability(text)

            ml_confidence = max(
                probabilities.values()
            ) * 100

        else:

            ml_prediction = None

            ml_confidence = 0

        # ---------------------------
        # Decision Logic
        # ---------------------------

        final_category = rule_prediction["category"]

        final_confidence = rule_prediction["confidence"]

        decision_source = "Rule Engine"

        if ml_prediction:

            if (
                ml_prediction != rule_prediction["category"]
                and
                ml_confidence > 80
            ):

                final_category = ml_prediction

                final_confidence = round(
                    ml_confidence,
                    2
                )

                decision_source = "Machine Learning"

        result = dict(rule_prediction)

        result["ml_prediction"] = ml_prediction

        result["final_category"] = final_category

        result["final_confidence"] = final_confidence

        result["decision_source"] = decision_source

        return result


# ==========================================================
# BULK ML CLASSIFICATION
# ==========================================================

class BulkHybridClassifier:

    def __init__(self):

        self.engine = HybridClassifier()

    def train(self, dataframe):

        self.engine.train(dataframe)

    def classify_dataframe(self, dataframe):

        data = dataframe.copy()

        final_category = []

        final_confidence = []

        decision_source = []

        ml_prediction = []

        for _, row in data.iterrows():

            result = self.engine.classify(
                str(row.get("Subject","")),
                str(row.get("Description",""))
            )

            final_category.append(
                result["final_category"]
            )

            final_confidence.append(
                result["final_confidence"]
            )

            decision_source.append(
                result["decision_source"]
            )

            ml_prediction.append(
                result["ml_prediction"]
            )

        data["Final Category"] = final_category

        data["Final Confidence"] = final_confidence

        data["ML Prediction"] = ml_prediction

        data["Decision Source"] = decision_source

        return data
    # ==========================================================
# PART 7
# DUPLICATE TICKET DETECTION & TICKET CLUSTERING
# Version 5.0
# ==========================================================

from collections import defaultdict
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans


# ==========================================================
# DUPLICATE DETECTOR
# ==========================================================

class DuplicateTicketDetector:

    def __init__(
        self,
        similarity_threshold=0.85
    ):

        self.similarity_threshold = similarity_threshold

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1,2)
        )

    # ------------------------------------------------------

    def find_duplicates(
        self,
        dataframe,
        subject_column="Subject",
        description_column="Description"
    ):

        df = dataframe.copy()

        df["Combined Text"] = (
            df[subject_column].fillna("")
            + " "
            + df[description_column].fillna("")
        )

        tfidf = self.vectorizer.fit_transform(
            df["Combined Text"]
        )

        similarity = cosine_similarity(tfidf)

        duplicate_pairs = []

        for i in range(len(df)):

            for j in range(i + 1, len(df)):

                score = similarity[i][j]

                if score >= self.similarity_threshold:

                    duplicate_pairs.append({

                        "Ticket 1": i,

                        "Ticket 2": j,

                        "Similarity": round(score,4)

                    })

        return pd.DataFrame(duplicate_pairs)


# ==========================================================
# TICKET CLUSTERING
# ==========================================================

class TicketClusterer:

    def __init__(
        self,
        clusters=10
    ):

        self.clusters = clusters

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1,2)
        )

    # ------------------------------------------------------

    def cluster(
        self,
        dataframe,
        subject_column="Subject",
        description_column="Description"
    ):

        df = dataframe.copy()

        df["Combined Text"] = (

            df[subject_column].fillna("")
            + " "
            + df[description_column].fillna("")

        )

        vectors = self.vectorizer.fit_transform(

            df["Combined Text"]

        )

        model = KMeans(

            n_clusters=self.clusters,

            random_state=42,

            n_init=20

        )

        df["Cluster"] = model.fit_predict(vectors)

        return df


# ==========================================================
# CLUSTER SUMMARY
# ==========================================================

class ClusterAnalyzer:

    @staticmethod
    def summary(dataframe):

        return (

            dataframe.groupby("Cluster")

            .size()

            .reset_index(name="Tickets")

            .sort_values(

                "Tickets",

                ascending=False

            )

        )


# ==========================================================
# CLUSTER KEYWORDS
# ==========================================================

class ClusterKeywordAnalyzer:

    @staticmethod
    def top_keywords(
        dataframe,
        top_n=10
    ):

        cluster_keywords = {}

        for cluster in sorted(

            dataframe["Cluster"].unique()

        ):

            subset = dataframe[

                dataframe["Cluster"] == cluster

            ]

            vectorizer = TfidfVectorizer(

                stop_words="english",

                max_features=top_n

            )

            matrix = vectorizer.fit_transform(

                subset["Combined Text"]

            )

            words = vectorizer.get_feature_names_out()

            scores = matrix.sum(axis=0).A1

            ranked = sorted(

                zip(words,scores),

                key=lambda x:x[1],

                reverse=True

            )

            cluster_keywords[cluster] = [

                word for word,_ in ranked

            ]

        return cluster_keywords


# ==========================================================
# INCIDENT DETECTOR
# ==========================================================

class IncidentDetector:

    def __init__(

        self,

        similarity_threshold=0.80,

        minimum_occurrence=5

    ):

        self.similarity_threshold = similarity_threshold

        self.minimum_occurrence = minimum_occurrence

    # ------------------------------------------------------

    def detect(

        self,

        clustered_dataframe

    ):

        incidents = []

        grouped = (

            clustered_dataframe

            .groupby("Cluster")

            .size()

        )

        for cluster,count in grouped.items():

            if count >= self.minimum_occurrence:

                incidents.append({

                    "Cluster":cluster,

                    "Tickets":count,

                    "Possible Incident":"Yes"

                })

        return pd.DataFrame(incidents)


# ==========================================================
# DUPLICATE MERGE SUGGESTIONS
# ==========================================================

class DuplicateMergeAdvisor:

    @staticmethod
    def recommend(

        duplicate_dataframe

    ):

        recommendations = []

        for _,row in duplicate_dataframe.iterrows():

            recommendations.append({

                "Primary Ticket":row["Ticket 1"],

                "Duplicate Ticket":row["Ticket 2"],

                "Similarity":row["Similarity"],

                "Recommendation":"Merge"

            })

        return pd.DataFrame(

            recommendations

        )


# ==========================================================
# KNOWLEDGE BASE OPPORTUNITY DETECTOR
# ==========================================================

class KnowledgeBaseOpportunity:

    @staticmethod
    def identify(

        clustered_dataframe,

        minimum_ticket_count=10

    ):

        summary = (

            clustered_dataframe

            .groupby("Cluster")

            .size()

            .reset_index(name="Tickets")

        )

        summary["Create KB Article"] = (

            summary["Tickets"]

            >= minimum_ticket_count

        )

        return summary


# ==========================================================
# ROOT CAUSE TREND ANALYZER
# ==========================================================

class RootCauseTrendAnalyzer:

    @staticmethod
    def recurring_root_causes(dataframe):

        return (

            dataframe["Root Cause"]

            .value_counts()

            .reset_index()

            .rename(

                columns={

                    "index":"Root Cause",

                    "Root Cause":"Tickets"

                }

            )

        )
    # ==========================================================
# PART 8
# SLA PREDICTION + RESOLUTION ANALYTICS + CUSTOMER HEALTH
# Version 5.0
# ==========================================================

import pandas as pd
import numpy as np
from datetime import datetime


# ==========================================================
# SLA CONFIGURATION
# ==========================================================

SLA_RULES = {

    "Critical": 4,      # hours

    "High": 8,

    "Medium": 24,

    "Low": 48

}


# ==========================================================
# SLA ANALYZER
# ==========================================================

class SLAAnalyzer:

    @staticmethod
    def calculate_resolution_time(
        dataframe,
        created_column="Created At",
        resolved_column="Resolved At"
    ):

        df = dataframe.copy()

        df[created_column] = pd.to_datetime(
            df[created_column],
            errors="coerce"
        )

        df[resolved_column] = pd.to_datetime(
            df[resolved_column],
            errors="coerce"
        )

        df["Resolution Hours"] = (

            df[resolved_column] -
            df[created_column]

        ).dt.total_seconds() / 3600

        return df

    # ------------------------------------------------------

    @staticmethod
    def assign_sla(dataframe):

        df = dataframe.copy()

        df["SLA Target"] = (

            df["Priority"]

            .map(SLA_RULES)

        )

        return df

    # ------------------------------------------------------

    @staticmethod
    def sla_status(dataframe):

        df = SLAAnalyzer.assign_sla(dataframe)

        df["SLA Met"] = (

            df["Resolution Hours"]

            <=

            df["SLA Target"]

        )

        return df


# ==========================================================
# RESOLUTION ANALYTICS
# ==========================================================

class ResolutionAnalytics:

    @staticmethod
    def average_resolution_time(dataframe):

        return round(

            dataframe["Resolution Hours"]

            .mean(),

            2

        )

    # ------------------------------------------------------

    @staticmethod
    def resolution_by_priority(dataframe):

        return (

            dataframe

            .groupby("Priority")["Resolution Hours"]

            .mean()

            .reset_index()

        )

    # ------------------------------------------------------

    @staticmethod
    def resolution_by_category(dataframe):

        return (

            dataframe

            .groupby("Predicted Category")["Resolution Hours"]

            .mean()

            .reset_index()

        )

    # ------------------------------------------------------

    @staticmethod
    def sla_summary(dataframe):

        return (

            dataframe["SLA Met"]

            .value_counts()

            .reset_index()

            .rename(

                columns={

                    "index":"SLA",

                    "SLA Met":"Tickets"

                }

            )

        )


# ==========================================================
# CUSTOMER HEALTH SCORING
# ==========================================================

class CustomerHealthScorer:

    def score(self,dataframe):

        health = []

        grouped = dataframe.groupby("Company")

        for company,data in grouped:

            score = 100

            tickets = len(data)

            critical = len(

                data[data["Priority"]=="Critical"]

            )

            high = len(

                data[data["Priority"]=="High"]

            )

            avg_resolution = (

                data["Resolution Hours"]

                .mean()

            )

            sla_breach = len(

                data[data["SLA Met"]==False]

            )

            score -= tickets * 0.5

            score -= critical * 10

            score -= high * 5

            score -= sla_breach * 4

            if avg_resolution > 24:

                score -= 10

            score = max(0,min(100,round(score)))

            health.append({

                "Company":company,

                "Health Score":score,

                "Tickets":tickets,

                "Critical Tickets":critical,

                "High Tickets":high,

                "Avg Resolution Hours":round(

                    avg_resolution,

                    2

                ),

                "SLA Breaches":sla_breach

            })

        return pd.DataFrame(health)


# ==========================================================
# CUSTOMER RISK CLASSIFIER
# ==========================================================

class CustomerRiskClassifier:

    @staticmethod
    def classify(score):

        if score >= 85:

            return "Healthy"

        elif score >= 70:

            return "Monitor"

        elif score >= 50:

            return "At Risk"

        else:

            return "Critical"

    # ------------------------------------------------------

    @staticmethod
    def apply(dataframe):

        df = dataframe.copy()

        df["Customer Status"] = (

            df["Health Score"]

            .apply(

                CustomerRiskClassifier.classify

            )

        )

        return df


# ==========================================================
# ESCALATION ADVISOR
# ==========================================================

class EscalationAdvisor:

    @staticmethod
    def recommend(dataframe):

        recommendations = []

        for _,row in dataframe.iterrows():

            if row["Priority"]=="Critical":

                recommendations.append(

                    "Immediate Engineering Escalation"

                )

            elif row["Priority"]=="High":

                recommendations.append(

                    "Escalate within 2 Hours"

                )

            elif row["SLA Met"]==False:

                recommendations.append(

                    "Review SLA Breach"

                )

            else:

                recommendations.append(

                    "Standard Support"

                )

        dataframe = dataframe.copy()

        dataframe["Recommendation"] = recommendations

        return dataframe


# ==========================================================
# EXECUTIVE KPI GENERATOR
# ==========================================================

class KPIBuilder:

    @staticmethod
    def generate(dataframe):

        kpis = {}

        kpis["Average Resolution Hours"] = round(

            dataframe["Resolution Hours"]

            .mean(),

            2

        )

        kpis["Median Resolution Hours"] = round(

            dataframe["Resolution Hours"]

            .median(),

            2

        )

        kpis["SLA Achievement %"] = round(

            dataframe["SLA Met"]

            .mean()

            *100,

            2

        )

        kpis["Critical Ticket %"] = round(

            len(

                dataframe[

                    dataframe["Priority"]=="Critical"

                ]

            )

            /

            len(dataframe)

            *100,

            2

        )

        return kpis
    # ==========================================================
# PART 9
# DASHBOARD DATA ENGINE + PLOTLY VISUALIZATIONS
# Version 5.0
# ==========================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ==========================================================
# DASHBOARD DATA BUILDER
# ==========================================================

class DashboardDataBuilder:

    @staticmethod
    def build(df):

        dashboard = {}

        dashboard["category"] = (
            df["Predicted Category"]
            .value_counts()
            .reset_index()
            .rename(columns={
                "index":"Category",
                "Predicted Category":"Tickets"
            })
        )

        dashboard["priority"] = (
            df["Priority"]
            .value_counts()
            .reset_index()
            .rename(columns={
                "index":"Priority",
                "Priority":"Tickets"
            })
        )

        dashboard["root"] = (
            df["Root Cause"]
            .value_counts()
            .reset_index()
            .rename(columns={
                "index":"Root Cause",
                "Root Cause":"Tickets"
            })
        )

        dashboard["impact"] = (
            df["Impact"]
            .value_counts()
            .reset_index()
            .rename(columns={
                "index":"Impact",
                "Impact":"Tickets"
            })
        )

        return dashboard


# ==========================================================
# EXECUTIVE DASHBOARD
# ==========================================================

class DashboardVisualizer:

    # ------------------------------------------------------

    @staticmethod
    def category_chart(df):

        fig = px.bar(
            df,
            x="Category",
            y="Tickets",
            title="Tickets by Category"
        )

        return fig

    # ------------------------------------------------------

    @staticmethod
    def priority_chart(df):

        fig = px.pie(
            df,
            names="Priority",
            values="Tickets",
            title="Priority Distribution"
        )

        return fig

    # ------------------------------------------------------

    @staticmethod
    def root_cause_chart(df):

        fig = px.bar(
            df,
            x="Root Cause",
            y="Tickets",
            title="Root Cause Analysis"
        )

        return fig

    # ------------------------------------------------------

    @staticmethod
    def impact_chart(df):

        fig = px.bar(
            df,
            x="Impact",
            y="Tickets",
            title="Impact Distribution"
        )

        return fig


# ==========================================================
# SLA DASHBOARD
# ==========================================================

class SLADashboard:

    @staticmethod
    def resolution_chart(df):

        fig = px.box(
            df,
            x="Priority",
            y="Resolution Hours",
            title="Resolution Time by Priority"
        )

        return fig

    # ------------------------------------------------------

    @staticmethod
    def sla_chart(df):

        summary = (
            df["SLA Met"]
            .value_counts()
            .reset_index()
        )

        summary.columns = [
            "SLA",
            "Tickets"
        ]

        fig = px.pie(
            summary,
            names="SLA",
            values="Tickets",
            title="SLA Compliance"
        )

        return fig


# ==========================================================
# CUSTOMER DASHBOARD
# ==========================================================

class CustomerDashboard:

    @staticmethod
    def health_chart(df):

        fig = px.bar(
            df,
            x="Company",
            y="Health Score",
            color="Customer Status",
            title="Customer Health Score"
        )

        return fig

    # ------------------------------------------------------

    @staticmethod
    def ticket_volume(df):

        summary = (
            df.groupby("Company")
            .size()
            .reset_index(name="Tickets")
        )

        fig = px.bar(
            summary,
            x="Company",
            y="Tickets",
            title="Tickets per Customer"
        )

        return fig


# ==========================================================
# TREND DASHBOARD
# ==========================================================

class TrendDashboard:

    @staticmethod
    def monthly_trend(df):

        trend = TrendAnalyzer.monthly_ticket_trend(df)

        fig = px.line(
            trend,
            x="Month",
            y="Tickets",
            markers=True,
            title="Monthly Ticket Trend"
        )

        return fig

    # ------------------------------------------------------

    @staticmethod
    def category_trend(df):

        pivot = TrendAnalyzer.monthly_category_trend(df)

        fig = go.Figure()

        for column in pivot.columns[1:]:

            fig.add_trace(

                go.Scatter(

                    x=pivot["Month"].astype(str),

                    y=pivot[column],

                    mode="lines+markers",

                    name=column

                )

            )

        fig.update_layout(

            title="Monthly Category Trend"

        )

        return fig


# ==========================================================
# EXECUTIVE KPI DASHBOARD
# ==========================================================

class ExecutiveKPIDashboard:

    @staticmethod
    def create(kpis):

        fig = make_subplots(
            rows=2,
            cols=2,
            specs=[
                [{"type":"indicator"},{"type":"indicator"}],
                [{"type":"indicator"},{"type":"indicator"}]
            ]
        )

        names = list(kpis.keys())
        values = list(kpis.values())

        positions = [
            (1,1),
            (1,2),
            (2,1),
            (2,2)
        ]

        for i in range(min(4, len(values))):

            row,col = positions[i]

            fig.add_trace(

                go.Indicator(

                    mode="number",

                    value=values[i],

                    title={"text":names[i]}

                ),

                row=row,

                col=col

            )

        fig.update_layout(

            title="Executive KPI Dashboard",

            height=700

        )

        return fig


# ==========================================================
# EXPORT DASHBOARD
# ==========================================================

class DashboardExporter:

    @staticmethod
    def export_html(

        figure,

        filename

    ):

        figure.write_html(filename)

    # ------------------------------------------------------

    @staticmethod
    def export_all(

        dashboard,

        processed_df,

        customer_health,

        kpis

    ):

        DashboardExporter.export_html(

            DashboardVisualizer.category_chart(

                dashboard["category"]

            ),

            "category_dashboard.html"

        )

        DashboardExporter.export_html(

            DashboardVisualizer.priority_chart(

                dashboard["priority"]

            ),

            "priority_dashboard.html"

        )

        DashboardExporter.export_html(

            DashboardVisualizer.root_cause_chart(

                dashboard["root"]

            ),

            "rootcause_dashboard.html"

        )

        DashboardExporter.export_html(

            DashboardVisualizer.impact_chart(

                dashboard["impact"]

            ),

            "impact_dashboard.html"

        )

        DashboardExporter.export_html(

            SLADashboard.resolution_chart(

                processed_df

            ),

            "resolution_dashboard.html"

        )

        DashboardExporter.export_html(

            SLADashboard.sla_chart(

                processed_df

            ),

            "sla_dashboard.html"

        )

        DashboardExporter.export_html(

            CustomerDashboard.health_chart(

                customer_health

            ),

            "customer_health_dashboard.html"

        )

        DashboardExporter.export_html(

            TrendDashboard.monthly_trend(

                processed_df

            ),

            "monthly_trend_dashboard.html"

        )

        DashboardExporter.export_html(

            ExecutiveKPIDashboard.create(

                kpis

            ),

            "executive_kpi_dashboard.html"

        )

        print("=" * 60)
        print("Dashboard HTML files generated successfully.")
        print("=" * 60)

        # ==========================================================
# PART 10
# CONFIGURATION + LOGGING + VALIDATION + PERFORMANCE
# Version 5.0 FINAL
# ==========================================================

import logging
import json
import os
import time
from pathlib import Path
from functools import wraps


# ==========================================================
# GLOBAL CONFIGURATION
# ==========================================================

class Config:

    VERSION = "5.0"

    RANDOM_STATE = 42

    DEFAULT_SIMILARITY = 0.85

    DEFAULT_CLUSTER_COUNT = 10

    DEFAULT_CONFIDENCE = 80

    LOG_FILE = "analytics.log"

    OUTPUT_FOLDER = "output"

    REPORT_FOLDER = "reports"

    DASHBOARD_FOLDER = "dashboards"

    EXPORT_EXCEL = "Freshdesk_AI_Analytics.xlsx"

    EXECUTIVE_REPORT = "Executive_Report.txt"

    CREATE_FOLDERS = True


# ==========================================================
# LOGGER
# ==========================================================

class Logger:

    @staticmethod
    def configure():

        logging.basicConfig(

            filename=Config.LOG_FILE,

            level=logging.INFO,

            format="%(asctime)s | %(levelname)s | %(message)s"

        )

        logging.info("=" * 60)
        logging.info("Freshdesk Analytics Started")
        logging.info("=" * 60)


# ==========================================================
# PERFORMANCE TIMER
# ==========================================================

def timer(func):

    @wraps(func)

    def wrapper(*args, **kwargs):

        start = time.time()

        result = func(*args, **kwargs)

        elapsed = round(time.time() - start, 2)

        logging.info(

            f"{func.__name__} executed in {elapsed} seconds"

        )

        print(

            f"{func.__name__:<35} {elapsed} sec"

        )

        return result

    return wrapper


# ==========================================================
# DIRECTORY MANAGER
# ==========================================================

class DirectoryManager:

    @staticmethod
    def create():

        if not Config.CREATE_FOLDERS:
            return

        folders = [

            Config.OUTPUT_FOLDER,

            Config.REPORT_FOLDER,

            Config.DASHBOARD_FOLDER

        ]

        for folder in folders:

            Path(folder).mkdir(

                parents=True,

                exist_ok=True

            )


# ==========================================================
# INPUT VALIDATION
# ==========================================================

class InputValidator:

    REQUIRED_COLUMNS = [

        "Subject",

        "Description"

    ]

    @staticmethod
    def validate(df):

        missing = [

            col

            for col in InputValidator.REQUIRED_COLUMNS

            if col not in df.columns

        ]

        if missing:

            raise ValueError(

                f"Missing columns: {missing}"

            )

        return True


# ==========================================================
# DATA QUALITY CHECKS
# ==========================================================

class DataQuality:

    @staticmethod
    def report(df):

        report = {}

        report["Rows"] = len(df)

        report["Columns"] = len(df.columns)

        report["Duplicate Rows"] = df.duplicated().sum()

        report["Null Values"] = (

            df.isnull()

            .sum()

            .to_dict()

        )

        report["Memory MB"] = round(

            df.memory_usage(deep=True)

            .sum()

            /1024/1024,

            2

        )

        return report


# ==========================================================
# JSON EXPORTER
# ==========================================================

class JSONExporter:

    @staticmethod
    def save(

        dictionary,

        filename="summary.json"

    ):

        with open(

            filename,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                dictionary,

                f,

                indent=4,

                default=str

            )


# ==========================================================
# MODEL INFORMATION
# ==========================================================

class ModelInformation:

    @staticmethod
    def metadata():

        return {

            "Version":Config.VERSION,

            "Keyword Categories":len(CATEGORY_KEYWORDS),

            "Similarity Threshold":Config.DEFAULT_SIMILARITY,

            "Clusters":Config.DEFAULT_CLUSTER_COUNT,

            "Random State":Config.RANDOM_STATE,

            "ML":"TF-IDF + Multinomial Naive Bayes",

            "Rule Engine":"Enabled",

            "Duplicate Detection":"Enabled",

            "Customer Health":"Enabled",

            "Dashboard":"Plotly",

            "Export":"Excel + HTML + JSON"

        }


# ==========================================================
# SYSTEM SUMMARY
# ==========================================================

class SystemSummary:

    @staticmethod
    def print():

        print()

        print("="*70)

        print("FRESHDESK AI ANALYTICS ENGINE")

        print("="*70)

        metadata = ModelInformation.metadata()

        for key,value in metadata.items():

            print(f"{key:<25}: {value}")

        print("="*70)


# ==========================================================
# FINAL ENGINE
# ==========================================================

class AnalyticsEngine:

    def __init__(self):

        Logger.configure()

        DirectoryManager.create()

        SystemSummary.print()

    @timer
    def run(

        self,

        input_file

    ):

        print()

        print("Loading dataset...")

        df = pd.read_csv(input_file)

        InputValidator.validate(df)

        quality = DataQuality.report(df)

        JSONExporter.save(

            quality,

            "data_quality.json"

        )

        print()

        print("Data Quality Report")

        print("-"*40)

        for k,v in quality.items():

            print(f"{k:<20}: {v}")

        print()

        pipeline = FreshdeskAnalyticsPipeline()

        processed = pipeline.run(

            input_file

        )

        metadata = ModelInformation.metadata()

        JSONExporter.save(

            metadata,

            "model_metadata.json"

        )

        logging.info(

            "Analytics Completed Successfully"

        )

        print()

        print("="*70)

        print("SYSTEM COMPLETED SUCCESSFULLY")

        print("="*70)

        print("Excel Report           : Generated")

        print("Executive Report       : Generated")

        print("Dashboard HTML         : Generated")

        print("Model Metadata JSON    : Generated")

        print("Data Quality JSON      : Generated")

        print("="*70)

        return processed


# ==========================================================
# ENTRY POINT
# ==========================================================
def get_input_file():

    csv_files = sorted(INPUT_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV file found in:\n{INPUT_DIR}"
        )

    return csv_files[0]
if __name__ == "__main__":

    try:

        input_file = get_input_file()

        print("=" * 60)
        print("INPUT FILE FOUND")
        print("=" * 60)
        print(input_file.name)
        print("=" * 60)

        engine = AnalyticsEngine()
        engine.run(str(input_file))

    except Exception:

        import traceback

        print("=" * 60)
        print("ERROR")
        print("=" * 60)

        traceback.print_exc()

        print("=" * 60)