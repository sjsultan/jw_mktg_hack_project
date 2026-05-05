# Kim Bot — Demo Walkthrough

> Use this as the script for the Friday demo. Read it top to bottom, hit the prompts in bold, screenshare the responses.

**Total runtime:** ~4 minutes
**Cast:** one person playing Kim (the VP), one playing Paraic (the IC)

---

## Setup (do this 5 minutes before the demo)

1. Open Claude Code in two windows side-by-side — left is "Kim's", right is "Paraic's"
2. Confirm `#mkt-vp-context-feed` is open in Slack on a third window
3. Have the two example briefs (`examples/kim-2026-04-27.md`, `examples/kim-2026-05-04.md`) already posted in the channel so `/ask-kim` has data to search
4. Mute notifications

---

## Act 1 — The problem (30 seconds)

> "Marketing ICs can't get VP context without waiting for a weekly meeting, playing telephone, or pinging someone who's back-to-back. Kim's calendar is packed. Paraic needs an answer in five minutes, not five days. So we built Kim Bot."

---

## Act 2 — Kim posts her brief (90 seconds)

**On Kim's screen, run:**

```
/vp-brief
```

**Narrate while Claude works:**

> "Claude is pulling Kim's Granola meeting notes from this week, scanning her recent Slack messages for decisions and priorities, and synthesizing it into a structured brief. She doesn't write anything — she just reviews."

**Claude shows the brief. Read it aloud, then say:**

> "Kim reviews. She can edit, redact, kill anything. Nothing posts without her approval."

**Type:**

```
approve
```

**Switch to the Slack window. Show the brief in `#mkt-vp-context-feed`.**

> "Posted. Searchable. Shareable. Done in under a minute."

---

## Act 3 — Paraic asks a question (90 seconds)

**Switch to Paraic's screen. Run:**

```
/ask-kim Has a decision been made on UGC? Should I start planning?
```

**Narrate while Claude works:**

> "Claude is searching the VP context feed for the relevant brief, finding Kim's note about UGC, and generating a grounded answer with a citation."

**Claude responds:**

> The UGC pilot is paused until the Q3 budget review on June 15. Hold off on planning new UGC work until that decision lands — Kim will share an update after the review.
>
> 📌 Source: Kim Ryneska's brief, May 4, 2026
>
> *Need more detail or want to discuss? Kim is the right person — flag it's a quick one if you need a fast turnaround.*

**Say:**

> "Paraic has his answer. He didn't message Kim. He didn't wait for a meeting. He didn't guess. And the answer is grounded — there's a citation to a real, approved source."

---

## Act 4 — The cross-VP digest (45 seconds)

**Run:**

```
/vp-digest
```

**Narrate while Claude works:**

> "Once we have multiple VPs posting briefs, we get something even better — a weekly digest that finds the through-lines, the conflicts, and the cross-team dependencies."

**Claude shows the digest. Read the headlines aloud:**

> "Aligned: Q2 close-out, brand refresh kickoff. Tensions: INBOUND sponsorship pending, UGC pilot conflicts with Lifecycle's Q3 plan. The team gets a navigation layer over every VP's context."

**Type:**

```
approve
```

---

## Act 5 — The pitch (30 seconds)

> "Three skills. One Slack channel. The output isn't AI-generated noise — every word came from a VP and was approved by them. It scales: more VPs post, more ICs query, the digest gets richer. We're not replacing the human — we're making the context they already create reachable."
>
> "Setup is one channel and three skill files. We could roll this out next week."

---

## Q&A prep — likely questions

**"What if a VP forgets to run it?"**
Add to existing weekly rituals — runs at the same time as their weekly review. Future: scheduled prompt that nudges them.

**"What about sensitive info?"**
The approval gate is the answer — VPs see every word before it posts. The skill also has explicit guardrails against PII, performance, headcount specifics.

**"How is this different from just reading Slack?"**
Slack is unstructured firehose. The brief is curated, dated, and queryable. `/ask-kim` searches the curated layer, not the noise.

**"What if briefs conflict?"**
The IC query skill flags conflicts explicitly — it doesn't pick a side. The digest skill surfaces them as "tensions."

**"Why not just use [existing tool]?"**
This isn't a tool — it's a pattern. Three skill files, one channel, zero infrastructure. Anyone on the team could extend it.
