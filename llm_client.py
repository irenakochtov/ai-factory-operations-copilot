import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

REQUIRED_ENV_VARS = ["NEBIUS_API_KEY", "NEBIUS_BASE_URL", "NEBIUS_MODEL"]


def _missing_env_vars() -> list:
    return [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]


def _parse_json(text: str) -> dict:
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        pass

    match = re.search(r"\{.*\}", text or "", re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return {
        "error": "LLM returned non-JSON response",
        "raw_response": text,
    }


def run_json_agent(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
    max_tokens: int = 900,
) -> dict:
    missing = _missing_env_vars()
    if missing:
        return {
            "error": "Missing Nebius model configuration",
            "missing_env_vars": missing,
            "required_env_vars": list(REQUIRED_ENV_VARS),
        }

    client = OpenAI(
        api_key=os.getenv("NEBIUS_API_KEY"),
        base_url=os.getenv("NEBIUS_BASE_URL"),
    )

    response = client.chat.completions.create(
        model=os.getenv("NEBIUS_MODEL"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    content = response.choices[0].message.content
    return _parse_json(content)
