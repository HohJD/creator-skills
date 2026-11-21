#!/usr/bin/env python3
"""Install canonical CreatorSkills skills into Claude Code or Codex; never run skill code."""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import sys
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
LOCATIONS={"claude": {"project":".claude/skills", "user":".claude/skills"},
           "codex": {"project":".agents/skills", "user":".agents/skills"}}

def install(agent:str,scope:str,target:Path|None=None,force:bool=False)->list[Path]:
    if scope=="user":
        destination=Path.home()/LOCATIONS[agent]["user"]
    else:
        destination=(target or Path.cwd()).resolve()/LOCATIONS[agent]["project"]
    skills=sorted(p.parent for p in (ROOT/"content-creation").rglob("SKILL.md"))
    collisions=[destination/p.name for p in skills if (destination/p.name).exists()]
    if collisions and not force:
        raise FileExistsError("Existing skills will not be overwritten: "+", ".join(map(str,collisions))+"; pass --force to back up and replace")
    destination.mkdir(parents=True,exist_ok=True)
    created=[]
    for item in skills:
        dst=destination/item.name
        if dst.exists():
            stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
            backup=destination/(item.name+".backup-"+stamp)
            suffix=1
            while backup.exists():
                backup=destination/(item.name+".backup-"+stamp+f"-{suffix}")
                suffix+=1
            dst.rename(backup)
            print(f"Backed up {dst} -> {backup}")
        shutil.copytree(item,dst)
        created.append(dst)
    return created

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent',choices=LOCATIONS,required=True)
    parser.add_argument('--scope',choices=['project','user'],default='project')
    parser.add_argument('--target',type=Path,help='project root; ignored for --scope user')
    parser.add_argument('--force',action='store_true',help='back up existing folders before replacing them')
    args=parser.parse_args()
    try:
        for path in install(args.agent,args.scope,args.target,args.force): print('Installed:',path)
    except (FileExistsError,OSError) as exc:
        print('Install failed:',exc,file=sys.stderr)
        sys.exit(2)
