#!/usr/bin/env python3
"""Validate bundle structure and instruction parity without network."""
import importlib.util
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from install import load_manifest, skill_name

def main():
    manifest = load_manifest()
    for name in manifest['localSkills']:
        path = ROOT / 'skills' / name / 'SKILL.md'
        assert skill_name(path) == name, name
        assert len(path.read_text().splitlines()) < 500, name
    for path in (ROOT / 'skills').rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent / link.split('#')[0]).is_file(), (path, link)
    agent = (ROOT / '.claude/agents/jade.md').read_text().split('---', 2)[1]
    listed = re.findall(r'^  - ([a-z0-9-]+)$', agent, re.M)
    assert listed == ['jade-workflow'], listed
    assert manifest['bundleVersion'] == (ROOT / 'VERSION').read_text().strip()
    subprocess.run([sys.executable, str(ROOT / 'scripts/sync-instructions.py'), '--check'], check=True)
    subprocess.run(['bash', '-n', str(ROOT / 'scripts/install-skills.sh')], check=True)
    print('PASS: manifesto, skills locais, referências, preload e instruções portáveis.')

if __name__ == '__main__':
    main()
