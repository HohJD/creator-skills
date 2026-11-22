# From a reader question to a three-frame Story

This fictional example follows a small bookbinding studio. It has two photos of its shelf, green tabs on blank notebooks and yellow tabs on used ones. A short guide already exists at `https://example.org/notebooks?lang=en#tabs`. The example domain is a stand-in for the creator's approved destination.

## 1. Choose the question

> $audience-listening C1 and C2 are the same viewer asking “Which tabs mark blank books?” and “Is green for new ones?” C3 is a second viewer asking about the paper weight. Pick a question for this week. Count people and comments separately.

**Editorial decision:** Make the tab guide. One person asked about tabs twice; one person asked about paper weight once. The studio already has the photos and can answer the tab question today. There is no evidence here that it is more popular among individual viewers.

## 2. Make the Story

> $vertical-stories Make three text-only-over-photo Story frames from the confirmed tab colours. The reader is choosing a notebook for a new project. Use a question and a reveal that work without stickers. I have a wide shelf shot and a detail of the tabs.

| Frame | On-screen copy | Build |
| --- | --- | --- |
| 1 | “Which one would you take for a new project?” | Use the wide shot. Keep both tabs in frame. |
| 2 | “Pick green. It marks a blank notebook.” | Crop the detail photo to the green tab. Put the word “Green” beside it so colour is only one cue. |
| 3 | “Yellow means this one’s already in use.” | Return to the shelf. Label the two stacks “Blank” and “In use.” |

Nothing here depends on seeing results from a poll. Preview the text against the actual photos before posting.

## 3. Give each placement a trackable link

> $campaign-links Make two links to the notebook guide. Use source instagram and medium organic-social for the Story placement, source studio-digest and medium email for the newsletter. Keep campaign tab-guide, the language query and the tabs anchor.

| Placement | URL |
| --- | --- |
| Story link, if enabled | `https://example.org/notebooks?lang=en&utm_source=instagram&utm_medium=organic-social&utm_campaign=tab-guide#tabs` |
| Newsletter | `https://example.org/notebooks?lang=en&utm_source=studio-digest&utm_medium=email&utm_campaign=tab-guide#tabs` |

To reproduce the newsletter link from the repository root:

```bash
python3 content-creation/campaign-links/scripts/tag_url.py 'https://example.org/notebooks?lang=en#tabs' --source studio-digest --medium email --campaign tab-guide
```

The generated address can be checked offline. Verify redirects and reporting against the real site and account if those are part of the handoff.
