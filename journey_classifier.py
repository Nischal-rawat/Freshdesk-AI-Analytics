JOURNEY = {

    "Evaluation": [
        "trial",
        "demo"
    ],

    "Onboarding": [
        "getting started",
        "first login",
        "setup"
    ],

    "Activation": [
        "activate",
        "enable"
    ],

    "Daily Usage": [
        "rewrite",
        "grammar",
        "ai"
    ],

    "Administration": [
        "license",
        "users",
        "admin"
    ],

    "Renewal": [
        "renew",
        "invoice",
        "quote"
    ]

}


def detect_journey(text):

    text = text.lower()

    best = "Unknown"

    best_score = 0

    for stage, words in JOURNEY.items():

        score = sum(w in text for w in words)

        if score > best_score:

            best_score = score

            best = stage

    return best