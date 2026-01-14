def calculate_intent_scores(detections):
    scores = {
        "Urgency & Scarcity": 0,
        "Social Proof": 0,
        "Pricing Tricks": 0,
        "Data Harvesting": 0,
        "FOMO & Emotion": 0,
        "Clickbait": 0,
        "Trust Manipulation": 0
    }

    for d in detections:
        category = d["category"]
        if category in scores:
            scores[category] += 1

    total = sum(scores.values()) or 1

    for key in scores:
        scores[key] = round((scores[key] / total) * 100, 2)

    return scores
