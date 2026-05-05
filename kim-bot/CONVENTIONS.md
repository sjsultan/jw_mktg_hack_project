# Kim Bot — Brief Conventions

The format contract every VP brief must follow. The `/vp-brief` skill produces this shape automatically; if a VP writes one manually, follow the same rules so `/ask-kim` and `/vp-digest` can parse it.

---

## Header (required)

Every brief starts with this exact line, on its own:

```
📋 *VP Brief | [VP Name] | [Date]*
```

- **Emoji**: `📋` — used by the IC query and digest skills to identify briefs in the channel
- **VP Name**: full name (e.g. `Kim Ryneska`, not `Kim` or `KR`)
- **Date**: `Month D, YYYY` format (e.g. `May 4, 2026`)

If the header is malformed, downstream skills will not find the brief.

---

## Sections

Always in this order. Skip sections that have nothing for the week — don't write "none" or "N/A".

### Decisions made
What was confirmed or directed this week. Past tense. One specific line each.

✅ "Paused UGC pilot until Q3 budget review (June 15)"
❌ "Discussed UGC initiative"

### Current priorities
What the VP is focused on this week and why it matters. Present tense.

✅ "Q2 close-out — every team must hit pipeline targets"
❌ "Working on stuff"

### What's still open
Pending decisions or unresolved questions ICs should know about.

✅ "Whether we sponsor INBOUND 2026 — decision by May 15"
❌ "TBD"

### Heads up
Anything coming that creates work or dependencies for the team.

✅ "I'll be in London May 18-22 — async only those days"
❌ "FYI"

---

## Hard rules

- **10 bullets max** total across all sections
- **One line per bullet** — no nested sub-bullets, no paragraphs
- **No fluff** — if you wouldn't say it in a 1:1 with an IC, don't put it in the brief
- **No AI-speak** — no "synergize", "leverage", "circle back", "at the end of the day"

---

## Don't put these in a brief

- **Performance details** about specific people (good or bad)
- **Headcount specifics** before they're announced (planned cuts, planned hires by name)
- **Compensation** — anything related to comp, raises, equity
- **NDA / legal-sensitive** content — pending acquisitions, legal disputes, customer-specific contract terms
- **Direct quotes** from people who didn't approve being quoted

If something feels borderline, leave it out. The brief is a public team artifact — treat it like a Confluence page, not a DM.

---

## Tone

- Direct, terse, declarative
- Past tense for decisions, present tense for priorities, future tense for heads-up
- No hedging language ("might", "potentially", "could possibly") — if you're not sure, don't include it
- Speak as the VP, not about the VP

---

## Example brief that follows all the rules

```
📋 *VP Brief | Kim Ryneska | May 4, 2026*

**Decisions made**
• Paused UGC pilot until Q3 budget review (June 15)
• Approved brand refresh kickoff with Studio for June

**Current priorities**
• Q2 close-out — every team must hit pipeline targets
• Brand refresh discovery (Studio + Marketing leads)

**What's still open**
• Whether we sponsor INBOUND 2026 — decision by May 15

**Heads up**
• I'll be in London May 18-22 — async only those days
```

See `examples/` for more.
