def build_failure_cascade(incident_type: str) -> list:
    cascades = {
        "cooling_risk": [
            "GPU thermal throttling",
            "GPU shutdown",
            "Training job interruption",
            "SLA violation",
        ],
        "network_risk": [
            "Packet retransmissions increase",
            "NCCL communication slowdown",
            "Distributed training degradation",
            "AI job failure",
        ],
        "storage_risk": [
            "Storage latency increase",
            "Checkpoint delays",
            "Training interruption",
            "Data pipeline backlog",
        ],
        "power_risk": [
            "Power redundancy degradation",
            "UPS/PDU overload risk",
            "Node shutdown",
            "Service disruption",
        ],
        "hardware_risk": [
            "Hardware instability",
            "Repeated device errors",
            "Node failure",
            "Workload migration",
        ],
        "environmental_risk": [
            "Environmental drift",
            "Sensor alarms",
            "Equipment stress",
            "Operational impact",
        ],
    }

    chain = cascades.get(
        incident_type,
        [
            "Incident escalation",
            "Service degradation",
            "Operational disruption",
        ],
    )

    return [
        {
            "step": idx + 1,
            "event": event,
        }
        for idx, event in enumerate(chain)
    ]