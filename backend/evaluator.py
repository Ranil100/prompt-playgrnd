import re


def _score(output: str) -> int:
    """Simple deterministic heuristic for a demo evaluator."""
    if not output.strip():
        return 0

    score = 50

    # Reward useful structure.
    if re.search(r"(^|\n)\s*[-*•]\s+", output):
        score += 10
    if re.search(r"(^|\n)\s*\d+[.)]\s+", output):
        score += 8

    # Reward moderate length, but avoid excessive verbosity.
    words = len(output.split())
    if 15 <= words <= 180:
        score += 15
    elif words > 300:
        score -= 10

    # Penalize obvious meta commentary.
    if "as an ai" in output.lower():
        score -= 8

    return max(0, min(100, score))


def evaluate_outputs(task: str, results: list[dict]):
    for result in results:
        result["score"] = _score(result["output"])

    winner_result = max(results, key=lambda item: item["score"])
    winner = winner_result["strategy"]
    reason = (
        f"{winner_result['strategy'].replace('-', ' ').title()} received the "
        f"highest heuristic score ({winner_result['score']}/100) based on "
        "clarity, useful structure, and response length."
    )
    return results, winner, reason
