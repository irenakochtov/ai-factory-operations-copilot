def normalize(value: str) -> str:
    return str(value or "").strip().lower()


def risk_level_for_window(
    severity: str,
    time_to_critical_minutes: int,
    window_minutes: int,
) -> str:
    severity = normalize(severity)

    if severity == "critical":
        if window_minutes >= time_to_critical_minutes:
            return "critical"
        return "high"

    if severity == "high":
        if window_minutes >= time_to_critical_minutes:
            return "high"
        return "medium"

    if severity == "medium":
        if window_minutes >= time_to_critical_minutes:
            return "medium"
        return "low"

    return "low"


def get_predictions_by_incident_type(incident_type: str) -> dict:
    incident_type = normalize(incident_type)

    forecasts = {
        "cooling_risk": {
            15: "GPU thermal throttling may begin as rack inlet temperature continues rising.",
            30: "Affected GPU nodes may reach shutdown threshold if cooling is not restored.",
            60: "Rack-level workload disruption may occur, including failed training or inference jobs.",
        },
        "power_risk": {
            15: "Power redundancy may degrade and affected equipment may shift to backup feeds.",
            30: "UPS or PDU stress may increase, raising the risk of node shutdowns.",
            60: "Critical workloads may be interrupted if power instability continues.",
        },
        "network_risk": {
            15: "Packet retransmits and NCCL latency may increase across distributed workloads.",
            30: "Training jobs may slow down significantly due to degraded interconnect performance.",
            60: "Distributed AI jobs may fail or require restart if fabric instability continues.",
        },
        "hardware_risk": {
            15: "Affected hardware may show degraded performance or intermittent errors.",
            30: "Node-level instability may increase, including resets or device errors.",
            60: "Workloads may fail or migrate due to persistent hardware degradation.",
        },
        "environmental_risk": {
            15: "Local environmental drift may begin affecting nearby racks or sensors.",
            30: "Temperature or humidity deviation may trigger secondary infrastructure alarms.",
            60: "Sustained environmental instability may impact hardware reliability.",
        },
        "security_risk": {
            15: "Physical or access-control anomaly may remain unresolved and increase operational exposure.",
            30: "Secondary environmental or operational risk may appear if the breach affects containment or access.",
            60: "Escalation to operations management may be required if the condition is not cleared.",
        },
        "storage_risk": {
            15: "Storage latency may increase and checkpoint operations may slow down.",
            30: "AI training checkpoints may be delayed or fail under sustained storage pressure.",
            60: "Workloads may experience interruption, rollback, or data pipeline delays.",
        },
    }

    return forecasts.get(
        incident_type,
        {
            15: "Operational degradation may begin if the condition remains unresolved.",
            30: "Incident impact may expand to dependent systems.",
            60: "Service reliability may degrade and require escalation.",
        },
    )


def generate_failure_forecast(
    incident_type: str,
    severity: str,
    time_to_critical_minutes: int,
) -> dict:
    """
    Generate a simple operational failure forecast timeline.

    This is a deterministic forecast layer. It does not replace the LLM analysis.
    It converts the incident type, severity, and time-to-critical estimate into
    a structured timeline that is easier for NOC and operations teams to consume.
    """

    try:
        time_to_critical_minutes = int(time_to_critical_minutes)
    except (TypeError, ValueError):
        time_to_critical_minutes = 60

    predictions = get_predictions_by_incident_type(incident_type)

    forecast = {}
    for window in [15, 30, 60]:
        forecast[f"{window}_minutes"] = {
            "risk": risk_level_for_window(
                severity=severity,
                time_to_critical_minutes=time_to_critical_minutes,
                window_minutes=window,
            ),
            "prediction": predictions[window],
        }

    return forecast