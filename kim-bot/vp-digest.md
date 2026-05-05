# /vp-digest — Cross-VP Weekly Digest

Pull all VP briefs posted to `#mkt-vp-context-feed` over the past week, synthesize them into a single cross-team digest, and post it back to the channel.

Use this on Monday mornings (or any time the team wants a one-stop read on what every VP is focused on).

---

**Instructions for Claude**:

You are running the cross-VP digest skill. Your job is to fetch every VP brief from the past 7 days, identify the through-lines and the friction points, and produce a single readable digest the whole marketing team can scan in 60 seconds.

---

## Step 1 — Fetch the past week of briefs

Call `slack_read_channel` on channel ID `C0B2N1L446L` (`#mkt-vp-context-feed`) for the last 7 days.

Filter for messages matching the brief header format:

```
📋 *VP Brief | [Name] | [Date]*
```

If there are zero briefs in the window, stop and report: "No VP briefs in the past 7 days — nothing to digest."

If there's only one brief, stop and report: "Only one brief this week ([VP Name]) — a digest needs at least two. Wait for more or just read [VP]'s brief directly."

---

## Step 2 — Identify cross-cutting themes

Across all briefs, find:

- **Aligned priorities** — multiple VPs focused on the same thing this week (e.g. Q2 close-out)
- **Conflicts or tensions** — one VP says X, another implies the opposite (flag explicitly)
- **Cross-team dependencies** — work one VP is doing that another team needs to know about
- **Open questions team-wide** — pending decisions that span multiple VPs

Don't repeat individual brief contents verbatim. The digest is *about* the briefs — readers can drill into source briefs for detail.

---

## Step 3 — Format the digest

```
📊 *Marketing Weekly Digest — Week of [Date]*

Briefs included: [VP Name 1], [VP Name 2], [VP Name 3]

**🎯 What everyone's aligned on**
• [Cross-cutting priority — one line, name the VPs in parens]

**⚠️ Tensions / open questions**
• [Where briefs disagree, hedge, or leave a decision unresolved]

**🔗 Cross-team dependencies**
• [Work in one VP's area that affects another team — call out who needs to know]

**📌 Drill in**
• [VP Name]'s brief → for [topic]
• [VP Name]'s brief → for [topic]
```

Rules:
- 8 bullets max across all sections
- Always cite which VP(s) each item came from in parens
- Be honest about conflicts — don't smooth them over
- If a section has nothing for the week, omit it entirely (don't write "none")

---

## Step 4 — Approval gate (REQUIRED)

Before posting, show the digest to whoever invoked the skill and ask:

> "Here's this week's digest pulling from [N] briefs. Anything to refine before I post it to #mkt-vp-context-feed?"

Wait for explicit approval. If they request edits, make them and re-confirm.

---

## Step 5 — Post to #mkt-vp-context-feed

Once approved, call `slack_send_message`:
- `channel_id`: `C0B2N1L446L`
- `text`: the formatted digest

After posting, confirm: "Digest posted — team can drill into source briefs from there."

---

## Example output

```
📊 *Marketing Weekly Digest — Week of May 4, 2026*

Briefs included: Kim Ryneska, Ted Sakai, Luis Loret de Mola

**🎯 What everyone's aligned on**
• Q2 close-out is the priority — pipeline targets are non-negotiable (Kim, Ted, Luis)
• Brand refresh kickoff in June — all teams should expect creative review cycles (Kim, Ted)

**⚠️ Tensions / open questions**
• INBOUND 2026 sponsorship — Kim says decision by May 15, Ted hasn't signaled budget allocation yet
• UGC pilot paused (Kim) but Luis's lifecycle plan still references UGC assets in Q3 — needs reconciliation

**🔗 Cross-team dependencies**
• Hightouch sync goes live Friday (Ted) — Lifecycle and Paid Social will see new audience segments next week
• Kim out May 18-22 — escalations during that window go to Ted

**📌 Drill in**
• Kim's brief → for UGC, brand refresh, INBOUND
• Ted's brief → for Hightouch, hiring, Q2 reforecast
• Luis's brief → for refer-a-friend, Q3 lifecycle plan
```

---

## Guardrails

- Never invent themes that aren't supported by the briefs
- If the briefs are short or sparse, the digest should be short — don't pad
- Treat the digest as a navigation tool, not a replacement for reading source briefs
