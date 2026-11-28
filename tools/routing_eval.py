#!/usr/bin/env python3
"""Score skill routing: does each request land on the skill evals/routing.json expects?

    python3 tools/routing_eval.py --check              # offline: the cases are complete and valid (CI)
    python3 tools/routing_eval.py --run codex          # ask a model, write evals/routing-results.json
    python3 tools/routing_eval.py --report             # print the saved results

A run gives the model every skill's name and description, as a host sees them when it decides
which skill to load, and asks it to pick one skill (or none) for each request. That measures
whether the descriptions route well; it is a proxy for, not a recording of, a host's own routing.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals/routing.json"
RESULTS = ROOT / "evals/routing-results.json"
KEY = re.compile(r"^([a-z][a-z-]*):\s*(.*)$")


def skills(root: Path = ROOT) -> dict[str, str]:
    out = {}
    for file in sorted((root / "content-creation").rglob("SKILL.md")):
        front = file.read_text(encoding="utf-8").split("---", 2)[1]
        meta = {m.group(1): m.group(2).strip() for line in front.splitlines() if (m := KEY.match(line))}
        out[meta["name"]] = meta["description"]
    return out


def check(cases: list[dict], names: dict[str, str]) -> list[str]:
    errors, prompts = [], set()
    for i, case in enumerate(cases, start=1):
        if case.get("expect") is not None and case["expect"] not in names:
            errors.append(f"case {i}: expects unknown skill {case['expect']!r}")
        if case.get("skill") not in names:
            errors.append(f"case {i}: belongs to unknown skill {case.get('skill')!r}")
        if case.get("case") == "hard" and (case.get("trap") not in names or case.get("trap") == case.get("expect")):
            errors.append(f"case {i}: a hard case needs a trap skill other than the expected one")
        if case.get("case") == "boundary" and case.get("expect") == case.get("skill"):
            errors.append(f"case {i}: a boundary case must route away from {case['skill']}")
        if case["prompt"] in prompts:
            errors.append(f"case {i}: duplicate prompt")
        prompts.add(case["prompt"])
    for name in names:
        kinds = {c["case"] for c in cases if c.get("skill") == name}
        for kind in ("positive", "boundary"):
            if kind not in kinds:
                errors.append(f"{name}: no {kind} case")
    return errors


def prompt(names: dict[str, str], requests: list[str]) -> str:
    listing = "\n".join(f"- {name}: {desc}" for name, desc in names.items())
    numbered = "\n".join(f"{i}. {text}" for i, text in enumerate(requests, start=1))
    return ("You are the skill router of a coding agent. Do not read files or run commands; answer from this text "
            f"only.\n\nInstalled skills:\n{listing}\n\nFor each numbered request below, name the one skill that should "
            "handle it, or \"none\" if no skill fits. Reply with only a JSON object mapping each number to a skill "
            f"name or \"none\", e.g. {{\"1\": \"social-captions\", \"2\": \"none\"}}.\n\nRequests:\n{numbered}\n")


def ask_codex(text: str, model: str | None) -> tuple[str, str]:
    if not shutil.which("codex"):
        raise RuntimeError("codex is not on PATH")
    version = subprocess.run(["codex", "--version"], capture_output=True, text=True).stdout.strip()
    with tempfile.TemporaryDirectory() as work:
        out = Path(work) / "answer.txt"
        cmd = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "--sandbox", "read-only",
               "--color", "never", "-o", str(out), *(["-m", model] if model else []), "-"]
        done = subprocess.run(cmd, input=text, capture_output=True, text=True, cwd=work, timeout=600)
        if done.returncode != 0 or not out.exists():
            raise RuntimeError(f"codex exited {done.returncode}: {done.stderr.strip()[-400:]}")
        return out.read_text(encoding="utf-8"), version


def codex_default_model() -> str:
    config = Path.home() / ".codex/config.toml"
    text = config.read_text(encoding="utf-8") if config.exists() else ""
    model = re.search(r'(?m)^model\s*=\s*"([^"]+)"', text)
    effort = re.search(r'(?m)^model_reasoning_effort\s*=\s*"([^"]+)"', text)
    return (model.group(1) if model else "codex default") + (f", reasoning {effort.group(1)}" if effort else "")


def parse_answer(text: str, count: int) -> list[str | None]:
    match = re.search(r"\{.*\}", text, re.S)
    data = json.loads(match.group(0)) if match else {}
    answers = []
    for i in range(1, count + 1):
        value = str(data.get(str(i), "")).strip().strip("`/$").lower()
        answers.append(None if value in ("", "none", "null") else value)
    return answers


def run(cases: list[dict], names: dict[str, str], host: str, model: str | None, batch: int, seed: int) -> dict:
    full = route(cases, names, model, batch, seed)
    blind = route(cases, {n: "(description hidden)" for n in names}, model, batch, seed)
    rows = [{**case, "got": full[i][0], "ok": full[i][0] == case.get("expect"),
             "names_only": blind[i][0], "names_only_ok": blind[i][0] == case.get("expect")}
            for i, case in enumerate(cases)]
    return {"date": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "host": host, "host_version": full[0][1],
            "model": model or codex_default_model(), "batch": batch, "seed": seed, "skills": len(names), "results": rows}


def route(cases: list[dict], names: dict[str, str], model: str | None, batch: int, seed: int):
    order = list(range(len(cases)))
    random.Random(seed).shuffle(order)
    answers: dict[int, str | None] = {}
    version = ""
    for start in range(0, len(order), batch):
        chunk = order[start:start + batch]
        reply, version = ask_codex(prompt(names, [cases[i]["prompt"] for i in chunk]), model)
        for i, answer in zip(chunk, parse_answer(reply, len(chunk))):
            answers[i] = answer
        print(f"  {min(start + batch, len(order))}/{len(order)} routed", file=sys.stderr)
    return [(answers[i], version) for i in range(len(cases))]


def summary(saved: dict) -> str:
    rows = saved["results"]
    def score(kind, key="ok"):
        part = [r for r in rows if kind in (None, r["case"])]
        return f"{sum(r[key] for r in part)}/{len(part)}"
    lines = [f"Routing eval, {saved['date']}: {saved['host']} ({saved['host_version']}, model: {saved['model']}), "
             f"{saved['skills']} skills, {len(rows)} requests in batches of {saved['batch']}.",
             "                          with descriptions   names only (control)"]
    for label, kind in (("should use the skill", "positive"), ("should go elsewhere", "boundary"),
                        ("hard (names mislead)", "hard"), ("total", None)):
        lines.append(f"  {label:<24}{score(kind):<20}{score(kind, 'names_only_ok')}")
    misses = [r for r in rows if not r["ok"]]
    if misses:
        lines.append("Misses:")
        lines += [f"  [{r['skill']}, {r['case']}] expected {r['expect'] or 'none'}, got {r['got'] or 'none'}: "
                  f"{r['prompt'][:70]}" for r in misses]
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog="\n\n".join(__doc__.split("\n\n")[1:]))
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--run", choices=["codex"])
    mode.add_argument("--report", action="store_true")
    p.add_argument("--model")
    p.add_argument("--batch", type=int, default=10)
    p.add_argument("--seed", type=int, default=7)
    args = p.parse_args()
    cases, names = json.loads(CASES.read_text(encoding="utf-8"))["cases"], skills()
    errors = check(cases, names)
    if args.check or errors:
        for e in errors:
            print("ERROR:", e)
        if not errors:
            print(f"PASS: {len(cases)} routing cases cover all {len(names)} skills (positive and boundary).")
        return 1 if errors else 0
    if args.report:
        print(summary(json.loads(RESULTS.read_text(encoding="utf-8"))))
        return 0
    saved = run(cases, names, args.run, args.model, args.batch, args.seed)
    RESULTS.write_text(json.dumps(saved, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(summary(saved))
    return 0


if __name__ == "__main__":
    sys.exit(main())
