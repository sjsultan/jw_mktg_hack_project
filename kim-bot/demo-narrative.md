# Kim Bot — Demo Narrative
### Marketing Mini-Hackathon | May 5, 2026 | ~5 minutes

---

## The Setup (60 sec)

**Speaker:** Start here.

> "Raise your hand if you've ever needed to know where a decision landed — and your only option was to wait for a weekly meeting, send a Slack that might get buried, or bother someone who's back-to-back all day."

*[Pause. Let the room react.]*

> "That's the problem we built for today. It's not a knowledge management problem. It's a context distribution problem. The VP knows what's been decided. The IC needs to know. And right now there's no good path between them that isn't a meeting or a game of telephone."

> "We built Kim Bot. Two Claude skills. One for the VP, one for the IC. Here's how it works."

---

## Act 1: Kim's side — the VP brief (90 sec)

**Speaker:** Walk through the VP flow.

> "It's end of day. Kim Ryneska, our Sr. Director of Brand Marketing, has been in back-to-back meetings. She runs one command: `/vp-brief`."

*[Show: `kim-brief-sample.md` — or the live Slack demo message if screensharing]*

> "Claude reads her Granola meeting notes and recent Slack messages from the week. It synthesizes everything into a structured brief — decisions made, current priorities, what's still open, and heads-up items for the team."

> "Kim reviews it. She removes one thing that's not ready to share. She types 'approve.' It posts to `#vp-context-feed`."

> "That's it. Two minutes. Her team now has her context."

**Key point to land:**
> "The approval gate is the whole product. Kim controls what goes out. Nothing posts without her sign-off. That's the guardrail."

---

## Act 2: Paraic's side — the IC query (90 sec)

**Speaker:** Switch to the IC perspective.

> "Now it's the next morning. Paraic McLean is a Social Media Marketing Manager. He's heard something about a UGC initiative but doesn't know if it's been decided or if he should start planning."

> "He doesn't send a Slack to Kim. He doesn't wait for the Thursday meeting. He types: `/ask-kim Has a decision been made on the UGC initiative?`"

*[Show: Example 1 from `ic-query-examples.md`]*

> "Claude searches `#vp-context-feed`, finds Kim's brief from yesterday, and answers: Yes, it's greenlit for Q3, you're leading it, Luis is supporting on paid amplification, but hold off on campaign calendar until the brand narrative is locked May 15."

> "Cited. Sourced. Thirty seconds."

---

## Act 3: The guardrail — knowing when NOT to answer (60 sec)

**Speaker:** Show the failure case.

> "Now Paraic asks something Kim didn't brief on: 'What's Kim's take on the agency we're evaluating for brand video?'"

*[Show: Example 4 from `ic-query-examples.md`]*

> "Kim's brief mentioned the agency decision is open, but she didn't share her view on the candidates. So Kim Bot doesn't guess. It says: I don't have enough context. Go to Kim directly — here's how."

> "That's the behavior we designed for. The skill knows when it's the right tool and when it should get out of the way."

---

## The Close — Why this matters (60 sec)

**Speaker:** Zoom out.

> "What we built is lightweight on purpose. Two markdown files. Two Claude skills. A Slack channel. No database. No UI. No integrations to maintain."

> "But the pattern it enables is real: structured VP context, approved before it ships, queryable by anyone on the team, grounded in what was actually decided — not what someone remembered from a meeting three weeks ago."

> "Scale this to 10 VPs. Every IC on the marketing team has a direct line to leadership context, on demand, with a citation. That's the version we're pointing at."

> "Kim Bot. Built in 45 minutes. Thank you."

---

## FAQ — If you get questions

**"What if the VP never runs it?"**
> That's a real adoption risk. You could automate the generation trigger (end-of-day cron), so the VP just gets a notification asking to approve — they don't have to initiate.

**"What stops someone from posting anything to #vp-context-feed?"**
> Channel permissions — only VPs or the bot have posting rights. The approval step is a human gate before the post happens.

**"What about information that changes mid-week?"**
> Briefs are dated and cited. ICs see when the context was approved. If something's changed, the skill flags it: "This was the state as of [date] — worth confirming if things have moved."

**"Could this work for other functions, not just marketing?"**
> Yes. The skill is generic. You'd give each VP or director their own instance, configured with their Slack ID and Granola access. Kim Bot is the prototype; the pattern is the product.
