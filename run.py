#!/usr/bin/env python3
"""Campaign OS — parse a brief or Granola transcript into a campaign schema.

Usage:
    python run.py --input transcripts/my-meeting.json [--output campaign.json]

To post results to Slack, ask Claude to read the output JSON and post via the Slack MCP.
"""
import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from agents.strategy_agent import parse_to_campaign
from sources.granola import load_transcript


def main() -> int:
    parser = argparse.ArgumentParser(description="Campaign OS: transcript/brief → campaign schema")
    parser.add_argument("--input", required=True, help="Path to Granola transcript or brief file")
    parser.add_argument("--output", default="campaign.json", help="Where to write the campaign JSON")
    args = parser.parse_args()

    print(f"Loading: {args.input}")
    text = load_transcript(args.input)

    print("Running Strategy Agent...")
    campaign = parse_to_campaign(text)
    campaign.id = str(uuid.uuid4())
    campaign.metadata.last_updated = datetime.now(timezone.utc).isoformat()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(campaign.model_dump(), indent=2))

    print(f"\nCampaign written to {args.output}")
    print(f"  Name:      {campaign.name or '(not found)'}")
    print(f"  Objective: {campaign.objective or '(not found)'}")
    print(f"  Channels:  {[c.type for c in campaign.channels] or []}")
    print(f"  Audience:  {campaign.audience.description[:80] + '...' if len(campaign.audience.description) > 80 else campaign.audience.description or '(not found)'}")

    if campaign.governance.issues:
        print(f"\nGovernance flags:")
        for issue in campaign.governance.issues:
            print(f"  ⚠️  {issue}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
