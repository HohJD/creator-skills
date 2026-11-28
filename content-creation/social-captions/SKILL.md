---
name: social-captions
description: Write or revise the caption that goes under a photo, Reel or carousel post, including openers, behind-the-scenes notes, launch announcements, sponsored posts and restrained calls to action. Use when someone asks for a caption, post copy, a few caption options or a CTA for a post. Not for timed subtitles or closed captions synced to video (subtitle-editor), alt text (image-descriptions) or multi-post threads (social-thread).
license: Apache-2.0
---

# Social captions

Read the post, image or rough notes. Identify what the audience can already see and what the creator can add: a decision, a detail outside the frame, instructions worth saving, or a reason the scene matters. Keep the speaker's best phrase. If the user says only “captions,” infer the intended deliverable from the input. Timestamps or dialogue suggest subtitles. A photo, post or request for a CTA suggests social copy. Ask if both are equally plausible.

Choose the shape that earns its space:
- **Behind the scenes:** name the moment a decision changed, then show its consequence.
- **Educational:** give the answer near the start, then one concrete way to try it.
- **Launch:** say what is available, for whom and how to get it. Use the supplied date, link and terms.
- **Story:** enter at a small observable moment. Use first person only for experiences the creator supplied.
- **Conversation:** ask a question whose answers would actually help the creator or reader.
- **Sponsored:** preserve the required disclosure, spelling and placement. Surface any unsupported offer or claim separately.

If the user asks for one caption only, return just the publishable words. Use only the supplied details. A strong one-line note can stand as the entire caption, especially if no photo is available.

Write the caption in paste-ready form. For variants, vary the angle or intent and say which one you would use if asked. Fit the requested language and length. Use hashtags or emoji when requested or when they carry meaning. Concrete observations carry more voice than a stock phrase about the creative journey. For more copyable briefs, see `references/caption-prompts.md`. Never manufacture a giveaway, scarcity, a personal reaction or a promise to send something. If the user asks for a strict character count, count the final string and state the counting convention when it matters.

Before handing over a caption for Instagram, Threads, Bluesky or X, run the bundled `scripts/check_post.py` on the final text: resolve it beside this installed SKILL.md, save the caption to a file in the user's project, and run `python3 "/path/to/social-captions/scripts/check_post.py" caption.txt --platform instagram`. It counts the way each platform publishes (Threads counts emoji as bytes, Bluesky counts graphemes, X weighs CJK, emoji and links) and checks Instagram's hashtag and @ tag caps. For a paid or gifted post add `--sponsored`: it fails without a disclosure and warns when the disclosure is below the first line or buried in hashtags. Report its findings; don't silently trim the creator's words to pass. A count within a few characters of a limit is still worth checking in the platform's composer.

## Try it

> Write two captions for my [post] for [audience]. My rough line is [line]. Give me a behind-the-scenes version and a useful tip. Keep [wording], and use [CTA or no CTA].

## Worked example

Fictional brief: a potter shows two photos of the same mug and says, “I kept the wonky handle. It's the one my thumb wants.” No sales link.

**Behind the scenes:** “I kept the wonky handle. See the little dent? That's where my thumb wants to go.”

**Practical angle:** “Before you smooth out a dent in a handle, pick up the mug. This one sits right under my thumb. I kept it.”

Both captions use the maker's observation. A claim that customers preferred this handle would need different evidence.

## Editorial sources

- Mailchimp describes how its writers adapt copy and use hashtags selectively. Use this as editorial practice, with the creator’s audience and voice taking precedence. [Mailchimp social style guide](https://styleguide.mailchimp.com/writing-for-social-media/)
- The checker's limits were read on 28 November 2026: Instagram's 2,200 characters, 30 hashtags and 20 @ tags from [Meta's IG User Media reference](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media), Threads' 500 from the [Threads API overview](https://developers.facebook.com/docs/threads/overview), Bluesky's 300 graphemes from the [post lexicon](https://github.com/bluesky-social/atproto/blob/main/packages/api/lexicons/app/bsky/feed/post.json) and X's weighted 280 from [Counting characters](https://docs.x.com/fundamentals/counting-characters). Instagram's in-app limit of 5 hashtags is stated in its Help Center, which renders client-side; the checker warns at 5 and fails at 30.
- A disclosure belongs with the endorsement, not behind "more" or among hashtags, in plain words such as "ad" or "sponsored". [FTC Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)
