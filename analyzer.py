import re
from app.patterns import PATTERNS
from app.scoring import calculate_intent_scores

def split_into_chunks(text: str):
    # Split on sentence endings, line breaks, or common separators
    chunks = re.split(r'(?<=[.!?])\s+|[\n\r]+|\s{2,}|\|', text)
    # Filter out empty chunks and very short ones
    return [chunk.strip() for chunk in chunks if chunk.strip() and len(chunk.strip()) > 2]

def analyze_text(text: str):
    chunks = split_into_chunks(text)
    results = []
    seen = set()  # Avoid duplicate detections

    # This catches patterns that span across the scraped content
    all_text_sources = chunks + [text]
    
    for source in all_text_sources:
        for pattern in PATTERNS:
            matches = pattern["regex"].findall(source)
            for match in matches:
                # Create a unique key for deduplication
                match_text = match if isinstance(match, str) else match[0]
                key = (pattern["name"], match_text.lower().strip())
                
                if key not in seen:
                    seen.add(key)
                    results.append({
                        "matched_text": match_text,
                        "pattern": pattern["name"],
                        "category": pattern["category"],
                        "explanation": pattern["explanation"]
                    })

    intent_scores = calculate_intent_scores(results)

    return {
        "input_text": text[:500] + "..." if len(text) > 500 else text,  # Truncate for readability
        "detections": results,
        "intent_breakdown": intent_scores
    }
