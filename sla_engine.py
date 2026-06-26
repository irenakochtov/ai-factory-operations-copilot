import json


SLA_CONTRACTS_PATH = "sla_contracts.json"


def load_sla_contracts() -> dict:
    with open(SLA_CONTRACTS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def _get_customer_tier(incident: dict) -> str:
    business_context = incident.get("business_context", {})
    return str(business_context.get("customer_tier", "standard")).lower()


def _get_contract_for_tier(customer_tier: str, contracts: dict) -> dict:
    return contracts.get(customer_tier) or contracts.get("standard") or {}


def _calculate_breach_state(minutes_remaining: int) -> str:
    if minutes_remaining <= 15:
        return "critical"
    if minutes_remaining <= 30:
        return "warning"
    if minutes_remaining <= 60:
        return "at_risk"
    return "monitoring"


def _recommended_action(incident_type: str) -> str:
    actions = {
        "cooling_risk": "Migrate critical workloads and dispatch Facilities for cooling validation.",
        "power_risk": "Pause non-critical workloads and prepare graceful shutdown if power redundancy degrades.",
        "network_risk": "Reroute traffic or reduce distributed training load while Network team investigates.",
        "security_risk": "Dispatch Operations to validate physical security and access logs.",
        "storage_risk": "Throttle affected workloads and validate storage latency or failure domain.",
        "environmental_risk": "Dispatch Facilities to inspect environmental conditions and protect affected racks.",
    }

    return actions.get(
        incident_type,
        "Notify Operations and continue monitoring until ownership is confirmed.",
    )


def assess_sla_risk(incident: dict, analysis: dict) -> dict:
    contracts = load_sla_contracts()

    customer_tier = _get_customer_tier(incident)
    contract = _get_contract_for_tier(customer_tier, contracts)

    priority_score = analysis.get("priority_score", 50)
    time_to_critical = analysis.get("time_to_critical_minutes")

    if isinstance(time_to_critical, int):
        minutes_remaining = time_to_critical
    elif priority_score >= 95:
        minutes_remaining = 15
    elif priority_score >= 85:
        minutes_remaining = 30
    elif priority_score >= 70:
        minutes_remaining = 60
    else:
        minutes_remaining = contract.get("breach_window_minutes", 180)

    incident_type = analysis.get("incident_type", "unknown")
    business_criticality = incident.get("business_context", {}).get(
        "business_criticality",
        "standard",
    )

    return {
        "sla_target": contract.get("availability_target", "best_effort"),
        "customer_tier": customer_tier,
        "sla_status": "at_risk" if minutes_remaining <= 60 else "monitoring",
        "sla_clock": {
            "status": "running",
            "minutes_remaining": minutes_remaining,
            "breach_state": _calculate_breach_state(minutes_remaining),
        },
        "business_criticality": business_criticality,
        "recommended_action_before_breach": _recommended_action(incident_type),
        "safe_automation": contract.get("allowed_automation", []),
        "restricted_automation": contract.get("restricted_automation", []),
        "human_validation_required": contract.get(
            "human_validation_required",
            True,
        ),
    }