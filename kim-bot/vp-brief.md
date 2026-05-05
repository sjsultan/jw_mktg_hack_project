# /vp-brief — VP Context Brief Generator

Generate a synthesized weekly brief from your meeting notes and Slack activity, review it, and post it to the shared VP context feed for your team.

---

**Instructions for Claude**:

You are running the VP Brief skill for a Justworks marketing leader. Your job is to synthesize this week's context into a structured, approvable brief — then post it to Slack after the VP confirms it's good to share.

**Step 1 — Pull Granola meeting notes**
Call `list_meetings` with `time_range: "this_week"` to get this week's meetings.
Then call `get_meetings` for all meetings this week (batch, max 10).
Extract from each meeting: decisions made, action items owned by the VP, and any directional signals.

**Step 2 — Pull recent Slack signals**
Search Slack for messages `from:<VP's user ID>` in the last 3 business days across public channels and DMs.
Focus on: decisions communicated, priorities stated, changes in direction, commitments made.

**Step 3 — Synthesize the brief**
Produce a structured brief in this format:

```
**[VP Name]'s Brief — Week of [Date]**

**Decisions made**
• [Each confirmed decision — be specific, one line each]

**Current priorities**
• [What the VP is focused on this week and why it matters]

**What's still open**
• [Unresolved questions or pending decisions the team should know about]

**Heads up**
• [Anything coming that will create work or dependencies for the team]
```

Keep it tight — 10 bullets max total. No fluff. This is what ICs will query against.

**Step 4 — Approval gate**
Show the VP the brief and ask:

> "Here's your brief for this week. Anything to add, remove, or mark as not-for-sharing before I post it to #vp-context-feed?"

Wait for their response. If they say approve / looks good / post it / yes — proceed to Step 5.
If they request edits, make them and confirm again before posting.

**Step 5 — Post to #vp-context-feed**
Post the approved brief to the Slack channel `#vp-context-feed` (channel ID: to be configured).
Use this header format so IC queries can identify it:

```
📋 *VP Brief | [VP Name] | [Date]*
```

Then paste the full approved brief below it.

Confirm to the VP that it's been posted and is now queryable by the team.
