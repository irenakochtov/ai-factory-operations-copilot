def event_text(events: list) -> str:
    return " ".join(str(event).lower() for event in events)


def classify_incident(incident: dict) -> dict:
    data_sources = incident.get("data_sources", {})

    bms_events = data_sources.get("bms_events", [])
    dcim_events = data_sources.get("dcim_events", [])
    gpu_events = data_sources.get("gpu_events", [])
    network_events = data_sources.get("network_events", [])
    storage_events = data_sources.get("storage_events", [])
    power_events = data_sources.get("power_events", [])
    environmental_events = data_sources.get("environmental_events", [])
    security_events = data_sources.get("security_events", [])

    cooling_text = event_text(
        bms_events
        + dcim_events
        + environmental_events
        + gpu_events
    )

    cooling_keywords = [
        "cooling",
        "cdu",
        "crac",
        "crah",
        "coolant",
        "flow",
        "pressure",
        "temperature",
        "temp",
        "thermal",
        "throttle",
        "throttling",
        "rack_inlet",
        "inlet",
        "hot aisle",
        "containment",
    ]

    if security_events:
        return {
            "incident_type": "security_risk",
            "escalation_team": "Operations",
            "severity_cap": "medium",
            "rule_id": "SEC-001",
        }

    if storage_events:
        return {
            "incident_type": "storage_risk",
            "escalation_team": "Platform",
            "severity_cap": "medium",
            "rule_id": "STOR-001",
        }

    if network_events:
        return {
            "incident_type": "network_risk",
            "escalation_team": "Network",
            "severity_cap": "high",
            "rule_id": "NET-001",
        }

    if power_events:
        return {
            "incident_type": "power_risk",
            "escalation_team": "Facilities",
            "severity_cap": "critical",
            "rule_id": "PWR-001",
        }

    if any(keyword in cooling_text for keyword in cooling_keywords):
        return {
            "incident_type": "cooling_risk",
            "escalation_team": "Facilities",
            "severity_cap": "critical",
            "rule_id": "COOL-001",
        }

    if environmental_events:
        return {
            "incident_type": "environmental_risk",
            "escalation_team": "Facilities",
            "severity_cap": "high",
            "rule_id": "ENV-001",
        }

    if gpu_events:
        return {
            "incident_type": "hardware_risk",
            "escalation_team": "AI Infrastructure",
            "severity_cap": "high",
            "rule_id": "GPU-001",
        }

    return {
        "incident_type": "hardware_risk",
        "escalation_team": "NOC",
        "severity_cap": "medium",
        "rule_id": "DEFAULT-001",
    }