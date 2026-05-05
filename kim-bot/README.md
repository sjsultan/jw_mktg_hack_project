# Kim Bot — VP Context Brief System

> Built at the Justworks Marketing Mini-Hackathon, May 5 2026.

**The problem:** Marketing ICs can't get VP-level context without waiting for a weekly meeting, playing telephone, or bothering someone who's back-to-back.

**The solution:** A two-skill system. VPs generate and approve a weekly brief from their Granola notes and Slack. ICs query that brief in natural language and get a grounded answer with a citation.

---

## How it works

### For VPs — `/vp-brief`
Run `/vp-brief` at the end of your day or week. Claude pulls your Granola meeting notes and recent Slack activity, synthesizes them into a structured brief (decisions, priorities, open items), and asks you to approve before posting to `#vp-context-feed`.

You control what goes out. Nothing posts without your approval.

### For ICs — `/ask-kim`
Run `/ask-kim [your question]` anytime. Claude searches `#vp-context-feed` for relevant VP briefs and answers your question with a citation. If the answer isn't there, it tells you who to ask and how.

---

## Demo scenario

- **VP:** Kimberly Ryneska, Sr. Director Brand Marketing
- **IC:** Paraic McLean, Social Media Marketing Manager
- **Question:** "Has a decision been made on the UGC initiative? Should I start planning?"
- **Answer:** Grounded in Kim's approved brief, with citation and escalation nudge.

---

## Dummy data — VP roster

10 weeks of briefs (Mar 2 – May 5, 2026) for each VP, with interconnected narratives across the team.

| VP | Title | Brief prefix | Narrative arc |
|----|-------|-------------|---------------|
| Kimberly Ryneska | Sr. Director, Brand Marketing | `kim-brief-` | LinkedIn deprioritization → UGC greenlit → brand narrative → influencer pilot |
| Catherine Crevels | Chief Marketing Officer | `catherine-brief-` | FY27 strategy → board prep → LinkedIn approval → Q3 planning |
| Ted Babcock | VP, Growth Marketing | `ted-brief-` | H1 targets → Meta vs LinkedIn audit → Q2 recovery → influencer as new channel |
| Jamie Joyce | Sr. Director, Strategic Communication | `jamie-brief-` | Exec thought leadership → analyst briefings → LinkedIn comms → May 15 launch PR |
| Rachita Paes | VP, Product Marketing | `rachita-brief-` | May 15 GTM → ICP refresh → sales enablement → Gartner inclusion → launch readiness |

Briefs live in `data/briefs/`. Cross-VP references are intentional — the LinkedIn decision, brand narrative, and product launch all appear from multiple perspectives.

---

## Files

| File | Purpose |
|------|---------|
| `vp-brief.md` | Claude skill — VP runs this to generate and post their brief |
| `ic-query.md` | Claude skill — IC runs this to ask questions against VP briefs |
| `demo-narrative.md` | 5-minute demo script with FAQ |
| `data/briefs/` | 50 weeks of dummy briefs across 5 VPs |
| `data/ic-query-examples.md` | Sample IC questions and expected answers |

---

## Setup (to productionize)

1. Create `#vp-context-feed` Slack channel
2. Install both skills in Claude Code (`~/.claude/commands/`)
3. Onboard VPs — each runs `/vp-brief` at end of week
4. ICs use `/ask-kim` anytime

## Team
Built by Sol Sultan, Luis Loret de Mola, and the Kim Bot crew.
