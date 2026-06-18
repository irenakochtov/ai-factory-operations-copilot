import copy


def prepare_incident_for_inference(incident: dict) -> dict:
    """
    Remove fields that should never be visible
    to the model during inference.
    """

    clean_incident = copy.deepcopy(incident)

    clean_incident.pop("ground_truth", None)
    clean_incident.pop("scenario", None)

    return clean_incident
    