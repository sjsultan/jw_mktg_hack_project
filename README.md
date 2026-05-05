# jw_mktg_hack_project — Campaign OS

Hackathon project building a **Campaign OS**: a structured campaign context layer with AI agents that operate on it. Not a generator — infrastructure.

## Start here

- **[BRIEF.md](./BRIEF.md)** — full product brief, schema, architecture, and scope.

## Pillars

Work is divided into five pillars. Claim one in a PR or in the team channel before starting.

| # | Pillar | Owns |
|---|--------|------|
| 1 | Platform | Schema storage, CRUD, agent orchestration framework, MCP-style connectors |
| 2 | Strategy Agent | Parse inputs (text, transcripts) → populated campaign schema |
| 3 | Generation Engine | Audience, messaging, channel plans, creative ideation |
| 4 | Governance Layer | Completeness, consistency, brand/compliance, operational checks |
| 5 | Execution + Integrations | Confluence publish (primary), Asana (optional) |

## Hackathon scope

**Build:** schema · strategy parsing · basic generation · Confluence output (mock or real) · basic UI or CLI.

**Do NOT overbuild:** deep integrations, real data pipelines, full agent loops.

## Contributing

1. Branch off `main`: `git checkout -b <pillar>/<short-description>`
2. Open a PR against `main` when ready for review.
3. Keep pillars loosely coupled — agents should be stateless and operate on the schema.
