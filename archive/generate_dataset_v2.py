import json
import random
from datetime import datetime, timedelta

random.seed(42)

SITES = ["DC-TLV-01", "DC-FRA-01", "DC-LON-01", "DC-NYC-01", "DC-SIN-01"]

SCENARIOS = [
    {
        "name": "cooling_to_gpu_throttling",
        "incident_type": "cooling_risk",
        "severity": "critical",
        "root_cause": "CDU coolant flow degradation causing GPU thermal throttling",
        "team": "Facilities",
        "action": "Inspect CDU flow rate, coolant pressure, and drain affected GPU workloads if temperature continues rising.",
        "business_impact": "Training throughput degradation and possible workload interruption.",
        "events": [
            ("bms_events", "CDU coolant flow low", "coolant_flow_lpm", 72, 120),
            ("dcim_events", "Rack inlet temperature high", "rack_inlet_temp_c", 35.6, 30),
            ("gpu_events", "GPU temperature high", "gpu_temp_c", 91.8, 85),
            ("gpu_events", "GPU thermal throttling active", "thermal_throttle", "true", "false"),
            ("workload_events", "Training throughput reduced", "training_throughput_pct", 68, 90),
        ],
    },
    {
        "name": "ib_packet_loss_training_slowdown",
        "incident_type": "network_risk",
        "severity": "high",
        "root_cause": "InfiniBand fabric packet loss causing NCCL communication slowdown",
        "team": "Network",
        "action": "Inspect affected InfiniBand switch ports, optics, and reroute training jobs if needed.",
        "business_impact": "Distributed training jobs may miss completion deadline.",
        "events": [
            ("network_events", "InfiniBand packet loss high", "packet_loss_pct", 1.8, 0.1),
            ("network_events", "NCCL allreduce latency high", "allreduce_latency_ms", 240, 80),
            ("workload_events", "Distributed training step time increased", "step_time_ms", 980, 450),
        ],
    },
    {
        "name": "ups_runtime_power_risk",
        "incident_type": "power_risk",
        "severity": "critical",
        "root_cause": "UPS battery degradation reducing runtime for critical racks",
        "team": "Facilities",
        "action": "Verify UPS battery string health and move critical load to redundant power path.",
        "business_impact": "Reduced power protection and risk of rack shutdown during utility instability.",
        "events": [
            ("power_events", "UPS battery health low", "battery_health_pct", 58, 70),
            ("power_events", "UPS runtime below policy", "runtime_minutes", 7, 15),
            ("dcim_events", "Rack power risk increased", "rack_power_risk_score", 88, 70),
        ],
    },
    {
        "name": "storage_checkpoint_delay",
        "incident_type": "hardware_risk",
        "severity": "medium",
        "root_cause": "Storage latency spike delaying model checkpoints",
        "team": "Platform",
        "action": "Check storage pool latency, queue depth, and NVMe health before next checkpoint cycle.",
        "business_impact": "Training jobs may slow down but immediate service impact is limited.",
        "events": [
            ("storage_events", "Storage p99 latency high", "p99_latency_ms", 48, 15),
            ("workload_events", "Checkpoint duration increased", "checkpoint_duration_sec", 420, 180),
        ],
    },
    {
        "name": "environmental_humidity_warning",
        "incident_type": "environmental_risk",
        "severity": "low",
        "root_cause": "Humidity drift outside preferred operating envelope",
        "team": "Facilities",
        "action": "Verify room humidity control and monitor trend for the next 30 minutes.",
        "business_impact": "No immediate business impact, but increased environmental risk if trend continues.",
        "events": [
            ("environmental_events", "Humidity high", "humidity_pct", 66, 60),
            ("dcim_events", "Room environmental risk warning", "environmental_risk_score", 42, 70),
        ],
    },
    {
        "name": "security_door_cooling_risk",
        "incident_type": "security_risk",
        "severity": "medium",
        "root_cause": "Hot aisle containment door left open causing local airflow imbalance",
        "team": "Operations",
        "action": "Send on-site operator to close containment door and verify rack inlet temperatures normalize.",
        "business_impact": "Potential localized hotspot if door remains open.",
        "events": [
            ("security_events", "Containment door left open", "door_open_minutes", 16, 5),
            ("environmental_events", "Local rack inlet temperature rising", "rack_inlet_temp_c", 32.1, 30),
        ],
    },
]

def generate_dataset(n_incidents=120, output_path="dataset_v2.json"):
    base = datetime(2026, 6, 17, 8, 0, 0)
    incidents = []

    for i in range(1, n_incidents + 1):
        scenario = random.choice(SCENARIOS)
        site = random.choice(SITES)
        rack = f"RACK-{random.choice(['A','B','C','D','E'])}{random.randint(1,40):02d}"
        incident_id = f"INC-{i:04d}"
        start_time = base + timedelta(minutes=i * 3)

        record = {
            "incident_id": incident_id,
            "site": site,
            "rack_id": rack,
            "timestamp_start": start_time.isoformat() + "Z",
            "scenario": scenario["name"],
            "data_sources": {
                "bms_events": [],
                "dcim_events": [],
                "gpu_events": [],
                "network_events": [],
                "power_events": [],
                "storage_events": [],
                "workload_events": [],
                "security_events": [],
                "environmental_events": []
            },
            "ground_truth": {
                "incident_type": scenario["incident_type"],
                "severity": scenario["severity"],
                "root_cause": scenario["root_cause"],
                "escalation_team": scenario["team"],
                "recommended_action": scenario["action"],
                "business_impact": scenario["business_impact"],
                "priority_score": {
                    "low": 25,
                    "medium": 55,
                    "high": 80,
                    "critical": 95
                }[scenario["severity"]],
                "time_to_critical_minutes": {
                    "low": 240,
                    "medium": 120,
                    "high": 30,
                    "critical": 15
                }[scenario["severity"]]
            }
        }

        for j, event_tuple in enumerate(scenario["events"], start=1):
            source, alarm, metric, value, threshold = event_tuple
            event_time = start_time + timedelta(minutes=j)
            record["data_sources"][source].append({
                "event_id": f"{incident_id}-E{j:02d}",
                "timestamp": event_time.isoformat() + "Z",
                "system": source.replace("_events", ""),
                "asset": f"{source.replace('_events','').upper()}-{random.randint(1,12):02d}",
                "rack_id": rack,
                "alarm": alarm,
                "metric": metric,
                "value": value,
                "threshold": threshold
            })

        incidents.append(record)

    dataset = {
        "dataset_name": "AI Factory Incident Triage Dataset V2",
        "version": "2.0",
        "description": "Synthetic multi-source AI factory incidents for evaluating an AI Data Center Operations Copilot.",
        "assumption": "Events are assumed to be already collected from BMS, DCIM, GPU telemetry, network monitoring, power systems, storage, workload telemetry, security, and environmental systems.",
        "incidents": incidents
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"Created {output_path}")
    print(f"Incidents: {len(incidents)}")

if __name__ == "__main__":
    generate_dataset()
