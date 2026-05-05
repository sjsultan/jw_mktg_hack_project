import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from llm_client import get_client, DEFAULT_MODEL
from schema.campaign import Campaign

SYSTEM_PROMPT = """You are a Campaign Strategy Agent for a B2B SaaS company.

Parse the provided text — which may be a meeting transcript, campaign brief, freeform notes, or a mix — and extract structured campaign information.

Return ONLY a single JSON object. Use the exact field names from the schema. Leave fields as empty strings or empty arrays when information is absent — do not invent details.

Be specific: extract real names, channels, timelines, and messaging from the text rather than using generic placeholders."""


def parse_to_campaign(text: str, model: str = DEFAULT_MODEL) -> Campaign:
    client = get_client()
    schema_str = json.dumps(Campaign.model_json_schema(), indent=2)

    resp = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Parse this input into the Campaign schema below.\n\n"
                    f"--- INPUT ---\n{text}\n\n"
                    f"--- SCHEMA ---\n{schema_str}\n\n"
                    "Return ONLY valid JSON. No prose, no markdown fences."
                ),
            }
        ],
    )

    raw = "".join(b.text for b in resp.content if b.type == "text").strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    data = json.loads(raw)
    return Campaign(**data)
