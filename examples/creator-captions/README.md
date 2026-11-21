# Captions for a repair clip

These examples use fictional creator notes and supplied sample timings. The photo shows a tote with a square patch where the strap joins the bag. Jo says the patch lets them identify the bag by touch. In the clip, Jo says “Left, not right.” A zipper sticks just after the line.

| Placement | Example | What the reader gets |
| --- | --- | --- |
| Under the post | “I can find this bag by touch now. The patch on the strap gives it away.” | The maker's observation outside the frame, using the supplied opening line. |
| Timed track | “Jo: Left, not right.” followed by “[zipper sticks]”. | Both the directional correction and the audible event. |
| Alternative for the still | “A square patch covers the point where the tote strap joins the bag.” | The visible detail that matters in this repair example. |

Download [the example SRT](example.srt) or [the example WebVTT](example.vtt). From the repository root you can reproduce either using the [sample cue data](cues.json):

```bash
python3 content-creation/subtitle-editor/scripts/export_captions.py examples/creator-captions/cues.json --format vtt
```

The exporter formats verified intervals. A transcript without audio alignment can be edited for wording, but needs timing evidence before it can become a synced track.
