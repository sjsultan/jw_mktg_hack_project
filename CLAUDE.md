# Campaign OS

Campaign schema + AI agents that parse marketing briefs and Granola transcripts into structured campaigns, then notify Slack.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env.local   # fill in LITELLM or ANTHROPIC_API_KEY + SLACK_WEBHOOK_URL
```

## Run

```bash
# From a saved transcript or brief:
python run.py --input transcripts/meeting.json

# With Slack notification:
python run.py --input transcripts/meeting.json --slack

# From any text file (brief, doc, etc.):
python run.py --input brief.txt --slack --output campaigns/q3-launch.json
```

## Fetching a Granola transcript

Granola is connected via MCP in this Claude Code session (OAuth already done). Ask Claude:

> "List my recent Granola meetings"
> "Fetch the transcript for [meeting title] and save it to transcripts/[name].json"

Claude will call `mcp__granola__list_meetings` and `mcp__granola__get_meeting_transcript`, then write the file. Then run `run.py --input transcripts/<file>.json`.

## Posting to Slack

Slack is connected via MCP plugin in Claude Code (already OAuth'd — no setup needed).

After running `run.py`, ask Claude: "Post the campaign from campaigns/<file>.json to #<channel>"

Claude will read the JSON and use the Slack MCP to post a formatted summary.

## Project structure

```
schema/campaign.py      — Pydantic Campaign model (source of truth)
agents/strategy_agent.py — Claude API: text → Campaign schema
sources/granola.py      — reads saved Granola transcript files
outputs/slack.py        — posts campaign summary via Slack webhook
run.py                  — CLI entry point
transcripts/            — drop Granola JSON files here
```

## Schema

The `Campaign` object (defined in `schema/campaign.py`) is the central data model all agents read/write. See `BRIEF.md` for full architecture.
