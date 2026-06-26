def find_similar_incidents(incident: dict) -> list:
    incident_type = (
        incident.get("ground_truth", {}).get("incident_type")
        or incident.get("incident_type")
        or "unknown"
    )

    similar_map = {
        "cooling_risk": [
            {
                "incident_id": "HIST-COOL-014",
                "summary": "Rack overheating caused by reduced cooling airflow.",
                "resolved_by": "Cleaned airflow path and verified CRAC output.",
                "confidence": 86,
            }
        ],
        "power_risk": [
            {
                "incident_id": "HIST-PWR-021",
                "summary": "Phase imbalance caused PDU overload risk.",
                "resolved_by": "Redistributed load across phases and inspected PDU.",
                "confidence": 84,
            }
        ],
        "network_risk": [
            {
                "incident_id": "HIST-NET-009",
                "summary": "Packet loss caused distributed training slowdown.",
                "resolved_by": "Replaced faulty switch port and verified fabric health.",
                "confidence": 82,
            }
        ],
        "environmental_risk": [
            {
                "incident_id": "HIST-ENV-006",
                "summary": "Water leak sensor triggered near cooling loop.",
                "resolved_by": "Isolated affected line and dispatched facilities inspection.",
                "confidence": 88,
            }
        ],
        "security_risk": [
            {
                "incident_id": "HIST-SEC-004",
                "summary": "Containment door left open causing thermal drift.",
                "resolved_by": "Secured door and checked access logs.",
                "confidence": 80,
            }
        ],
    }

    return similar_map.get(
        incident_type,
        [
            {
                "incident_id": "HIST-GEN-001",
                "summary": "Similar infrastructure degradation pattern detected.",
                "resolved_by": "Escalated to operations team for manual validation.",
                "confidence": 70,
            }
        ],
    )