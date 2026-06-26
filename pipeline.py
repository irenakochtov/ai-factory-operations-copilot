from cascade_engine import build_failure_cascade
from classification_engine import classify_incident
from copilot import analyze_incident
from correlation_engine import calculate_correlation_context
from forecast_engine import generate_failure_forecast
from incident_history_engine import find_similar_incidents
from incident_preprocessor import prepare_incident_for_inference
from sla_engine import assess_sla_risk
from validation_engine import enforce_deterministic_classification


def run_correlation_context(incident: dict) -> dict:
    clean_incident = prepare_incident_for_inference(incident)
    return calculate_correlation_context(clean_incident)


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

    prediction = enforce_deterministic_classification(
        prediction,
        deterministic_classification,
    )

    prediction["failure_forecast"] = generate_failure_forecast(
        incident_type=prediction.get("incident_type"),
        severity=prediction.get("severity"),
        time_to_critical_minutes=prediction.get("time_to_critical_minutes"),
    )

    prediction["failure_cascade"] = build_failure_cascade(
        prediction.get("incident_type"),
    )

    prediction["similar_incidents"] = find_similar_incidents(
        {
            **clean_incident,
            "incident_type": prediction.get("incident_type"),
        }
    )

    prediction["sla_assessment"] = assess_sla_risk(
        incident=clean_incident,
        analysis=prediction,
    )

    return {
        "incident_id": clean_incident.get("incident_id"),
        "correlation_context": correlation_context,
        "deterministic_classification": deterministic_classification,
        "analysis": prediction,
    }