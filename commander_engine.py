from collections import Counter

from pipeline import run_analysis_pipeline


def _normalize_domain(domain: str) -> str:
    value = str(domain or "").lower().strip()

    if "cool" in value or "thermal" in value or "environment" in value:
        return "cooling"
    if "power" in value or "ups" in value or "pdu" in value:
        return "power"
    if "gpu" in value or "workload" in value or "training" in value:
        return "gpu_workloads"
    if "network" in value or "fabric" in value or "ib" in value:
        return "network"
    if "security" in value or "access" in value or "door" in value:
        return "security"

    return value or "unknown"


def _site_status(analyses: list) -> str:
    severities = [
        report["analysis"].get("severity", "unknown")
        for report in analyses
    ]

    critical_count = severities.count("critical")
    high_count = severities.count("high")

    if critical_count >= 2:
        return "critical"
    if critical_count == 1 or high_count >= 2:
        return "high_risk"
    if high_count == 1:
        return "elevated"
    return "stable"


def _highest_priority(analyses: list) -> dict:
    return max(
        analyses,
        key=lambda report: report["analysis"].get("priority_score", 0),
    )


def _collect_domains(analyses: list) -> list[str]:
    domains = set()

    for report in analyses:
        for system in report["analysis"].get("affected_systems", []):
            domains.add(_normalize_domain(system))

        incident_type = report["analysis"].get("incident_type")
        domains.add(_normalize_domain(incident_type))

    return sorted(domains)


def _collect_teams(analyses: list) -> list[str]:
    teams = {
        report["analysis"].get("escalation_team")
        for report in analyses
        if report["analysis"].get("escalation_team")
    }

    return sorted(teams)


def _count_incident_types(analyses: list) -> dict:
    counter = Counter(
        report["analysis"].get("incident_type", "unknown")
        for report in analyses
    )

    return dict(counter)


def _minimum_time_to_critical(analyses: list):
    values = [
        report["analysis"].get("time_to_critical_minutes")
        for report in analyses
        if isinstance(
            report["analysis"].get("time_to_critical_minutes"),
            int,
        )
    ]

    return min(values) if values else None


def _build_commander_summary(
    site_status: str,
    highest_priority: dict,
    affected_domains: list[str],
    recommended_teams: list[str],
    min_time_to_critical,
) -> str:
    incident_id = highest_priority["incident_id"]
    analysis = highest_priority["analysis"]

    incident_type = analysis.get("incident_type", "unknown")
    severity = analysis.get("severity", "unknown")
    root_cause = analysis.get("root_cause", "unknown root cause")

    time_text = (
        f"The shortest time to critical impact is {min_time_to_critical} minutes."
        if min_time_to_critical is not None
        else "Time to critical impact is currently unknown."
    )

    return (
        f"Site status is {site_status}. "
        f"The highest priority incident is {incident_id}, classified as "
        f"{incident_type} with {severity} severity. "
        f"The likely primary root cause is: {root_cause} "
        f"Affected domains include: {', '.join(affected_domains)}. "
        f"Recommended response teams: {', '.join(recommended_teams)}. "
        f"{time_text}"
    )


def _build_response_plan(analyses: list) -> list[str]:
    sorted_reports = sorted(
        analyses,
        key=lambda report: report["analysis"].get("priority_score", 0),
        reverse=True,
    )

    plan = []

    for report in sorted_reports:
        incident_id = report["incident_id"]
        analysis = report["analysis"]

        team = analysis.get("escalation_team", "Operations")
        action = analysis.get("recommended_action", "Investigate incident")
        workload_action = analysis.get("recommended_workload_action")

        plan.append(
            f"{incident_id}: Dispatch {team}. {action}"
        )

        if workload_action:
            plan.append(
                f"{incident_id}: Workload action: {workload_action}"
            )

    return plan[:8]


def _build_commander_decision(
    site_status: str,
    incident_types: dict,
    min_time_to_critical,
    primary_operational_risk: str,
) -> str:
    dominant_type = primary_operational_risk or max(
        incident_types,
        key=incident_types.get,
    )

    if site_status in ["critical", "high_risk"]:
        return (
            f"Treat this as a {site_status} multi-incident event. "
            f"The primary operational risk is {dominant_type}. "
            "Coordinate response through the NOC and prioritize field validation "
            "before any automated remediation."
        )

    return (
        "Continue monitoring and assign ownership to the recommended teams. "
        "Escalate if additional incidents appear or time-to-critical decreases."
    )


def generate_incident_commander_report(incidents: list) -> dict:
    analyses = []

    for incident in incidents:
        result = run_analysis_pipeline(incident)
        analyses.append(result)

    highest_priority = _highest_priority(analyses)
    affected_domains = _collect_domains(analyses)
    recommended_teams = _collect_teams(analyses)
    incident_types = _count_incident_types(analyses)
    min_time_to_critical = _minimum_time_to_critical(analyses)
    site_status = _site_status(analyses)

    primary_operational_risk = highest_priority["analysis"].get(
        "incident_type"
    )

    commander_summary = _build_commander_summary(
        site_status=site_status,
        highest_priority=highest_priority,
        affected_domains=affected_domains,
        recommended_teams=recommended_teams,
        min_time_to_critical=min_time_to_critical,
    )

    response_plan = _build_response_plan(analyses)

    commander_decision = _build_commander_decision(
        site_status=site_status,
        incident_types=incident_types,
        min_time_to_critical=min_time_to_critical,
        primary_operational_risk=primary_operational_risk,
    )

    return {
        "site_status": site_status,
        "incident_count": len(analyses),
        "highest_priority_incident": highest_priority["incident_id"],
        "primary_operational_risk": primary_operational_risk,
        "incident_type_distribution": incident_types,
        "affected_domains": affected_domains,
        "recommended_teams": recommended_teams,
        "minimum_time_to_critical_minutes": min_time_to_critical,
        "commander_summary": commander_summary,
        "commander_decision": commander_decision,
        "response_plan": response_plan,
        "incident_reports": analyses,
    }