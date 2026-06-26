import json

from agent_router import analyze_with_routed_agent


def analyze_incident(incident: dict) -> dict:
    return analyze_with_routed_agent(incident)


def print_human_readable_report(prediction: dict) -> None:
    print("\n=== INCIDENT SUMMARY ===")
    print(prediction.get("executive_summary", ""))

    print("\n=== INCIDENT TYPE ===")
    print(prediction.get("incident_type", ""))

    print("\n=== SEVERITY ===")
    print(prediction.get("severity", ""))

    print("\n=== ROOT CAUSE ===")
    print(prediction.get("root_cause", ""))

    print("\n=== EVENT PROPAGATION PATH ===")
    for step in prediction.get("event_propagation_path", []):
        print(f"- {step}")

    print("\n=== AFFECTED SYSTEMS ===")
    for system in prediction.get("affected_systems", []):
        print(f"- {system}")

    print("\n=== BUSINESS IMPACT ===")
    print(prediction.get("business_impact", ""))

    print("\n=== PREDICTED NEXT FAILURE ===")
    print(prediction.get("predicted_next_failure", ""))

    print("\n=== RECOMMENDED WORKLOAD ACTION ===")
    print(prediction.get("recommended_workload_action", ""))

    print("\n=== RECOMMENDED ACTION ===")
    print(prediction.get("recommended_action", ""))

    print("\n=== IMMEDIATE ACTIONS ===")
    for idx, action in enumerate(prediction.get("immediate_actions", []), start=1):
        print(f"{idx}. {action}")

    print("\n=== ESCALATION TEAM ===")
    print(prediction.get("escalation_team", ""))

    print("\n=== PRIORITY ===")
    print(prediction.get("priority_score", ""))

    print("\n=== CONFIDENCE ===")
    print(prediction.get("confidence_score", ""))

    print("\n=== TIME TO CRITICAL ===")
    print(prediction.get("time_to_critical_minutes", ""))


if __name__ == "__main__":
    with open("dataset_v2.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    incident = data["incidents"][15]

    print("Analyzing incident:", incident.get("incident_id", "unknown"))

    prediction = analyze_incident(incident)

    print("\n=== RAW JSON OUTPUT ===")
    print(json.dumps(prediction, indent=2))

    print_human_readable_report(prediction)