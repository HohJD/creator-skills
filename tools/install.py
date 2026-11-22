#!/usr/bin/env python3
"""Install canonical CreatorSkills skills into Claude Code or Codex; never run skill code."""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import sys
import tempfile
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
LOCATIONS={"claude": {"project":".claude/skills", "user":".claude/skills"},
           "codex": {"project":".agents/skills", "user":".agents/skills"}}

def install(agent:str,scope:str,target:Path|None=None,force:bool=False, *, skill: str | None = None)->list[Path]:
    if scope=="user":
        destination=Path.home()/LOCATIONS[agent]["user"]
    else:
        destination=(target or Path.cwd()).resolve()/LOCATIONS[agent]["project"]
    skills=sorted(p.parent for p in (ROOT/"content-creation").rglob("SKILL.md"))
    if skill is not None:
        selected = [item for item in skills if item.name == skill]
        if not selected:
            names = ", ".join(item.name for item in skills)
            raise ValueError(f"Unknown skill {skill!r}. Available skills: {names}")
        skills = selected
    collisions = [destination / p.name for p in skills
                  if (destination / p.name).exists() or (destination / p.name).is_symlink()]
    if collisions and not force:
        raise FileExistsError("Existing skills will not be overwritten: "+", ".join(map(str,collisions))+"; pass --force to back up and replace")
    destination.mkdir(parents=True,exist_ok=True)
    created=[]
    for item in skills:
        dst = destination / item.name
        # Finish the copy outside the host's discovery directory before changing a live skill.
        with tempfile.TemporaryDirectory(prefix=".creator-skills-stage-", dir=destination.parent) as tmp:
            staged = Path(tmp) / item.name
            shutil.copytree(item, staged, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            backup = None
            if dst.exists() or dst.is_symlink():
                if not force:
                    raise FileExistsError(f"Existing skill will not be overwritten: {dst}")
                archive = destination.parent / "creator-skills-backups"
                archive.mkdir(exist_ok=True)
                stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                batch = Path(tempfile.mkdtemp(prefix=f"{stamp}-", dir=archive))
                backup = batch / item.name
                dst.rename(backup)
            try:
                staged.rename(dst)
            except OSError:
                if backup is not None and not dst.exists() and not dst.is_symlink():
                    backup.rename(dst)
                raise
            if backup is not None:
                print(f"Backed up {dst} -> {backup}")
        created.append(dst)
    return created

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent',choices=LOCATIONS,required=True)
    parser.add_argument('--scope',choices=['project','user'],default='project')
    parser.add_argument('--target',type=Path,help='project root; ignored for --scope user')
    parser.add_argument('--skill', help='install one skill by name (default: all)')
    parser.add_argument('--force',action='store_true',help='back up existing folders before replacing them')
    args=parser.parse_args()
    try:
        for path in install(args.agent,args.scope,args.target,args.force,skill=args.skill): print('Installed:',path)
    except (ValueError,OSError) as exc:
        print('Install failed:',exc,file=sys.stderr)
        sys.exit(2)
