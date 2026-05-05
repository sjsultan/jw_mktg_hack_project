# Campaign OS — Product Brief

> This is not a campaign generator.
> It is a **Campaign OS**: a system that structures campaign intelligence into a canonical schema, enables AI agents to operate on that schema, and orchestrates strategy, generation, governance, and execution.

**Core idea:** instead of pushing outputs directly into tools, create a central campaign context layer that other agents and systems can read from.

---

## 1. Reframed Product Definition

A Campaign OS — not a generator. A structured campaign context layer with agents operating on top.

---

## 2. Product Principles

1. AI is the operating layer, not a feature.
2. Build for agents + workflows, not just human prompting.
3. Prioritize reusability, shareability, and automation.
4. Bridge the gap from "AI as chat partner" → "AI as execution system."

---

## 3. System Architecture — 5 Layers

### 1. Input Layer
- Campaign brief upload (docs, transcripts, freeform)
- Guided input (Q&A)

### 2. Strategy Layer
Normalize into structured campaign schema:
- Goals
- Audience
- Messaging
- Channels
- Timing

### 3. Generation Layer
Create:
- Audience segments
- Messaging variants
- Creative directions
- Channel plans

### 4. Governance Layer
Validate:
- Completeness
- Logical consistency
- Brand / compliance rules
- Operational requirements

### 5. Execution Layer
Publish to:
- Confluence (source of truth)
- Asana (optional tasks)

Trigger:
- Slack notifications
- Agent workflows
- Future: downstream systems (ads, lifecycle, etc.)

---

## 4. Key Architectural Insight

> "Create a database / MCP for campaigns that other agents can pull from."

### Campaign Context Engine (Core Asset)

We are building:
- A structured campaign database
- With a defined schema
- That becomes the source of truth for all campaign-related agents

This unlocks:
- Google Ads agent
- Lifecycle agent
- Reporting agent
- Optimization agent

Without this, we just have a generator.

---

## 5. Campaign Schema (v1)

Claude Code should treat this as the central object model.

```
Campaign {
  id
  name
  objective
  audience {
    description
    segments
    source
  }
  messaging {
    pillars
    variants
    tone
  }
  channels [
    {
      type
      strategy
      assets
    }
  ]
  creative {
    concepts
    assets
    status
  }
  operations {
    budget
    timeline
    campaign_name
    requirements
  }
  governance {
    checks_passed
    issues
  }
  outputs {
    confluence_url
    asana_project_id
  }
  metadata {
    created_by
    last_updated
  }
}
```

---

## 6. Product Workflow

1. User inputs campaign OR uploads doc/transcript.
2. **Strategy Agent**: parses → structured schema.
3. **Generation Agents**: fill missing pieces; generate messaging, audiences, channels.
4. **Governance Agent**: validates + flags gaps.
5. **Execution Agent**: publishes to Confluence; optionally creates Asana artifacts.
6. **Agent Loop**: weekly updates via Slack; suggests changes.

---

## 7. Core Features

### 1. Campaign Builder
- Guided Q&A
- Upload + parse

### 2. Waterfall Workflow
Step-by-step campaign construction: Audience → Channels → Messaging → Ops

### 3. Content Engine
- Generate messaging
- Remix from existing content

### 4. Execution Outputs
- Confluence (primary)
- Asana (secondary or optional)

### 5. Agent System
- Scheduled updates (cron)
- Slack notifications
- Optimization suggestions

### 6. Sandbox Mode
- Simulate integrations
- No writes to production systems

---

## 8. Project Plan for Claude Code

Build a modular system with:
- A shared campaign schema
- Independent agents operating on that schema
- A simple UI to orchestrate flow

---

## 9. System Decomposition — 5 Build Pillars

### Pillar 1: Platform (Core Infrastructure)
**Owns:** backend, database (campaign schema), API layer, agent orchestration framework.

**Deliverables:**
- Campaign schema storage
- CRUD operations
- Agent execution framework
- MCP-style connectors (stubbed)

### Pillar 2: Strategy Agent
**Function:** convert inputs → structured campaign.

**Inputs:** text, transcript (Granola), partial inputs.

**Outputs:** populated campaign schema (partial or full).

### Pillar 3: Generation Engine
**Function:** fill and expand campaign.

**Includes:** audience generation, messaging generation, channel planning, creative ideation.

### Pillar 4: Governance Layer
**Function:** prevent bad outputs.

**Checks:** missing fields, logical inconsistencies, operational gaps, optional brand rules.

### Pillar 5: Execution + Integrations
**Function:** push outputs externally.

**MVP:** Confluence publishing; optional Asana project creation.

**Future:** Slack bot, ads integrations, lifecycle tools.

---

## 10. Frontend Requirements

### UI v1
- Chat + structured panel hybrid
- Step-based flow: Input → Strategy → Build → Review → Publish

### Key Constraints
- Must visualize the campaign schema
- Must allow editing before execution

---

## 11. Hackathon Scope (Realistic)

### Build
- Campaign schema
- Strategy agent (basic parsing)
- Generation (messaging + channels)
- Confluence output (mock or real)
- Basic UI or CLI

### Do NOT Overbuild
- Deep integrations
- Real data pipelines
- Full agent loops

---

## 12. Execution Plan (Phased)

### Phase 1: Hackathon (Prototype)
- Schema
- Strategy parsing
- Basic generation
- Output to doc

### Phase 2: Internal Tool
- UI
- Real integrations
- Workflow polish

### Phase 3: Platform
- Agent ecosystem
- External integrations
- Optimization loops

---

## 13. Critical Pushback

> "I know it's a fancy campaign generator."

That's the trap.

If we:
- Push directly to Asana
- Generate tasks
- Stop there

We've built a disposable tool.

If instead we:
- Build a structured campaign context layer
- Enable agents to operate on it

We're building infrastructure. **That's the fork in the road.**

---

## 14. What Claude Code Should Optimize For

- Treat campaign schema as source of truth
- Make agents stateless but schema-driven
- Keep integrations loosely coupled
- Prioritize extensibility over completeness
- Enable multi-agent orchestration later
