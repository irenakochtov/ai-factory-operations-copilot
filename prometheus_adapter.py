import json


def convert_alert_to_incident(alert):
    rack_id = alert["rack_id"]

    incident = {
        "incident_id": f"PROM-{rack_id}",
        "site": "DC-DEMO",
        "rack_id": rack_id,
        "timestamp_start": "2026-06-18T12:00:00Z",
        "data_sources": {
            "gpu_events": [],
            "network_events": [],
            "storage_events": [],
        },
    }

    if alert["alertname"] == "HighGPUTemperature":
        incident["data_sources"]["gpu_events"].append(
            {
                "system": "gpu",
                "asset": alert["gpu_id"],
                "alarm": "GPU temperature high",
                "metric": "temperature",
                "value": alert["temperature"],
                "threshold": alert["threshold"],
            }
        )

    elif alert["alertname"] == "IBPacketLoss":
        incident["data_sources"]["network_events"].append(
            {
                "system": "network",
                "asset": "IB-FABRIC",
                "alarm": "Packet loss detected",
                "metric": "packet_loss_pct",
                "value": alert["packet_loss_pct"],
                "threshold": alert["threshold"],
            }
        )

    elif alert["alertname"] == "StorageLatency":
        incident["data_sources"]["storage_events"].append(
            {
                "system": "storage",
                "asset": "STORAGE-01",
                "alarm": "Storage latency high",
                "metric": "p99_latency_ms",
                "value": alert["p99_latency_ms"],
                "threshold": alert["threshold"],
            }
        )

    return incident


if __name__ == "__main__":

    with open(
        "sample_prometheus_alerts.json",
        "r",
        encoding="utf-8",
    ) as f:
        alerts = json.load(f)

    for alert in alerts:
        incident = convert_alert_to_incident(alert)

        print("\n" + "=" * 80)
        print(json.dumps(incident, indent=2))