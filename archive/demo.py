import json
import re
from pathlib import Path

from pipeline import run_analysis_pipeline

DATASET_PATH = "dataset_v2.json"
OUTPUT_PATH = "results/demo_output.txt"

DEMO_INCIDENTS = [
    "INC-0001",
    "INC-0008",
    "INC-0016",
    "INC-0025",
    "INC-0040",
]


def clean_text(value):
    if value is None:
        return ""

    text = str(value)
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)
    text = re.sub(r"(?<=[a-zA-Z])(?=\d)", " ", text)
    text = re.sub(r"(?<=\d)(?=[a-zA-Z])", " ", text)
    text = text.replace("Infini Band", "InfiniBand")
    text = text.replace("workloadaction", "workload action")
    text = text.replace("willlikely", "will likely")
    text = text.replace("operationalactions", "operational actions")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def find_incident(data, incident_id):
    for incident in data["incidents"]:
        if incident["incident_id"] == incident_id:
            return incident

    raise ValueError(f"Incident {incident_id} not found")


def format_demo_result(incident_id, correlation_context, analysis):
    lines = []

    lines.append("\n" + "=" * 90)
    lines.append(f"INCIDENT: {incident_id}")
    lines.append("=" * 90)

    lines.append(f"Type:       {clean_text(analysis.get('incident_type'))}")
    lines.append(f"Severity:   {clean_text(analysis.get('severity'))}")
    lines.append(f"Team:       {clean_text(analysis.get('escalation_team'))}")
    lines.append(f"Priority:   {analysis.get('priority_score')}")
    lines.append(f"Confidence: {analysis.get('confidence_score')}")
    lines.append(f"TTC:        {analysis.get('time_to_critical_minutes')} minutes")

    lines.append("\nCorrelation:")
    lines.append(clean_text(correlation_context.get("correlation_summary")))

    lines.append("\nRoot Cause:")
    lines.append(clean_text(analysis.get("root_cause")))

    lines.append("\nPredicted Next Failure:")
    lines.append(clean_text(analysis.get("predicted_next_failure")))

    lines.append("\nRecommended Workload Action:")
    lines.append(clean_text(analysis.get("recommended_workload_action")))

    lines.append("\nImmediate Actions:")
    for index, action in enumerate(
        analysis.get("immediate_actions", []),
        start=1,
    ):
        lines.append(f"{index}. {clean_text(action)}")

    return "\n".join(lines)


def main():
    data = load_dataset()
    output_lines = []

    output_lines.append("AI FACTORY OPERATIONS COPILOT DEMO")
    output_lines.append("Running selected incident scenarios...")
    output_lines.append(
        "Ground truth and scenario fields are removed before inference."
    )

    for incident_id in DEMO_INCIDENTS:
        incident = find_incident(data, incident_id)
        result = run_analysis_pipeline(incident)

        result_text = format_demo_result(
            incident_id=incident_id,
            correlation_context=result["correlation_context"],
            analysis=result["analysis"],
        )

        output_lines.append(result_text)

    final_output = "\n".join(output_lines)

    print(final_output)

    Path("results").mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(final_output)

    print(f"\nDemo output saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
