#!/usr/bin/env python3
"""Static checks only: agent skill metadata, discoverability and relative links."""
from __future__ import annotations
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parents[1]
KEY=re.compile(r'^([a-z][a-z-]*):\s*(.*)$')
NAME=re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
LINK=re.compile(r'(?<!https:)(?<!http:)(?:`)((?:references|assets)/[^`]+)(?:`)')

def lint(root:Path=ROOT)->list[str]:
    errors=[]
    skills=list(sorted((root/'content-creation').rglob('SKILL.md')))
    if not skills: return ['No skills found']
    for file in skills:
        text=file.read_text(encoding='utf-8')
        parts=text.split('---',2)
        if len(parts)<3 or parts[0].strip():
            errors.append(f'{file}: missing frontmatter');continue
        meta={m.group(1):m.group(2).strip() for line in parts[1].splitlines() if (m:=KEY.match(line))}
        if meta.get('name')!=file.parent.name or not NAME.fullmatch(meta.get('name','')):
            errors.append(f'{file}: name mismatch/invalid')
        desc=meta.get('description','')
        if len(desc)<80 or len(desc)>650: errors.append(f'{file}: description should describe routing in 80-650 chars')
        if 'Use when' not in desc: errors.append(f'{file}: description needs a "Use when" trigger clause')
        if ': ' in desc or ' #' in desc or desc[:1] in '\'"[{&*!|>%@`': errors.append(f'{file}: description is not a safe plain YAML scalar')
        siblings={p.parent.name for p in skills}
        for ref in re.findall(r'\(([a-z][a-z-]+)\)',desc):
            if '-' in ref and ref not in siblings: errors.append(f'{file}: description points to unknown skill {ref}')
        if len(text.splitlines())>500: errors.append(f'{file}: >500 lines; split references')
        for target in LINK.findall(parts[2]):
            if not (file.parent/target).is_file():errors.append(f'{file}: missing {target}')
        if 'Do not' not in parts[2] and 'Never' not in parts[2]:errors.append(f'{file}: no guardrail language')
    return errors

if __name__=='__main__':
    issues=lint()
    for e in issues:print('ERROR:',e)
    if issues:sys.exit(1)
    print(f'PASS: {len(list((ROOT/"content-creation").rglob("SKILL.md")))} skills metadata/resources inspected.')
