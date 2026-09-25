INTENTS = {

    "Learn": [
        "how",
        "guide",
        "tutorial",
        "where",
        "help"
    ],

    "Fix": [
        "error",
        "failed",
        "broken",
        "issue",
        "problem"
    ],

    "Configure": [
        "enable",
        "disable",
        "setting",
        "configure"
    ],

    "Access": [
        "login",
        "permission",
        "access",
        "account"
    ],

    "Purchase": [
        "renew",
        "invoice",
        "payment",
        "license"
    ]

}


def detect_intent(text):

    scores = {}

    text = text.lower()

    for intent, words in INTENTS.items():

        score = sum(w in text for w in words)

        scores[intent] = score

    return max(scores, key=scores.get)