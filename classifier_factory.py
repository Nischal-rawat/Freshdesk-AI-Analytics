"""
Classifier Factory

Returns the active classifier based on configuration.
"""

from config import USE_V2_CLASSIFIER


def get_classifier():
    """
    Returns the active classifier instance.
    """

    if USE_V2_CLASSIFIER:
        from classification.classifier import TicketClassifier
    else:
        from classifier import TicketClassifier

    return TicketClassifier()