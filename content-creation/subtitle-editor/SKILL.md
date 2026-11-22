---
name: subtitle-editor
description: Edit spoken captions against a transcript or recording and deliver timed SRT or WebVTT files, translated subtitle tracks or clearly marked untimed cue text, with a bundled exporter that turns aligned cues into SRT or VTT. Use when someone asks for subtitles, closed captions, an SRT or VTT file, or to fix caption timing or line breaks. Not for the caption under a social post (social-captions) or describing visuals for blind viewers (audio-description).
license: Apache-2.0
---

# Subtitles and closed captions

Establish the language, target player and timing source. If media is accessible, listen to it, including meaningful sounds. If the only source is a transcript, work from its exact words, names and supplied timecodes. Never invent precise cue timings, speaker identities or inaudible words. With untimed text, deliver a segmented draft and ask for the recording or aligned cues to finish sync. Estimates explicitly requested for a rehearsal belong in a labelled timing plan.

For same-language captions, preserve meaning, negations, names and relevant hesitations. Identify speakers when the listener needs that information. Include sounds such as a second click when the demonstration turns on hearing it. For translated subtitles, preserve intent and required terms, and check reading time in the target language. Use a separate track per language unless bilingual display is requested.

Break on natural phrase boundaries. Preserve verified intervals when they suffice. Splitting a supplied interval more precisely requires word timing or an audio check. Keep each end after its start and cue starts in order. Inspect overlaps against what is actually audible; simultaneous speakers can be legitimate. Follow the target player's reading-speed and layout guidance when specified.

For a timed file, put notes outside its body. Basic SRT uses numbered blocks and comma milliseconds. WebVTT begins with WEBVTT and uses dot milliseconds. For simple, already aligned cues, the bundled `scripts/export_captions.py` accepts UTF-8 JSON objects in an array with integer `start_ms`, `end_ms` and plain `text`. Resolve the script relative to this installed SKILL.md and the input relative to the user’s project. From the project, run `python3 "/path/to/subtitle-editor/scripts/export_captions.py" "cues.json" --format vtt`, or choose `srt`. It writes the track to stdout. Verify sync, attribution and line breaks on playback when media is available.

## Try it

> Use my timecoded transcript to make an English VTT. Keep the second click audible in the captions and preserve the verified cue boundaries. If only text is available, return an untimed draft.

## Worked example

Invented alignment supplied by the creator: 0–1200 ms, “Listen.” Then 1500–2100 ms, a latch clicks. The silent gap has no cue.

```vtt
WEBVTT

00:00:00.000 --> 00:00:01.200
Listen.

00:00:01.500 --> 00:00:02.100
[latch clicks]
```

## Editorial sources

- Caption meaningful sound as well as speech and review automatic transcripts against the recording. [W3C WAI captions guide](https://www.w3.org/WAI/media/av/captions/)
- Use the file syntax and cue timing rules for WebVTT. [W3C WebVTT format](https://www.w3.org/TR/webvtt1/)
- YouTube illustrates basic plain UTF-8 SubRip files and the timestamp notation it accepts. [YouTube caption file examples](https://support.google.com/youtube/answer/2734698)
