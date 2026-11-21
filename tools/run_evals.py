#!/usr/bin/env python3
"""Small deterministic regression corpus. NOT a model-based eval."""
from pathlib import Path
import json
import sys
from validate_package import validate
ROOT=Path(__file__).resolve().parents[1]
def main():
    cases=sorted((ROOT/'fixtures').glob('*.json'))
    if not cases:raise RuntimeError('No fixtures')
    wrong=[]
    for file in cases:
        data=json.loads(file.read_text(encoding='utf-8'))
        expected=data.pop('_expected_valid')
        result=validate(data)
        ok=(not result)==expected
        print(('PASS' if ok else 'FAIL')+': '+file.name+' ('+('; '.join(result) if result else 'clean')+')')
        if not ok:wrong.append(file.name)
    if wrong:print('Mismatches:',wrong);return 1
    print(f'Passed {len(cases)} deterministic fixtures. This is not a LLM eval.');return 0
if __name__=='__main__':sys.exit(main())
