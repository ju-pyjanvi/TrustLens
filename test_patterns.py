import pytest
from app.analyzer import analyze_text

TEST_CASES = [
    (
        "Only 2 rooms left! Hurry before it's gone.",
        ["Artificial Scarcity", "Time Pressure"]
    ),
    (
        "10 people are viewing this now. Bestseller product!",
        ["Activity Notifications", "Popularity Claims"]
    ),
    (
        "Sign up today to get your free trial.",
        ["Account Pressure", "Free Bait"]
    ),
    (
        "You won't believe this shocking offer.",
        ["Curiosity Gap", "Sensationalism"]
    ),
    (
        "Deal ends in 2 hours. Time is running out!",
        ["Countdown Pressure"]
    ),
    (
        "Money back guarantee. Risk free purchase.",
        ["Risk Reversal"]
    ),
    (
        "Exclusive access for members only. Don't miss out!",
        ["Exclusivity", "Fear of Missing Out"]
    )
]

@pytest.mark.parametrize("text,expected_patterns", TEST_CASES)
def test_pattern_detection(text, expected_patterns):
    result = analyze_text(text)
    detected = [d["pattern"] for d in result["detections"]]
    for pattern in expected_patterns:
        assert pattern in detected, f"Expected {pattern} in detections for: {text}"
