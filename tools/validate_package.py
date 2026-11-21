#!/usr/bin/env python3
"""Conservative deterministic QA for structured scene packages.

This checks schema-ish invariants and claim references, NOT the truth of prose.
"""
from __future__ import annotations
from datetime import date
import json
from pathlib import Path
import re
import sys

# False positives are possible; these indicate required human review, not censorship.
RISKY=re.compile(r'\b(best|fastest|guaranteed|unlimited|free forever|100% accurate)\b', re.I)

def validate(data:dict)->list[str]:
    issues=[]
    for k in ('brief','claims','scenes'):
        if k not in data:issues.append(f'missing top-level {k}')
    if issues:return issues
    brief=data['brief'];cl=data['claims']; scenes=data['scenes']
    if not isinstance(brief,dict) or not isinstance(cl,dict) or not isinstance(scenes,list):return ['invalid top-level types']
    for k in ('topic','audience','observable_outcome','mode'):
        if not brief.get(k):issues.append(f'brief missing {k}')
    if brief.get('mode') not in ('short','long','sponsored'):issues.append('invalid mode')
    if not scenes:issues.append('no scenes')
    if brief.get('mode')=='sponsored':
        for k in ('mandatory_cta','mandatory_disclosure'):
            if not brief.get(k):issues.append(f'sponsored brief missing {k}')
    claims=cl.get('claims',[])
    if not isinstance(claims,list):return issues+['claims must be a list']
    ids=set();scene_ids=set()
    for c in claims:
        if not isinstance(c,dict):issues.append('claim is not an object');continue
        cid=c.get('id')
        if not cid or cid in ids:issues.append(f'duplicate/missing claim id: {cid}')
        ids.add(cid)
        if c.get('risk') not in ('critical','minor'):issues.append(f'{cid}: invalid risk')
        if c.get('status') not in ('documented','observed','unverified','inference'):issues.append(f'{cid}: invalid status')
        if c.get('risk')=='critical' and c.get('status') in ('unverified','inference'):issues.append(f'{cid}: unverified critical claim')
        if c.get('status')=='documented' and not c.get('source'):issues.append(f'{cid}: documented claim missing source')
        if c.get('status')=='observed':
            d=c.get('demo') or {}
            if d.get('state')!='observed' or not d.get('evidence'):issues.append(f'{cid}: observed claim missing observation evidence')
        checked=c.get('checked_at')
        if checked:
            try: date.fromisoformat(checked)
            except (ValueError,TypeError):issues.append(f'{cid}: invalid checked_at')
        if c.get('risk')=='critical' and c.get('status')=='documented' and not checked:
            issues.append(f'{cid}: critical documented claim missing checked_at')
    for s in scenes:
        if not isinstance(s,dict):issues.append('scene is not an object');continue
        sid=s.get('id')
        if not sid or sid in scene_ids:issues.append(f'duplicate/missing scene id: {sid}')
        scene_ids.add(sid)
        for k in ('narration','screen_action','claim_ids'):
            if k not in s or not s[k] and k!='claim_ids':issues.append(f'{sid}: missing {k}')
        for cid in s.get('claim_ids',[]):
            if cid not in ids:issues.append(f'{sid}: unknown claim ref {cid}')
        speech=s.get('narration','')
        if not isinstance(speech,str): issues.append(f'{sid}: narration must be text');continue
        if RISKY.search(speech):issues.append(f'{sid}: superlative/offer requires human claim check')
    for c in claims:
        if isinstance(c,dict):
            for sid in c.get('scenes',[]):
                if sid not in scene_ids:issues.append(f'{c.get("id")}: unknown scene ref {sid}')
    if brief.get('mode')=='sponsored' and brief.get('mandatory_cta'):
        full=' '.join(s.get('narration','') for s in scenes if isinstance(s,dict))
        if brief['mandatory_cta'] not in full:issues.append('mandatory CTA not present verbatim in narration')
    return issues

if __name__=='__main__':
    if len(sys.argv)!=2:sys.exit('Usage: validate_package.py path/to/package.json')
    try:data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError) as exc:sys.exit(str(exc))
    issues=validate(data)
    for issue in issues:print('FAIL:',issue)
    if issues:sys.exit(1)
    print('PASS: structural QA; not a fact-check.')
