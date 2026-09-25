"""
Master taxonomy used across the project.
Everything classifies into these dimensions.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class TicketClassification:

    # Existing
    category: str
    subcategory: str

    # New
    intent: str
    journey_stage: str
    product_area: str
    feature: str
    root_cause: str
    owner_team: str
    preventability: str
    engineering_required: bool
    confidence: float

    matched_keywords: List[str]
    matched_rules: List[str]