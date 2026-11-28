---
name: social-thread
description: Write a thread of connected short text posts for X, Threads, Bluesky or another platform, with a substantial first post, posts that make sense alone and qualifiers kept beside the claims they limit. Use when someone asks for a thread, tweetstorm or series of connected posts. Not for a single post caption (social-captions) or a swipe carousel (carouselcraft).
license: Apache-2.0
---

# Social post threads

State who the thread is for and what the first post can deliver immediately. Break the material at real turns: observation, evidence, implication, decision. Each post may be shared alone, so keep a qualification beside the claim it limits. Use a thread-level source note only when the specific claims still make sense by themselves. Never divide a quote in a way that reverses its meaning, invent a hook statistic or force a reply bait ending.

Deliver paste-ready posts in order, with numbering only when useful or requested. Keep links and exact handles provided by the creator. Respect the user's length limit. For platform-weighted limits, rely on a suitable counter or identify that a count is only a plain-character estimate. A thread can end when the reader has the answer.

To check the finished thread, save it with a line containing only `---` between posts and run the bundled `scripts/check_post.py`, resolved beside this installed SKILL.md: `python3 "/path/to/social-thread/scripts/check_post.py" thread.txt --platform x --thread`. Use `threads` or `bluesky` for those platforms, and add `--sponsored` for a paid thread, which must disclose in the first post. It uses each platform's published counting rule, so report its numbers rather than a plain character estimate.

## Copyable brief

> Turn [source note] into [number] text posts. Lead with the result, keep the sample limits near it, and give each post a useful job. No sales CTA.

## Worked example

**Fictional input.** One of four binder clips slipped during a maker's desk test. It was the only clip used on glossy card; there was no second trial.

**1.** “One of four binder clips slipped in this desk test. It was also the only clip holding glossy card.”
**2.** “Two things changed at once: the clip and the surface. This run can’t tell us which explains the slip.”
**3.** “For the next round, try the same clip on both surfaces, then swap clips. Keep the stack thickness the same.”

## Source

X documents how connected posts work and how a single post from a thread can be shared on its own. [Read the source](https://help.x.com/en/using-x/create-a-thread).

The checker counts X posts by its [published weighting](https://docs.x.com/fundamentals/counting-characters), Threads posts by the [500-character limit](https://developers.facebook.com/docs/threads/overview) with emoji as bytes, and Bluesky posts by the [lexicon's 300 graphemes](https://github.com/bluesky-social/atproto/blob/main/packages/api/lexicons/app/bsky/feed/post.json), all read 28 November 2026.
