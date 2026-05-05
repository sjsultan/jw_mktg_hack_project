# Kim Bot — VP Context Brief System

> Built at the Justworks Marketing Mini-Hackathon, May 5 2026.

**The problem:** Marketing ICs can't get VP-level context without waiting for a weekly meeting, playing telephone, or bothering someone who's back-to-back.

**The solution:** A two-skill system. VPs generate and approve a weekly brief from their Granola notes and Slack. ICs query that brief in natural language and get a grounded answer with a citation.

---

## How it works

### For VPs — `/vp-brief`
Run `/vp-brief` at the end of your day or week. Claude pulls your Granola meeting notes and recent Slack activity, synthesizes them into a structured brief (decisions, priorities, open items), and asks you to approve before posting to `#mkt-vp-context-feed`.

You control what goes out. Nothing posts without your approval.

### For ICs — `/ask-kim`
Run `/ask-kim [your question]` anytime. Claude searches `#mkt-vp-context-feed` for relevant VP briefs and answers your question with a citation. If the answer isn't there, it tells you who to ask and how.

---

## Demo scenario

- **VP:** Kimberly Ryneska, Sr. Director Brand Marketing
- **IC:** Paraic McLean, Social Media Marketing Manager
- **Question:** "Has a decision been made on the UGC initiative? Should I start planning?"
- **Answer:** Grounded in Kim's approved brief, with citation and escalation nudge.

---

## Files

| File | Purpose |
|------|---------|
| `vp-brief.md` | Claude skill — VP runs this to generate and post their brief |
| `ic-query.md` | Claude skill — IC runs this to ask questions against VP briefs |

---

## Setup (to productionize)

1. Slack channel `#mkt-vp-context-feed` (channel ID: `C0B2N1L446L`) — already created
2. Install both skills in Claude Code (`~/.claude/commands/`)
3. Onboard VPs — each runs `/vp-brief` at end of week
4. ICs use `/ask-kim` anytime

## Team
Built by Sol Sultan, Luis Loret de Mola, and the Kim Bot crew.
