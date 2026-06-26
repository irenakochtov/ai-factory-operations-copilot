import json
import os
from openai import OpenAI


def _build_commander_prompt(commander_context: dict) -> str:
    compact_context = {
        "site_status": commander_context.get("site_status"),
        "incident_count": commander_context.get("incident_count"),
        "highest_priority_incident": commander_context.get("highest_priority_incident"),
        "primary_operational_risk": commander_context.get("primary_operational_risk"),
        "incident_type_distribution": commander_context.get("incident_type_distribution"),
        "affected_domains": commander_context.get("affected_domains"),
        "recommended_teams": commander_context.get("recommended_teams"),
        "minimum_time_to_critical_minutes": commander_context.get(
            "minimum_time_to_critical_minutes"
        ),
        "response_plan": commander_context.get("response_plan"),
        "incident_reports": [
            {
                "incident_id": report.get("incident_id"),
                "incident_type": report.get("analysis", {}).get("incident_type"),
                "severity": report.get("analysis", {}).get("severity"),
                "root_cause": report.get("analysis", {}).get("root_cause"),
                "business_impact": report.get("analysis", {}).get("business_impact"),
                "predicted_next_failure": report.get("analysis", {}).get(
                    "predicted_next_failure"
                ),
                "priority_score": report.get("analysis", {}).get("priority_score"),
                "time_to_critical_minutes": report.get("analysis", {}).get(
                    "time_to_critical_minutes"
                ),
                "recommended_action": report.get("analysis", {}).get(
                    "recommended_action"
                ),
                "recommended_workload_action": report.get("analysis", {}).get(
                    "recommended_workload_action"
                ),
                "similar_incidents": report.get("analysis", {}).get(
                    "similar_incidents"
                ),
            }
            for report in commander_context.get("incident_reports", [])
        ],
    }

    return f"""
You are an Incident Commander Agent for an AI Factory operations center.

You receive already-analyzed infrastructure incidents from lower-level operational agents.
Your job is to create one executive operational situation report.

Return ONLY valid JSON.

Required JSON schema:
{{
  "executive_briefing": "short executive summary",
  "overall_site_status": "stable | elevated | high_risk | critical",
  "primary_operational_risk": "main risk domain",
  "response_priority": [
    "first action",
    "second action",
    "third action"
  ],
  "safest_operational_strategy": "recommended strategy",
  "automation_recommendation": {{
    "approved": true,
    "action": "safe automation action or none",
    "reason": "why this is safe or unsafe"
  }},
  "human_validation_required": true,
  "business_impact_summary": "business impact",
  "executive_message": "one paragraph for NOC or operations leadership"
}}

Rules:
- Prioritize human safety and infrastructure safety.
- Do not recommend automated physical remediation for power, cooling, or security systems.
- Workload migration or pausing non-critical workloads may be considered safe automation.
- If power or cooling risk is critical, require human field validation.
- Keep the answer concise and operational.

Commander context:
{json.dumps(compact_context, indent=2)}
"""


def generate_executive_commander_report(commander_context: dict) -> dict:
    api_key = os.getenv("NEBIUS_API_KEY")
    base_url = os.getenv("NEBIUS_BASE_URL")
    model = os.getenv("NEBIUS_MODEL")

    if not api_key or not base_url or not model:
        return {
            "error": "Missing Nebius model configuration",
            "required_env_vars": [
                "NEBIUS_API_KEY",
                "NEBIUS_BASE_URL",
                "NEBIUS_MODEL",
            ],
        }

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    prompt = _build_commander_prompt(commander_context)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a precise AI Factory Incident Commander Agent. Return only valid JSON.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        max_tokens=900,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "error": "Commander Agent returned non-JSON response",
            "raw_response": content,
        }