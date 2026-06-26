"""Maps a deterministic incident_type to its specialized agent system prompt."""

from agent_prompts import (
    COOLING_SYSTEM_PROMPT,
    ENVIRONMENTAL_SYSTEM_PROMPT,
    GENERALIST_SYSTEM_PROMPT,
    HARDWARE_SYSTEM_PROMPT,
    NETWORK_SYSTEM_PROMPT,
    POWER_SYSTEM_PROMPT,
    SECURITY_SYSTEM_PROMPT,
    STORAGE_SYSTEM_PROMPT,
)

AGENT_REGISTRY = {
    "cooling_risk": COOLING_SYSTEM_PROMPT,
    "power_risk": POWER_SYSTEM_PROMPT,
    "security_risk": SECURITY_SYSTEM_PROMPT,
    "network_risk": NETWORK_SYSTEM_PROMPT,
    "storage_risk": STORAGE_SYSTEM_PROMPT,
    "environmental_risk": ENVIRONMENTAL_SYSTEM_PROMPT,
    "hardware_risk": HARDWARE_SYSTEM_PROMPT,
}

FALLBACK_AGENT_PROMPT = GENERALIST_SYSTEM_PROMPT


def get_agent_prompt(incident_type: str) -> str:
    """Return the specialized system prompt for an incident_type.

    Falls back to the generalist prompt for unknown or missing types.
    """
    return AGENT_REGISTRY.get(incident_type, FALLBACK_AGENT_PROMPT)
