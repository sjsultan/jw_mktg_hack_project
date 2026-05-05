# Campaign OS — Pillar 1 (Platform)

## Context

Hackathon project at `github.com/benuchadnezzar/jw_mktg_hack_project` (seeded with BRIEF.md + README.md). The PRD reframes the product: Campaign OS is **the central campaign context layer** — a Postgres-backed schema that agents read and write, not a brief generator. "Campaign context is the durable asset" (PRD §3.2); "Execution happens inside Campaign OS" (§3.3). Asana/Slack/Confluence are notification layers, not the workflow.

**My scope: Pillar 1 (Platform) only.** Other teammates own Pillars 2 (Strategy Agent), 3 (Generation), 4 (Governance), 5 (Execution). Pillar 1 builds the foundation they plug into.

Pillar 1 deliverables per PRD §5:
- Working app shell + frontend
- Campaign object CRUD
- Postgres schema
- Agent runner interface (plug-in contract for pillars 2-5)
- Shared context directory
- MCP connection registry
- Stubbed integration interface (sandbox-by-default)
- Real auth (Google OAuth)
- Campaign MCP server exposed over HTTP

Deploy target: **GCP Cloud Run**. Winning narrative (PRD §12): *"We created the campaign context layer that future agents can execute from."*

**Critical safety rule from PRD §5.4** (transcript-derived): "Agents must not manipulate people or systems while communicating as the user." Pillar 1 enforces this at the platform level — sandbox mode is default, approvals are required rows in a table, integration stubs refuse to publish without an approval for the specific action.

## Architecture decision

**Single Next.js 14 App Router service on Cloud Run.** Frontend, REST API, MCP HTTP transport, and integration stubs all colocated. Matches `gm-planning-app` pattern — same Dockerfile, same `deploy.sh` skeleton, same Cloud SQL connector, same NextAuth pattern. One service, one deploy, one auth surface.

Rejected: split Next + Python FastAPI (doubles deploy surface; shared-context MCPs in `~/growth-marketing/capabilities/` are consumed over HTTP via the MCP registry, not embedded).

**Database**: Cloud SQL Postgres. New database `campaign_os` on existing `gm-planning-db` instance. Tables: `campaigns` (JSONB data + indexed top-level fields), `campaign_revisions` (append-only audit), `jobs` (async agent state), `approvals` (safety gate).

**Auth** (corrected — real auth, cloud-hosted):
- **UI**: NextAuth v4 with Google OAuth, Justworks workspace-only (hd-restricted). Copy auth config directly from [gm-planning-app](/Users/tbabcock/growth-marketing/apps/gm-planning-app). Session via `getServerSession(authOptions)` in API routes.
- **MCP / API (service-to-service)**: bearer token in `Authorization` header. Token stored in Secret Manager, rotatable. MCP clients (Claude Desktop, teammate agents, external Claude Code) authenticate via bearer.
- Middleware routes the check: a request to `/api/mcp` or `/api/agents/*` can authenticate via EITHER a NextAuth session OR a valid bearer. All other `/api/*` routes require a session. UI routes require a session.

