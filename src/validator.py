import re
from collections import Counter

COMMON_VERBS = {
    "create", "update", "delete", "implement", "add", "remove", "fix",
    "build", "configure", "integrate", "enable", "disable", "validate",
    "deploy", "generate", "login", "authenticate", "authorize",
    "sync", "export", "import", "monitor", "alert", "notify"
}

STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with",
    "is", "are", "am", "was", "were", "be", "been", "being", "this", "that",
    "it", "as", "at", "by", "from", "we", "you", "they", "i"
}

def validate_notes_text(text: str) -> tuple[bool, str]:
    """
    Returns (is_valid, message). If invalid, message tells user what to add.
    """
    if not text or not text.strip():
        return False, "Please enter notes (requirement/bug description) to generate a work item."

    t = text.strip()

    if len(t) < 20:
        return False, "Notes are too short. Add 1–2 sentences describing the requirement or problem."

    words = re.findall(r"[A-Za-z0-9']+", t.lower())
    if len(words) < 5:
        return False, "Notes look unclear. Add more detail (goal, expected behavior, constraints)."

    non_alnum = len(re.findall(r"[^A-Za-z0-9\s]", t))
    if non_alnum / max(len(t), 1) > 0.35:
        return False, "Notes contain too many symbols. Please provide a clear text description."

    counts = Counter(words)
    most_common_ratio = counts.most_common(1)[0][1] / max(len(words), 1)
    if most_common_ratio > 0.45:
        return False, "Notes repeat the same word too much. Please describe the feature/bug in normal sentences."

    unique_ratio = len(set(words)) / max(len(words), 1)
    if unique_ratio < 0.40:
        return False, "Notes look repetitive/unclear. Please add more specific details."

    stop_ratio = sum(1 for w in words if w in STOPWORDS) / max(len(words), 1)
    if stop_ratio > 0.65:
        return False, "Notes do not contain enough meaningful keywords. Please describe what to build or fix."

    has_verb = any(w in COMMON_VERBS for w in words)
    if not has_verb:
        return False, "Please include an action (e.g., implement/login/fix/configure) and expected outcome."

    return True, "OK"
