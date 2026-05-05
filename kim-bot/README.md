# Kim Bot — VP Context Brief System

> Built at the Justworks Marketing Mini-Hackathon, May 5 2026.

**The problem:** Marketing ICs can't get VP-level context without waiting for a weekly meeting, playing telephone, or interrupting someone who's back-to-back.

**The solution:** A three-skill system. VPs generate and approve a weekly brief from their Granola notes and Slack. ICs query that brief in natural language and get a grounded answer with a citation. A weekly digest stitches every VP brief into one cross-team read.

---

## How it works

### For VPs — `/vp-brief`
Run `/vp-brief` at the end of your day or week. Claude pulls your Granola meeting notes and recent Slack activity, synthesizes them into a structured brief (decisions, priorities, open items), and asks you to approve before posting to `#mkt-vp-context-feed`.

You control what goes out. Nothing posts without your explicit approval.

### For ICs — `/ask-kim`
Run `/ask-kim [your question]` anytime. Claude searches `#mkt-vp-context-feed` for relevant VP briefs and answers your question with a citation. If the answer isn't there, it tells you who to ask and how.

### For everyone — `/vp-digest`
Run `/vp-digest` on Monday mornings (or whenever). Claude pulls every VP brief from the past week, identifies aligned priorities, conflicts, and cross-team dependencies, and posts a single digest the whole team can scan in 60 seconds.

---

## Demo scenario

- **VP:** Kimberly Ryneska, Sr. Director Brand Marketing
- **IC:** Paraic McLean, Social Media Marketing Manager
- **Question:** "Has a decision been made on the UGC initiative? Should I start planning?"
- **Answer:** Grounded in Kim's approved brief, with citation and escalation nudge.

See [`examples/`](./examples/) for sample briefs the demo runs against.

---

## Files

| File | Purpose |
|------|---------|
| `vp-brief.md` | Claude skill — VP runs this to generate and post their brief |
| `ic-query.md` | Claude skill — IC runs this to ask questions against VP briefs |
| `vp-digest.md` | Claude skill — anyone runs this to get a cross-VP weekly digest |
| `examples/` | Sample briefs (Kim Ryneska) showing what good output looks like |

---

## Setup (to productionize)

1. Slack channel `#mkt-vp-context-feed` (channel ID: `C0B2N1L446L`) — already created
2. Install all three skills in Claude Code (`~/.claude/commands/`)
3. Onboard VPs — each runs `/vp-brief` at end of week
4. ICs use `/ask-kim` anytime, anyone runs `/vp-digest` weekly

## Team
Built by Sol Sultan, Luis Loret de Mola, Rikki Piccirillo, and the Kim Bot crew.
