import json

from fastapi import FastAPI, HTTPException

from classification_engine import classify_incident
from copilot import analyze_incident
from correlation_engine import calculate_correlation_context
from incident_preprocessor import prepare_incident_for_inference
from prometheus_adapter import convert_alert_to_incident
from rules_engine import apply_operational_rules

DATASET_PATH = "dataset_v2.json"

app = FastAPI(
    title="AI Factory Operations Copilot",
    description="AI-powered incident triage API for AI factories and data center operations.",
    version="0.6.0",
)


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def find_incident_by_id(incident_id: str):
    data = load_dataset()

    for incident in data["incidents"]:
        if incident["incident_id"] == incident_id:
            return incident

    raise HTTPException(
        status_code=404,
        detail=f"Incident {incident_id} not found",
    )


def run_analysis_pipeline(incident: dict) -> dict:
    clean_incident = prepare_incident_for_inference(incident)

    correlation_context = calculate_correlation_context(clean_incident)

    deterministic_classification = classify_incident(clean_incident)

    enriched_incident = {
        "incident": clean_incident,
        "correlation_context": correlation_context,
        "deterministic_classification": deterministic_classification,
    }

    prediction = analyze_incident(enriched_incident)

    prediction = apply_operational_rules(
        clean_incident,
        prediction,
    )

    return {
        "incident_id": clean_incident.get("incident_id"),
        "correlation_context": correlation_context,
        "deterministic_classification": deterministic_classification,
        "analysis": prediction,
    }


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "AI Factory Operations Copilot",
        "version": "0.6.0",
    }


@app.get("/incidents")
def list_incidents():
    data = load_dataset()

    return {
        "total": len(data["incidents"]),
        "incidents": [
            {
                "incident_id": incident["incident_id"],
                "site": incident.get("site"),
                "rack_id": incident.get("rack_id"),
                "scenario": incident.get("scenario"),
            }
            for incident in data["incidents"]
        ],
    }


@app.get("/correlation/{incident_id}")
def get_correlation_context(incident_id: str):
    incident = find_incident_by_id(incident_id)
    clean_incident = prepare_incident_for_inference(incident)
    correlation_context = calculate_correlation_context(clean_incident)

    return {
        "incident_id": incident_id,
        "correlation_context": correlation_context,
    }


@app.post("/analyze/{incident_id}")
def analyze_by_incident_id(incident_id: str):
    incident = find_incident_by_id(incident_id)
    return run_analysis_pipeline(incident)


@app.post("/analyze_alert")
def analyze_alert(alert: dict):
    incident = convert_alert_to_incident(alert)
    result = run_analysis_pipeline(incident)

    return {
        "input_alert": alert,
        **result,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )