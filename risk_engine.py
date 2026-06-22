from collections import Counter


def build_risk_summary(incidents: list) -> dict:
    if not incidents:
        return {
            "site": "DC-DEMO",
            "risk_score": 0,
            "critical_incidents": 0,
            "high_incidents": 0,
            "top_risk_domain": None,
            "highest_risk_assets": [],
        }

    critical = 0
    high = 0

    domains = []
    assets = []

    for incident in incidents:
        analysis = incident.get("analysis", {})

        severity = analysis.get("severity", "").lower()
        incident_type = analysis.get("incident_type")
        asset = incident.get("incident_id")

        if severity == "critical":
            critical += 1

        if severity == "high":
            high += 1

        if incident_type:
            domains.append(incident_type)

        if asset:
            assets.append(asset)

    risk_score = min(
        100,
        (critical * 15) + (high * 7),
    )

    top_domain = None
    if domains:
        top_domain = Counter(domains).most_common(1)[0][0]

    top_assets = assets[:5]

    return {
        "site": "DC-DEMO",
        "risk_score": risk_score,
        "critical_incidents": critical,
        "high_incidents": high,
        "top_risk_domain": top_domain,
        "highest_risk_assets": top_assets,
    }