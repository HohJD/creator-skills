---
name: image-descriptions
description: Write contextual alt text, carousel card descriptions and longer text equivalents for charts, diagrams, functional images and photos in posts, articles and newsletters. Use when someone asks for alt text, an image description, accessibility text for a carousel or a text version of a chart. Not for the promotional caption under a post (social-captions) or narration of video visuals (audio-description).
license: Apache-2.0
---

# Alt text and image descriptions

Inspect the actual asset and its placement when available. Ask what the reader needs from the image in this piece. If you only have a creator's description, derive a draft from that and flag any missing visual evidence. Do not guess identity, disability, relationships, ethnicity, mood or other unseen facts.

For an informative photo, give the relevant subject and action with the distinguishing detail. Include essential visible text that surrounding copy does not convey. For a linked image or control, communicate its purpose or destination when there is no other accessible name. On the web, a purely decorative or fully redundant image can take empty alt text as appropriate. Social platforms handle empty fields differently; specify the intended treatment for the destination.

For a chart, describe its subject, units, direction and important exception. Offer a nearby table or longer description for precise values if the data is available. For a carousel, describe each card in order and preserve the differences between them. Keep public post captions and image alternatives in separate fields. Use the requested length or platform constraints; avoid universal character caps.

For a set of descriptions, run the bundled `scripts/check_alt.py`, resolved beside this installed SKILL.md, on a file with one description per paragraph: `python3 "/path/to/image-descriptions/scripts/check_alt.py" alts.txt --platform instagram`. It flags empty or file-name descriptions, a leading "image of", two cards with the same text, Instagram's and X's 1,000-character limit, and long text that belongs in a fuller description. A clean result only means none of those mistakes; it cannot judge whether the description serves the reader.

## Try it

> Write alt text for [image] in an article about [topic]. The adjacent caption already says [caption]. For a chart, give a short alt and a fuller text equivalent using my values.

## Worked example

Supplied image: a poster shows a hand circling the “Thursday” on a calendar. Nearby caption already identifies the event as the studio opening.

**Alt:** A hand circles Thursday in red on the studio calendar.

If that same image is the sole content of a link to the booking form, its accessible name needs to convey that action, for example “Book a studio opening slot.” With an already-labelled link and a purely decorative image inside it, empty image alt can avoid repeating the link text.

## Editorial sources

- An image’s purpose and nearby text determine the alternative it needs. [W3C image decision tree](https://www.w3.org/WAI/tutorials/images/decision-tree/)
- For a chart, provide a short identification plus access to the important values and relationships. [W3C complex images](https://www.w3.org/WAI/tutorials/images/complex/)
- Skip "image of" and keep alt text to a short phrase or sentence, moving detail into a long description. [W3C images tips](https://www.w3.org/WAI/tutorials/images/tips/)
- Instagram accepts up to 1,000 characters of alt text through [Meta's IG User Media reference](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media); X's Help Center states the same limit (both read 28 November 2026).