**LLM**: `@anthropic-ai/vertex-sdk` via ADC (matches [loop.ts:18-21](/Users/tbabcock/growth-marketing/apps/gm-planning-app/lib/agent/loop.ts#L18-L21)). Project `teds-project-493922`, region `us-east5`. Model `claude-sonnet-4-6`. Prompt caching via `cache_control: {type: 'ephemeral'}`. *Note: Pillar 1 doesn't invoke the LLM directly — only ships the Vertex SDK + a shared `lib/llm/client.ts` helper that pillar-2-5 agents import.*

**MCP transport**: `@modelcontextprotocol/sdk` v1.x Streamable HTTP at `/api/mcp`. Single POST endpoint, JSON or SSE response. Gotcha: small adapter between `NextRequest` and the SDK's Node `http.*` types — budget ½ day. Fallback if it fights at 4 hrs: mount Express under `/api/mcp/[...path]`. Stdio is useless for Cloud Run.

**Long-running agents (>60s)**: orchestrator returns `{status: 'pending', job_id}` immediately, writes `jobs` row, executes via `waitUntil`. Client polls `/api/jobs/[id]`. Cloud Tasks + separate Cloud Run Job is Phase 2.

**Sandbox mode** (PRD §3.4): `SANDBOX=true` env var is the default. All `integrations/*` writes return `{preview: <payload>, published: false}` unless `SANDBOX=false` AND the campaign has a recorded approval row for that specific action.

**MCP registry** (PRD §5 Platform + §9): `integrations/mcp_registry.ts` holds connection config and bearer tokens for shared-context MCPs (brand-guidelines, content-repository, funnel-governance, etc.). Pillar-2-5 agents call `getMcp('brand-guidelines').callTool('get_voice_rules', {...})`. Credentials live at platform level in Secret Manager — never duplicated in agent code.

## Reuse vs. build

| Asset | Action | Source |
|---|---|---|
| `Dockerfile` | Copy unchanged | [gm-planning-app/Dockerfile](/Users/tbabcock/growth-marketing/apps/gm-planning-app/Dockerfile) |
| `deploy.sh` | Copy; rename IMAGE/SERVICE; delete lines 11-25 (context bundling — not needed) | [gm-planning-app/deploy.sh](/Users/tbabcock/growth-marketing/apps/gm-planning-app/deploy.sh) |
| `next.config.js`, `tsconfig.json` | Copy unchanged | gm-planning-app |
| `lib/db.ts` | Copy; change default DB to `campaign_os` | [gm-planning-app/lib/db.ts](/Users/tbabcock/growth-marketing/apps/gm-planning-app/lib/db.ts) |
| NextAuth config (Google OAuth, Justworks hd-restriction) | Copy verbatim | gm-planning-app `/lib/auth` and `/app/api/auth/[...nextauth]/route.ts` |
| Vertex SDK init | Copy verbatim (for `lib/llm/client.ts`) | loop.ts:18-21 |
| `scripts/snapshot-env.sh` | Copy unchanged | gm-planning-app |

Everything else: build new.

## Schema v1 (from PRD §6 — canonical)

Stored as JSONB `data` column. Zod validator uses `.passthrough()` at the API boundary (teammates will add fields hourly).

```
campaign { id, name, tier, status, created_by, created_at, updated_at }
strategy { objective, business_goal, funnel_stage, target_audience,
           audience_rationale, core_insight, core_message, timing,
           success_metrics[], open_questions[] }
audience { description, segments[], data_sources[], future_integrations[] }
messaging { pillars[], variants[], tone, proof_points[] }
channels[ { channel, role, strategy, required_assets[],
            operational_requirements[] } ]
creative { concepts[], assets[], approval_status }
operations { budget, timeline, campaign_name,
             tracking_requirements[], mops_requirements[],
             customer_io_requirements[], salesforce_requirements[],
             approval_checkpoints[] }
governance { status, checks[], risks[], required_approvals[] }
execution { confluence_page, asana_tasks[], slack_updates[], publish_status }
```

Indexed top-level columns (for query perf): `id` PK, `name`, `status`, `tier`, `created_by`, `updated_at`. Everything else in `data` JSONB with GIN index.

## Directory structure

```
jw_mktg_hack_project/
  README.md                           # exists
  BRIEF.md                            # exists
  PRD.md                              # write: full PRD from user's message
  TEAMMATE_AGENT_GUIDE.md             # write: plug-in recipe for pillars 2-5
  context/                            # PRD §8 — shared context files
    brand_guidelines.md
    messaging_guidelines.md
    campaign_hub.md
    funnel_taxonomy.md
    operational_requirements.md
    governance_rules.md               # codifies PRD §5.4 safety rules
    integration_policy.md
  integrations/                       # PRD §9
    types.ts                          # Integration interface
    confluence.ts                     # publish() — preview in sandbox
    asana.ts                          # createTasks() — preview in sandbox
    slack.ts                          # sendUpdate() — preview in sandbox
    mcp_registry.ts                   # getMcp(name), shared creds
  app/
    layout.tsx                        # NextAuth SessionProvider + shell
    page.tsx                          # landing: list campaigns
    campaigns/
      new/page.tsx                    # create empty campaign → redirect to detail
      [id]/page.tsx                   # split view: agent panel L, schema R
    api/
      auth/[...nextauth]/route.ts     # NextAuth handler
      health/route.ts
      campaigns/route.ts              # GET list, POST create
      campaigns/[id]/route.ts         # GET, PATCH, DELETE
      campaigns/[id]/revisions/route.ts
      campaigns/[id]/approve/route.ts # record action approval
      agents/[name]/route.ts          # orchestrator dispatch (no per-agent routes)
      jobs/[id]/route.ts              # poll async
      context/[file]/route.ts         # serve /context/*.md
      mcp/route.ts                    # MCP Streamable HTTP
  components/
    AgentPanel.tsx                    # list available agents, invoke, show results
    SchemaView.tsx                    # editable JSON tree of campaign data
    CampaignList.tsx
    ApprovalQueue.tsx                 # pending approvals for this campaign
  lib/
    db.ts                             # copied
    auth/
      options.ts                      # NextAuth config — copied from gm-planning-app
      middleware.ts                   # session OR bearer check
    llm/
      client.ts                       # Vertex SDK wrapper — shared by pillar agents
    schema/
      campaign.ts                     # Zod .passthrough()
    campaigns/
      repository.ts                   # CRUD
      revisions.ts                    # append-only audit
      approvals.ts                    # record/check action approvals
    agents/
      types.ts                        # Agent interface (plug-in contract)
      registry.ts                     # registerAgent / dispatch
      echo/
        index.ts                      # trivial seed agent — proves the plug-in path
    mcp/
      server.ts                       # MCP Server + tool list
      transport.ts                    # Next <-> StreamableHTTP adapter
      tools.ts                        # list/get/create/update/query + read_context
  db/
    schema.sql                        # campaigns + revisions + jobs + approvals
    seed.sql                          # example campaign
  docs/
    architecture.md                   # how the layers fit
  agents/                             # PRD §9 — per-pillar spec docs (teammates own these)
    strategy_agent.md                 # reference doc — Pillar 2 owner fills impl
    generation_agent.md
    governance_agent.md
    execution_agent.md
  scripts/
    migrate.sh                        # psql < db/schema.sql against Cloud SQL
    snapshot-env.sh                   # copied
  middleware.ts                       # applies auth/middleware
  Dockerfile
  deploy.sh
  next.config.js
  tsconfig.json
  package.json                        # @anthropic-ai/sdk, @anthropic-ai/vertex-sdk,
                                      # @modelcontextprotocol/sdk, next-auth, pg, zod,
                                      # swr, @google-cloud/cloud-sql-connector, next, react
```

No Pillar 2 code here. `lib/agents/strategy/` stays empty — Pillar 2 owner creates it.

## Teammate plug-in contract

The most important artifact. Write hour 1, paste to team channel.

```ts
// lib/agents/types.ts
export interface Agent {
  name: string                                  // 'strategy' | 'generation' | ...
  description: string
  run(input: { campaignId: string; payload?: unknown }): Promise<AgentResult>
}

export interface AgentResult {
  patch?: Partial<Campaign>                     // JSON-merge into campaign
  outputs?: Record<string, unknown>             // e.g. {confluence_preview_url}
  open_questions?: string[]                     // Strategy populates when info missing
  requires_approval?: {                         // MUST be set for external writes
    action: string                              // 'publish_confluence' | 'create_asana_task'
    preview: unknown                            // what will be sent
  }[]
  status: 'ok' | 'error' | 'pending'
  jobId?: string
}
```

Each pillar adds one file: `lib/agents/<name>/index.ts`, calls `registerAgent()` at module load. Zero platform code changes. The `requires_approval` field is the safety-rule enforcement hook — platform refuses external writes unless an `approvals` row exists for the specific action.

`TEAMMATE_AGENT_GUIDE.md` includes:
- The `Agent` interface
- A 15-line echo-agent example (the one seeded at `lib/agents/echo/`)
- How to read shared context: `const rules = await readContext('governance_rules.md')`
- How to call shared MCPs: `const res = await getMcp('brand-guidelines').callTool(...)`
- How to declare `requires_approval` instead of directly publishing

## Build sequence (ordered; each step independently demoable)

| # | Step | Est | Success criterion |
|---|---|---|---|
| 1 | Scaffold + deploy skeleton: `create-next-app`, copy Dockerfile/deploy.sh/next.config/tsconfig. Empty page live on Cloud Run at `campaign-os` service. | 2h | `curl <url>/api/health` → 200 |
| 2 | DB migration: `db/schema.sql` with 4 tables + GIN index. Run `scripts/migrate.sh` against Cloud SQL. | 1h | `\dt` shows 4 tables |
| 3 | **NextAuth Google OAuth**: copy config from gm-planning-app, Justworks workspace hd-restriction. NEXTAUTH_SECRET via Secret Manager. | 2h | Unauth'd → /api/auth/signin; auth'd Justworks account → session cookie set |
| 4 | Schema + REST CRUD: Zod `.passthrough()`, `/api/campaigns` POST/GET/PATCH/DELETE. Revisions auto-written on PATCH. Session-guarded. | 2h | curl round-trip with session: create → patch → `/revisions` shows 2 rows |
| 5 | Bearer auth for MCP/API: middleware accepts session OR bearer. Token in Secret Manager. | 1h | `/api/mcp` rejects no-auth, accepts bearer, accepts session |
| 6 | Context directory: create 7 files under `/context/`, `/api/context/[file]` route (session-guarded). Seed from `~/growth-marketing` equivalents where possible. | 1h | `curl /api/context/governance_rules.md` with session returns markdown |
| 7 | Integrations scaffolding: `integrations/types.ts` interface, confluence/asana/slack stubs returning `{preview, published:false}` under SANDBOX=true. `mcp_registry.ts` skeleton. | 1h | `integrations.confluence.publish({...})` returns preview object |
| 8 | Orchestrator + registry + `Agent` interface + seed echo agent. `/api/agents/[name]` dispatch. | 2h | `POST /api/agents/echo {campaignId, payload:{foo:'bar'}}` returns `{status:'ok', outputs:{echoed:{foo:'bar'}}}` |
| 9 | Frontend shell: landing (list), new-campaign (creates empty + redirects), detail (split view). `SchemaView` (editable JSON tree), `AgentPanel` (lists registered agents, invokes, renders result). `ApprovalQueue`. | 4h | Browser: sign in → create campaign → invoke echo agent → see result in panel → edit schema field → saves |
| 10 | **MCP HTTP transport** (highest risk): `StreamableHTTPServerTransport` at `/api/mcp`. Tools: `list_campaigns`, `get_campaign`, `create_campaign`, `update_campaign`, `query_campaigns`, `read_context`. | 4h | Claude Desktop connects with bearer; `tools/call get_campaign` returns JSON |
| 11 | Approval gate: `/api/campaigns/[id]/approve {action}` records approval. `approvals.ts` `requireApproval(campaignId, action)` check that integrations call before publishing. | 2h | Without approval: preview only. With approval + SANDBOX=false: mock-publishes |
| 12 | `TEAMMATE_AGENT_GUIDE.md` + PRD.md + agents/*.md stubs. Paste guide in team channel. Seed one demo campaign. | 1h | Teammate can open first PR without asking questions |

**Total: ~23 hours of focused agentic work.** Scoped so steps 1-9 alone deliver a working platform that pillars 2-5 can plug into. Steps 10-11 complete the "Campaign OS as infrastructure" story.

## Deployment

- **GCP project**: `teds-project-493922`
- **Region**: `us-east1` (Cloud Run) / `us-east5` (Vertex, for shared `lib/llm/client.ts`)
- **Artifact Registry**: `us-east1-docker.pkg.dev/teds-project-493922/campaign-os/app`
- **Cloud Run service**: `campaign-os`
- **Cloud SQL**: reuse `gm-planning-db` instance; new DB `campaign_os`
- **Secrets** (Secret Manager):
  - `POSTGRES_PASSWORD`
  - `NEXTAUTH_SECRET`
  - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` (can reuse gm-planning-app OAuth client or create new; callback URL must include `campaign-os` URL)
  - `MCP_BEARER_TOKEN`
- **Env vars**:
  - `CLOUD_SQL_INSTANCE_CONNECTION_NAME=teds-project-493922:us-east1:gm-planning-db`
  - `POSTGRES_DB=campaign_os`
  - `POSTGRES_USER=postgres`
  - `GOOGLE_CLOUD_PROJECT=teds-project-493922`
  - `NEXTAUTH_URL=https://<cloud-run-url>`
  - `SANDBOX=true`
- **Cold starts**: `min-instances=1` (~$15/mo) during demo window
- **Env updates**: `gcloud run services update ... --update-env-vars` only — never `--set-env-vars` (wipes unlisted vars per memory). Snapshot before changes.

## Verification

1. **Deploy**: `curl https://<url>/api/health` → 200.
2. **DB**: `psql \d campaigns` shows JSONB `data` + indexes; `\dt` shows 4 tables.
3. **Auth**: un-authenticated hit on `/` → redirected to `/api/auth/signin`. Non-Justworks Google account → access denied. Justworks Google account → session cookie, lands on campaign list.
4. **REST**: with session cookie, create → list → patch → revisions endpoint shows diff. Without session AND without bearer → 401.
5. **Bearer**: `curl -H "Authorization: Bearer $MCP_BEARER_TOKEN" /api/campaigns` → 200. Bad token → 401.
6. **Context**: `curl -H "Bearer ..." /api/context/governance_rules.md` → markdown.
7. **Sandbox**: `integrations.confluence.publish({campaignId, ...})` returns `{preview:..., published:false}` with `SANDBOX=true` (the default).
8. **Orchestrator**: `POST /api/agents/echo` returns `{status:'ok', outputs:{echoed:...}}` — proves teammate plug-in path works.
9. **Frontend**: sign in → create → detail page shows split view → invoke echo agent from panel → result renders → edit schema field → save → re-fetch shows edit + new revision.
10. **MCP** (infrastructure proof): add the Cloud Run MCP URL + bearer to a Claude Code session's `.mcp.json` → `tools/list` shows 6 tools → `get_campaign({id})` returns the JSON. **This is the "agents can pull from it" moment the brief's fork-in-road hinges on.**
11. **Approval gate**: with SANDBOX=false, `integrations.asana.createTasks({campaignId, tasks})` returns `{error: 'approval_required', action: 'create_asana_task'}`. POST `/api/campaigns/[id]/approve {action: 'create_asana_task'}` → retry → mock-publishes.
12. **Teammate integration test**: have one teammate clone the guide, add `lib/agents/<test>/index.ts` in a PR, verify their agent appears in `AgentPanel` and is invocable without any platform edit.

## Risks (ordered)

1. **MCP HTTP transport on Next.js App Router** — only non-paved-road piece. Box at 4 hrs; fall back to Express under `/api/mcp/[...path]`. Don't burn the hackathon on it.
2. **Teammate divergence on Agent interface** — write `types.ts` hour 1, paste in channel with the echo example. Include `requires_approval` from day 1; retrofit is painful.
3. **Schema churn across pillars** — JSONB + `.passthrough()` absorbs it. Tighten validators post-hackathon.
4. **Safety-rule enforcement slipping** — easy for a Pillar 5 teammate to bypass sandbox in their pillar. Provide the `requireApproval()` helper in `integrations/`; require all integration calls to route through it; contract-test during review.
5. **OAuth callback URL mismatch** — new Cloud Run URL needs to be added to the Google OAuth client's authorized redirects before sign-in works. Do this during step 3, not at demo time.
6. **Cold starts** — `min-instances=1` on deployed service during the demo window.
7. **Env wipe on redeploy** — `--update-env-vars` only; snapshot before changes per `scripts/snapshot-env.sh`.

## Critical files to reference during build

- [gm-planning-app/Dockerfile](/Users/tbabcock/growth-marketing/apps/gm-planning-app/Dockerfile)
- [gm-planning-app/deploy.sh](/Users/tbabcock/growth-marketing/apps/gm-planning-app/deploy.sh)
- [gm-planning-app/lib/db.ts](/Users/tbabcock/growth-marketing/apps/gm-planning-app/lib/db.ts)
- [gm-planning-app/lib/agent/loop.ts](/Users/tbabcock/growth-marketing/apps/gm-planning-app/lib/agent/loop.ts) — Vertex SDK init pattern for shared `lib/llm/client.ts`
- [gm-planning-app/scripts/snapshot-env.sh](/Users/tbabcock/growth-marketing/apps/gm-planning-app/scripts/snapshot-env.sh)
- gm-planning-app NextAuth config (to be located at step 3) — Google OAuth + Justworks hd-restriction
- `/tmp/jw_mktg_hack_project/BRIEF.md` — original framing, pillars, scope discipline
- User-provided PRD (to be written to repo as `PRD.md` step 1 of execution) — schema v1, safety rules, demo script
