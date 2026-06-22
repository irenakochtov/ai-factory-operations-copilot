from collections import defaultdict


def build_incident_clusters(analyses: list) -> dict:
    groups = defaultdict(list)

    for item in analyses:
        analysis = item.get("analysis", {})
        incident_type = analysis.get("incident_type")

        if not incident_type:
            continue

        groups[incident_type].append(
            item.get("incident_id")
        )

    clusters = []

    for incident_type, incidents in groups.items():

        if len(incidents) < 2:
            continue

        confidence = min(
            99,
            70 + (len(incidents) * 5),
        )

        clusters.append(
            {
                "suspected_common_cause": incident_type,
                "incident_count": len(incidents),
                "confidence": confidence,
                "incidents": incidents,
            }
        )

    clusters.sort(
        key=lambda x: x["incident_count"],
        reverse=True,
    )

    return {
        "total_clusters": len(clusters),
        "clusters": clusters,
    }