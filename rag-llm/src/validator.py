INTENT_RULES = {
    "policy_info": [],
    "company_eligibility": ["company", "batch_year", "cgpa", "branch"],
    "company_package": ["company", "batch_year"],
    "company_rounds": ["company", "batch_year"],
    "placement_statistics": ["batch_year"]
}

def validate(parsed: dict) -> tuple[bool, str | None]:
    intent = parsed.get("intent")

    if intent not in INTENT_RULES:
        return False, "Unsupported query intent."

    missing = []
    for field in INTENT_RULES[intent]:
        if parsed.get(field) is None:
            missing.append(field)

    if missing:
        return False, f"Missing required information: {', '.join(missing)}"

    return True, None
