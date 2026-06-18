from classification_engine import classify_incident
from copilot import analyze_incident
from correlation_engine import calculate_correlation_context
from incident_preprocessor import prepare_incident_for_inference
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

    return {
        "incident_id": clean_incident.get("incident_id"),
        "correlation_context": correlation_context,
        "deterministic_classification": deterministic_classification,
        "analysis": prediction,
    }
