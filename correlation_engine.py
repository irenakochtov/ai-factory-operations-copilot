import json


def get_all_events(incident: dict) -> list:
    events = []

    data_sources = incident.get("data_sources", {})

    for source_name, source_events in data_sources.items():
        events.extend(source_events)

    return events


def calculate_correlation_context(
    incident: dict,
    asset_history_path: str = "asset_history.json",
) -> dict:
    """
    Build compact operational context before sending data to the LLM.
    """

    rack_id = incident.get("rack_id")

    events = get_all_events(incident)

    affected_systems = set()
    affected_assets = set()

    high_severity_signals = 0

    for event in events:
        affected_systems.add(event.get("system"))
        affected_assets.add(event.get("asset"))

        value = event.get("value", 0)
        threshold = event.get("threshold", 1)

        try:
            if threshold and value > threshold:
                high_severity_signals += 1
        except Exception:
            pass

    asset_history_matches = []

    try:
        with open(asset_history_path, "r", encoding="utf-8") as f:
            history = json.load(f)

        for asset in history:
            if asset.get("asset_id") == rack_id:
                asset_history_matches.append(asset)

    except FileNotFoundError:
        pass

    correlation_summary = (
        f"Rack {rack_id} contains "
        f"{len(events)} correlated events across "
        f"{len(affected_systems)} operational domains."
    )

    return {
        "rack_id": rack_id,
        "total_events": len(events),
        "affected_systems": sorted(list(affected_systems)),
        "affected_assets": sorted(list(affected_assets)),
        "high_severity_signals": high_severity_signals,
        "historical_matches": len(asset_history_matches),
        "correlation_summary": correlation_summary,
    }


if __name__ == "__main__":

    with open("dataset_v2.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    incident = data["incidents"][15]

    result = calculate_correlation_context(incident)

    print(json.dumps(result, indent=2))