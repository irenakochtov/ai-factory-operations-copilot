import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("NEBIUS_BASE_URL"),
    api_key=os.getenv("NEBIUS_API_KEY"),
)

MODEL = os.getenv("NEBIUS_MODEL")


def extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in model response")
    return json.loads(match.group(0))


def analyze_incident(incident: dict) -> dict:
    deterministic_classification = incident.get(
        "deterministic_classification",
        {},
    )

    prompt = f"""
You are a Senior AI Factory Operations Copilot.

Your job is to help NOC, Facilities, Network, Platform, and AI Infrastructure teams understand what is happening, what will likely happen next, and what they should do first.

You analyze multi-source operational signals from:
- BMS
- DCIM
- cooling systems
- power systems
- GPU clusters
- NVIDIA DCGM telemetry
- InfiniBand networks
- Ethernet networks
- storage systems
- workload telemetry
- environmental monitoring
- security systems

IMPORTANT:

A deterministic classification layer has already analyzed the incident using structured operational signals.

Use the provided deterministic classification as the primary routing decision.

Do not override:
- incident_type
- escalation_team

unless the provided evidence clearly contradicts it.

Your primary responsibility is:
- root cause analysis
- business impact analysis
- operational recommendations
- predicted next failure
- immediate operational actions

Return ONLY valid JSON.

Required JSON schema:
{{
  "executive_summary": "",
  "incident_type": "",
  "severity": "",
  "root_cause": "",
  "event_propagation_path": [],
  "affected_systems": [],
  "escalation_team": "",
  "recommended_action": "",
  "immediate_actions": [],
  "business_impact": "",
  "predicted_next_failure": "",
  "recommended_workload_action": "",
  "priority_score": 0,
  "confidence_score": 0,
  "time_to_critical_minutes": 0
}}

Rules:
- Do not include markdown.
- Do not explain outside the JSON.
- incident_type must be one of: cooling_risk, power_risk, network_risk, hardware_risk, environmental_risk, security_risk, storage_risk.
- severity must be one of: low, medium, high, critical.
- escalation_team must be one of: Facilities, NOC, Network, Platform, Security, Operations, AI Infrastructure, SRE.
- priority_score must be an integer from 1 to 100.
- confidence_score must be an integer from 0 to 100.
- time_to_critical_minutes must be one of: 15, 30, 60, 120, 240.
- immediate_actions must contain 3 to 5 concrete operational steps.
- affected_systems must contain impacted technical domains.
- event_propagation_path should describe the chain of events in order.
- recommended_workload_action should describe what to do with AI workloads if relevant. If not relevant, write "No workload action required".

Deterministic Classification:
{json.dumps(deterministic_classification, indent=2)}

Incident:
{json.dumps(incident, indent=2)}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=1100,
    )

    raw_text = response.choices[0].message.content
    return extract_json(raw_text)


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