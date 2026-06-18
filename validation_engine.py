SEVERITY_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def cap_severity(severity: str, severity_cap: str) -> str:
    if not severity or not severity_cap:
        return severity

    severity = severity.lower()
    severity_cap = severity_cap.lower()

    if severity not in SEVERITY_ORDER:
        return severity_cap

    if severity_cap not in SEVERITY_ORDER:
        return severity

    if SEVERITY_ORDER[severity] > SEVERITY_ORDER[severity_cap]:
        return severity_cap

    return severity


def enforce_deterministic_classification(
    prediction: dict,
    deterministic_classification: dict,
) -> dict:
    prediction = prediction.copy()

    if not deterministic_classification:
        return prediction

    if deterministic_classification.get("incident_type"):
        prediction["incident_type"] = deterministic_classification["incident_type"]

    if deterministic_classification.get("escalation_team"):
        prediction["escalation_team"] = deterministic_classification["escalation_team"]

    if deterministic_classification.get("severity_cap"):
        prediction["severity"] = cap_severity(
            prediction.get("severity"),
            deterministic_classification["severity_cap"],
        )

    prediction["deterministic_rule_id"] = deterministic_classification.get("rule_id")

    return prediction