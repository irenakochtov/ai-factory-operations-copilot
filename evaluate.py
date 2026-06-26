import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from pipeline import run_analysis_pipeline

DATASET_PATH = "dataset_v3.json"
REPORT_PATH = "results/eval_report.json"


def normalize(value):
    return str(value).strip().lower()


def evaluate_incident(incident: dict) -> dict:
    ground_truth = incident["ground_truth"]
    result = run_analysis_pipeline(incident)
    prediction = result["analysis"]

    checks = {
        "severity": normalize(prediction.get("severity"))
        == normalize(ground_truth["severity"]),
        "incident_type": normalize(prediction.get("incident_type"))
        == normalize(ground_truth["incident_type"]),
        "escalation_team": normalize(prediction.get("escalation_team"))
        == normalize(ground_truth["escalation_team"]),
    }

    return {
        "incident_id": incident["incident_id"],
        "scenario": incident.get("scenario"),
        "prediction": {
            "severity": prediction.get("severity"),
            "incident_type": prediction.get("incident_type"),
            "escalation_team": prediction.get("escalation_team"),
        },
        "ground_truth": {
            "severity": ground_truth["severity"],
            "incident_type": ground_truth["incident_type"],
            "escalation_team": ground_truth["escalation_team"],
        },
        "deterministic_classification": result["deterministic_classification"],
        "correct": checks,
        "all_correct": all(checks.values()),
    }


def summarize(results: list) -> dict:
    total = len(results)
    if total == 0:
        return {}

    counts = {
        "severity": sum(1 for r in results if r["correct"]["severity"]),
        "incident_type": sum(1 for r in results if r["correct"]["incident_type"]),
        "escalation_team": sum(
            1 for r in results if r["correct"]["escalation_team"]
        ),
        "all_correct": sum(1 for r in results if r["all_correct"]),
    }

    accuracy = {key: value / total for key, value in counts.items()}
    accuracy["overall"] = (
        accuracy["severity"] + accuracy["incident_type"] + accuracy["escalation_team"]
    ) / 3

    return {
        "total_incidents": total,
        "counts": counts,
        "accuracy": accuracy,
    }


def print_summary(summary: dict, failures: list) -> None:
    total = summary["total_incidents"]
    counts = summary["counts"]
    accuracy = summary["accuracy"]

    print("\n" + "=" * 80)
    print("AI FACTORY COPILOT EVALUATION")
    print("=" * 80)
    print(f"Total incidents: {total}")
    print(
        f"Severity accuracy:       "
        f"{counts['severity']}/{total} = {accuracy['severity']:.2%}"
    )
    print(
        f"Incident type accuracy:  "
        f"{counts['incident_type']}/{total} = {accuracy['incident_type']:.2%}"
    )
    print(
        f"Escalation team accuracy:"
        f" {counts['escalation_team']}/{total} = {accuracy['escalation_team']:.2%}"
    )
    print(
        f"All fields correct:      "
        f"{counts['all_correct']}/{total} = {accuracy['all_correct']:.2%}"
    )
    print(f"\nOverall accuracy: {accuracy['overall']:.2%}")

    if failures:
        print(f"\nFailures ({len(failures)}):")
        for item in failures:
            print(f"  {item['incident_id']} ({item['scenario']})")
            for field, ok in item["correct"].items():
                if not ok:
                    print(
                        f"    {field}: predicted={item['prediction'][field]!r} "
                        f"expected={item['ground_truth'][field]!r}"
                    )


def main():
    parser = argparse.ArgumentParser(description="Evaluate the operations copilot.")
    parser.add_argument(
        "--max-incidents",
        type=int,
        default=None,
        help="Limit number of incidents (default: full dataset)",
    )
    parser.add_argument(
        "--output",
        default=REPORT_PATH,
        help=f"Path for JSON report (default: {REPORT_PATH})",
    )
    args = parser.parse_args()

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    incidents = data["incidents"]
    if args.max_incidents is not None:
        incidents = incidents[: args.max_incidents]

    results = []
    for index, incident in enumerate(incidents, start=1):
        incident_id = incident["incident_id"]
        print(f"[{index}/{len(incidents)}] Evaluating {incident_id}...")
        results.append(evaluate_incident(incident))

    summary = summarize(results)
    failures = [r for r in results if not r["all_correct"]]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dataset_path": DATASET_PATH,
        "eval_path": (
            "pipeline (preprocessor + correlation + classification + "
            "analyze + validation)"
        ),
        "labels_stripped": True,
        "summary": summary,
        "failures": failures,
        "results": results,
    }

    Path(args.output).parent.mkdir(exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print_summary(summary, failures)
    print(f"\nReport saved to: {args.output}")


if __name__ == "__main__":
    main()
