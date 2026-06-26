import json
import random

INPUT_PATH = "dataset_v2.json"
OUTPUT_PATH = "dataset_v3.json"

SLA_TARGET_BY_TIER = {
    "gold": "99.95%",
    "silver": "99.9%",
    "bronze": "99.5%",
    "standard": "best_effort",
}

MINUTES_REMAINING_BY_SEVERITY = {
    "critical": (15, 30),
    "high": (30, 60),
    "medium": (60, 120),
    "low": (120, 240),
}

BREACH_STATE_BY_SEVERITY = {
    "critical": "critical",
    "high": "warning",
    "medium": "at_risk",
    "low": "monitoring",
}

TIER_CHOICES_BY_SEVERITY = {
    "critical": (["gold", "silver"], [0.7, 0.3]),
    "high": (["silver", "gold"], [0.6, 0.4]),
    "medium": (["bronze", "standard"], [0.6, 0.4]),
    "low": (["standard", "bronze"], [0.7, 0.3]),
}

RESTRICTED_ACTIONS_BY_DOMAIN = {
    "cooling_risk": ["restart_cdu", "open_valve", "reset_pump"],
    "power_risk": ["restart_ups", "switch_power_feed", "reset_pdu"],
    "security_risk": ["unlock_rack", "bypass_access_control"],
    "network_risk": ["reset_switch", "change_fabric_route"],
    "storage_risk": ["restart_storage_node", "force_failover"],
    "hardware_risk": ["restart_node", "reseat_component", "drain_node"],
    "environmental_risk": ["adjust_crah_setpoint", "increase_airflow"],
}

HUMAN_VALIDATION_DOMAINS = {
    "power_risk",
    "cooling_risk",
    "security_risk",
    "environmental_risk",
}

SAFE_ACTIONS = [
    "pause_non_critical_workloads",
    "migrate_workloads",
    "notify_operations",
]

CLUSTER_HEALTH_BY_SEVERITY = {
    "critical": "degraded",
    "high": "degraded",
    "medium": "healthy",
    "low": "healthy",
}

PREDICTED_AVAILABILITY_BY_SEVERITY = {
    "critical": (98.5, 99.4),
    "high": (99.4, 99.8),
    "medium": (99.8, 99.95),
    "low": (99.95, 99.99),
}

GPU_UTIL_BY_DOMAIN = {
    "cooling_risk": (45, 70),
    "network_risk": (60, 85),
    "power_risk": (50, 80),
}

THROUGHPUT_BY_DOMAIN = {
    "cooling_risk": (50, 75),
    "network_risk": (40, 70),
    "power_risk": (55, 80),
    "storage_risk": (60, 85),
    "hardware_risk": (60, 85),
}

WORKLOAD_BY_DOMAIN = {
    "cooling_risk": "llm-training-cluster",
    "network_risk": "llm-training-cluster",
    "power_risk": "llm-training-cluster",
    "hardware_risk": "checkpoint-storage",
    "storage_risk": "checkpoint-storage",
    "security_risk": "facility-systems",
    "environmental_risk": "facility-systems",
}

REVENUE_BY_TIER = {
    "gold": 50000,
    "silver": 20000,
    "bronze": 5000,
    "standard": 1000,
}


def affected_systems(incident: dict) -> list:
    data_sources = incident.get("data_sources", {})
    return sorted(
        source.replace("_events", "")
        for source, events in data_sources.items()
        if events
    )


def difficulty_for(num_affected: int) -> str:
    if num_affected >= 4:
        return "hard"
    if num_affected >= 2:
        return "medium"
    return "easy"


def enrich_incident(incident: dict, rng: random.Random) -> dict:
    enriched = json.loads(json.dumps(incident))

    ground_truth = enriched.get("ground_truth", {})
    incident_type = ground_truth.get("incident_type", "hardware_risk")
    severity = ground_truth.get("severity", "medium")
    scenario = enriched.get("scenario", "unknown")

    systems = affected_systems(enriched)
    num_affected = len(systems)

    tier_options, tier_weights = TIER_CHOICES_BY_SEVERITY.get(
        severity, (["standard", "bronze"], [0.7, 0.3])
    )
    customer_tier = rng.choices(tier_options, weights=tier_weights, k=1)[0]

    low, high = MINUTES_REMAINING_BY_SEVERITY.get(severity, (60, 120))
    minutes_remaining = rng.randint(low, high)

    enriched["business_context"] = {
        "customer_tier": customer_tier,
        "environment": "production",
        "workload_name": WORKLOAD_BY_DOMAIN.get(incident_type, "llm-training-cluster"),
        "business_criticality": severity,
        "revenue_impact_per_hour_usd": int(
            REVENUE_BY_TIER[customer_tier] * rng.uniform(0.8, 1.2)
        ),
    }

    enriched["sla"] = {
        "sla_target": SLA_TARGET_BY_TIER[customer_tier],
        "sla_clock": {
            "status": "running",
            "minutes_remaining": minutes_remaining,
            "breach_state": BREACH_STATE_BY_SEVERITY.get(severity, "monitoring"),
        },
    }

    enriched["automation_policy"] = {
        "safe_actions": list(SAFE_ACTIONS),
        "restricted_actions": RESTRICTED_ACTIONS_BY_DOMAIN.get(incident_type, []),
        "human_validation_required": incident_type in HUMAN_VALIDATION_DOMAINS,
    }

    gpu_low, gpu_high = GPU_UTIL_BY_DOMAIN.get(incident_type, (70, 95))
    tp_low, tp_high = THROUGHPUT_BY_DOMAIN.get(incident_type, (80, 98))
    avail_low, avail_high = PREDICTED_AVAILABILITY_BY_SEVERITY.get(
        severity, (99.8, 99.95)
    )

    enriched["operational_metrics"] = {
        "gpu_utilization_percent": rng.randint(gpu_low, gpu_high),
        "training_throughput_percent": rng.randint(tp_low, tp_high),
        "cluster_health": CLUSTER_HEALTH_BY_SEVERITY.get(severity, "healthy"),
        "predicted_availability": round(rng.uniform(avail_low, avail_high), 3),
    }

    enriched["incident_metadata"] = {
        "domain": incident_type.replace("_risk", ""),
        "scenario": scenario,
        "difficulty": difficulty_for(num_affected),
        "synthetic": True,
        "dataset_version": "3.0",
    }

    return enriched


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    enriched_incidents = []
    for index, incident in enumerate(data["incidents"]):
        rng = random.Random(f"v3-{incident.get('incident_id', index)}")
        enriched_incidents.append(enrich_incident(incident, rng))

    dataset = {
        "dataset_name": "AI Factory Incident Triage Dataset V3",
        "version": "3.0",
        "description": (
            "Synthetic multi-source AI factory incidents enriched with business "
            "context, SLA, automation policy, operational metrics, and metadata "
            "for evaluating an AI Data Center Operations Copilot."
        ),
        "assumption": data.get("assumption", ""),
        "incidents": enriched_incidents,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"Created {OUTPUT_PATH}")
    print(f"Incidents: {len(enriched_incidents)}")


if __name__ == "__main__":
    main()
