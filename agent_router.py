"""Lightweight deterministic router for domain-specific operational agents.

Selects a specialized system prompt based on deterministic_classification.incident_type,
then runs the shared LLM agent. The user prompt, response schema, output rules, and
sampling settings are identical to the original Operational Copilot so the output
schema and evaluation results remain unchanged.
"""

import json

from agent_prompts import OUTPUT_RULES, RESPONSE_SCHEMA
from agent_registry import get_agent_prompt
from llm_client import run_json_agent

AGENT_TEMPERATURE = 0
AGENT_MAX_TOKENS = 1100


def _build_user_prompt(enriched_incident: dict, deterministic_classification: dict) -> str:
    return f"""Required JSON schema:
{RESPONSE_SCHEMA}

{OUTPUT_RULES}

Deterministic Classification:
{json.dumps(deterministic_classification, indent=2)}

Incident:
{json.dumps(enriched_incident, indent=2)}
"""


def analyze_with_routed_agent(enriched_incident: dict) -> dict:
    deterministic_classification = enriched_incident.get(
        "deterministic_classification",
        {},
    )

    incident_type = deterministic_classification.get("incident_type")
    system_prompt = get_agent_prompt(incident_type)

    user_prompt = _build_user_prompt(
        enriched_incident,
        deterministic_classification,
    )

    return run_json_agent(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=AGENT_TEMPERATURE,
        max_tokens=AGENT_MAX_TOKENS,
    )
