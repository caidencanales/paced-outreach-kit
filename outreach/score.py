"""Evidence-backed scoring. Every signal is 0-5 and must cite a URL; no URL, no points.

Card format (JSON):
    {"traction": {"value": 4, "evidence": "https://...", "why": "10k MAU per their launch post"}, ...}
"""


def score(cfg, card):
    s = cfg["scoring"]
    weights, social = s["signals"], set(s.get("social_signals", []))
    errors, total = [], 0.0
    for name, entry in card.items():
        if name not in weights:
            errors.append(f"unknown signal {name!r}; known: {', '.join(weights)}")
            continue
        v = entry.get("value")
        if not isinstance(v, (int, float)) or not 0 <= v <= 5:
            errors.append(f"{name}: value must be 0-5")
            continue
        if v > 0 and not str(entry.get("evidence", "")).startswith("http"):
            errors.append(f"{name}: needs an evidence URL to score above 0")
            continue
        total += weights[name] * v
    best = 5 * sum(weights.values())
    missing = [k for k in weights if k not in card]
    has_social = any(card.get(k, {}).get("value", 0) > 0 for k in social)
    result = round(100 * total / best, 1) if best else 0
    return {"score": result, "has_social": has_social, "missing": missing, "errors": errors,
            "contact": result >= s["min_score_to_contact"] and not errors}
