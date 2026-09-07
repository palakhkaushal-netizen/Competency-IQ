SEVERITY_THRESHOLDS = ((40, "CRITICAL"), (25, "HIGH"), (10, "MEDIUM"), (0, "LOW"))


def severity_for_gap(gap: float) -> str:
    for threshold, severity in SEVERITY_THRESHOLDS:
        if gap >= threshold:
            return severity
    return "LOW"


def readiness_for_scores(scores: list[float]) -> float | None:
    if not scores:
        return None
    return round(sum(scores) / len(scores), 1)
