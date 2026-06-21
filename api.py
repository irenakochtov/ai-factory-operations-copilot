import json
import os
from typing import Literal, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from pipeline import run_analysis_pipeline, run_correlation_context
from prometheus_adapter import convert_alert_to_incident

DATASET_PATH = "dataset_v2.json"

app = FastAPI(
    title="AI Factory Operations Copilot",
    description="AI-powered incident triage API for AI factories and data center operations.",
    version="0.7.1",
)


class PrometheusAlert(BaseModel):
    alertname: Literal[
        "HighGPUTemperature",
        "IBPacketLoss",
        "StorageLatency",
    ]

    rack_id: str = Field(..., examples=["RACK-01"])

    gpu_id: Optional[str] = Field(None, examples=["GPU-07"])
    temperature: Optional[float] = Field(None, examples=[92])
    packet_loss_pct: Optional[float] = Field(None, examples=[1.8])
    p99_latency_ms: Optional[float] = Field(None, examples=[240])
    threshold: float = Field(..., examples=[85])


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


def validate_alert_payload(alert: dict):
    alertname = alert.get("alertname")

    if alertname == "HighGPUTemperature":
        required = ["rack_id", "gpu_id", "temperature", "threshold"]
    elif alertname == "IBPacketLoss":
        required = ["rack_id", "packet_loss_pct", "threshold"]
    elif alertname == "StorageLatency":
        required = ["rack_id", "p99_latency_ms", "threshold"]
    else:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported alertname: {alertname}",
        )

    missing = [field for field in required if field not in alert or alert[field] is None]

    if missing:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Missing required fields for alert type",
                "alertname": alertname,
                "missing_fields": missing,
            },
        )


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "AI Factory Operations Copilot",
        "version": "0.7.1",
    }


@app.get("/debug-env")
def debug_env():
    return {
        "has_nebius_api_key": bool(os.getenv("NEBIUS_API_KEY")),
        "nebius_base_url": os.getenv("NEBIUS_BASE_URL"),
        "nebius_model": os.getenv("NEBIUS_MODEL"),
        "max_llm_calls_per_run": os.getenv("MAX_LLM_CALLS_PER_RUN"),
        "llm_max_output_tokens": os.getenv("LLM_MAX_OUTPUT_TOKENS"),
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
    correlation_context = run_correlation_context(incident)

    return {
        "incident_id": incident_id,
        "correlation_context": correlation_context,
    }


@app.post("/analyze/{incident_id}")
def analyze_by_incident_id(incident_id: str):
    incident = find_incident_by_id(incident_id)
    return run_analysis_pipeline(incident)


@app.post("/analyze_alert")
def analyze_alert(alert: PrometheusAlert):
    alert_dict = alert.model_dump(exclude_none=True)

    validate_alert_payload(alert_dict)

    incident = convert_alert_to_incident(alert_dict)
    result = run_analysis_pipeline(incident)

    return {
        "input_alert": alert_dict,
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