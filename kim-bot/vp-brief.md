# /vp-brief — VP Context Brief Generator

Generate a synthesized weekly brief from the VP's meeting notes and Slack activity, review it with them, and post it to `#mkt-vp-context-feed` for their team.

---

**Instructions for Claude**:

You are running the VP Brief skill for a Justworks marketing leader. Your job is to synthesize this week's context into a structured, approvable brief — then post it to Slack only after the VP confirms.

---

## Step 1 — Pull Granola meeting notes

Use the Granola MCP. Get this week's meetings, then pull the notes for each one (cap at 10 to keep it fast).

For every meeting, extract:
- **Decisions made** (the VP confirmed or directed something)
- **Action items the VP owns**
- **Directional signals** (priorities, things they emphasized, pushback they gave)

Skip 1:1s with reports unless something clearly team-relevant came up.

---

## Step 2 — Pull recent Slack activity

Use `slack_search_public_and_private` to find the VP's recent messages.

Query: `from:@<VP slack handle>` over the last 3 business days. If you don't know the handle, ask the VP first. Pull the most recent ~30 messages.

Filter for signal:
- Decisions communicated to the team
- Priorities stated explicitly
- Changes in direction
- Commitments made publicly

Ignore reactions, "thanks", scheduling chatter, etc.

---

## Step 3 — Synthesize the brief

Produce a structured brief in this exact format:

```
**[VP Name]'s Brief — Week of [Date]**

**Decisions made**
• [Confirmed decision — one specific line each]

**Current priorities**
• [What the VP is focused on this week and why it matters to the team]

**What's still open**
• [Unresolved questions or pending decisions ICs should know about]

**Heads up**
• [Anything coming that creates work or dependencies for the team]
```

Rules:
- 10 bullets max total across all sections
- One line per bullet, no nested sub-bullets
- Be specific: "decided to pause UGC pilot until Q3 budget review" not "discussed UGC"
- No fluff, no hedging, no AI-speak ("synergize", "leverage")

### Example output

```
**Kim Ryneska's Brief — Week of May 4, 2026**

**Decisions made**
• Paused UGC pilot until Q3 budget review (June 15)
• Approved brand refresh kickoff with Studio for June
• Killed the Tuesday newsletter — moving content to LinkedIn instead

**Current priorities**
• Q2 close-out — every team must hit pipeline targets
• Brand refresh discovery (Studio + Marketing leads)

**What's still open**
• Whether we sponsor INBOUND 2026 — decision by May 15
• New social agency RFP — short list landing this week

**Heads up**
• I'll be in London May 18-22 — async only those days
• Budget reforecast meeting Friday, ICs will see new targets next week
```

---

## Step 4 — Approval gate (REQUIRED)

Show the VP the brief and ask:

> "Here's your brief for this week. Anything to add, remove, or mark as not-for-sharing before I post it to #mkt-vp-context-feed?"

Wait for explicit approval (e.g. "approve", "looks good", "post it", "yes"). If they request edits, make them and re-confirm before posting. **Never post without explicit approval — even if they said yes earlier in the session.**

---

## Step 5 — Post to #mkt-vp-context-feed

Once approved, call `slack_send_message` with:
- `channel_id`: `C0B2N1L446L`
- `text`: the message below

Header format (so `/ask-kim` queries can identify it):

```
📋 *VP Brief | [VP Name] | [Date]*
```

Then the full approved brief beneath it.

After posting, confirm to the VP: "Posted — your brief is now queryable by the team via `/ask-kim`."
