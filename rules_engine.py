def apply_operational_rules(incident: dict, prediction: dict) -> dict:
    prediction = prediction.copy()

    text_parts = [
        prediction.get("root_cause", ""),
        prediction.get("business_impact", ""),
        prediction.get("recommended_action", ""),
        prediction.get("predicted_next_failure", ""),
        prediction.get("recommended_workload_action", ""),
        str(incident),
    ]

    text = " ".join(str(part).lower() for part in text_parts)

    storage_keywords = [
        "checkpoint",
        "storage",
        "i/o",
        "latency",
        "throughput",
        "filesystem",
        "nfs",
        "lustre",
        "p99",
        "disk",
        "raid",
        "controller",
    ]

    if any(keyword in text for keyword in storage_keywords):
        prediction["incident_type"] = "storage_risk"
        prediction["escalation_team"] = "Platform"

        if prediction.get("severity") in ["high", "critical"]:
            prediction["severity"] = "medium"

        return prediction

    security_keywords = [
        "containment door",
        "unauthorized",
        "physical access",
        "badge",
        "door left open",
        "access control",
    ]

    if any(keyword in text for keyword in security_keywords):
        prediction["incident_type"] = "security_risk"
        prediction["escalation_team"] = "Operations"

        if prediction.get("severity") in ["high", "critical"]:
            prediction["severity"] = "medium"

        return prediction

    return prediction