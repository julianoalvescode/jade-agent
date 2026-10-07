#!/usr/bin/env python3
"""Project-scoped installer: standard library + Git, immutable source revisions."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    'claude-code': '.claude/skills', 'codex': '.agents/skills',
    'cursor': '.cursor/skills', 'github-copilot': '.github/skills',
    'windsurf': '.windsurf/skills', 'gemini-cli': '.gemini/skills',
    'cline': '.cline/skills', 'universal': '.agents/skills',
}
NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
SHA = re.compile(r'[0-9a-f]{40}\Z')

def safe_relative(value):
    p = PurePosixPath(value)
    if p.is_absolute() or '..' in p.parts or '\\' in value or not value:
        raise ValueError('Caminho relativo inválido: ' + value)
    return p

def skill_name(path):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n') or len(text.split('---', 2)) != 3:
        raise ValueError('Frontmatter inválido: ' + str(path))
    header = text.split('---', 2)[1]
    match = re.search(r'^name:\s*[\"\']?([a-z0-9-]+)[\"\']?\s*$', header, re.M)
    if not match or not re.search(r'^description:\s*\S', header, re.M):
        raise ValueError('Nome/descrição ausente: ' + str(path))
    return match[1]

def load_manifest(root=ROOT):
    manifest = json.loads((root / 'skills-lock.json').read_text())
    if manifest.get('schemaVersion') != 2 or not manifest.get('localSkills'):
        raise ValueError('Manifesto incompatível.')
    names = list(manifest['localSkills'])
    for source in manifest['sources']:
        if not re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', source['repository']):
            raise ValueError('Fonte GitHub HTTPS inválida.')
        if not SHA.fullmatch(source['revision']):
            raise ValueError('Toda fonte precisa de SHA imutável de 40 caracteres.')
        for item in source['skills']:
            safe_relative(item['path'])
            names.append(item['name'])
    if any(not NAME.fullmatch(n) for n in names) or len(names) != len(set(names)):
        raise ValueError('Nomes inválidos ou duplicados no manifesto.')
    return manifest

def run_git(*args):
    env = os.environ.copy()
    env['GIT_TERMINAL_PROMPT'] = '0'
    env['GIT_LFS_SKIP_SMUDGE'] = '1'
    return subprocess.run(['git', *map(str, args)], check=True, capture_output=True,
                          text=True, env=env, timeout=240).stdout.strip()

def checkout(source, target):
    run_git('init', '--quiet', target)
    run_git('-C', target, 'remote', 'add', 'origin', source['repository'])
    run_git('-C', target, 'fetch', '--quiet', '--depth', '1', 'origin', source['revision'])
    run_git('-C', target, 'checkout', '--quiet', '--detach', 'FETCH_HEAD')
    if run_git('-C', target, 'rev-parse', 'HEAD') != source['revision']:
        raise ValueError('Revisão obtida não corresponde ao manifesto.')

def fingerprint(path):
    if path.is_symlink():
        raise ValueError('Link simbólico não permitido: ' + str(path))
    digest = hashlib.sha256()
    entries = [path] if path.is_file() else sorted(path.rglob('*'))
    for item in entries:
        if item.is_symlink():
            raise ValueError('Link simbólico não permitido: ' + str(item))
        if item.is_file():
            relative = 'file' if path.is_file() else item.relative_to(path).as_posix()
            digest.update(relative.encode() + b'\0' + item.read_bytes() + b'\0')
            digest.update(str(item.stat().st_mode & 0o111).encode())
    return digest.hexdigest()

def copy_skill(source, target, expected):
    if source.is_symlink() or skill_name(source / 'SKILL.md') != expected:
        raise ValueError('Identidade inesperada para skill: ' + expected)
    fingerprint(source)
    shutil.copytree(source, target)
    return fingerprint(target)

def guarded_destination(project, relative):
    safe_relative(relative)
    target = project / relative
    for part in [target, *target.parents]:
        if part == project:
            break
        if part.is_symlink():
            raise ValueError('Destino contém link simbólico: ' + str(part))
    if not target.resolve().is_relative_to(project):
        raise ValueError('Destino fora do projeto.')
    return target

def install(project, agent='claude-code', core_only=False, replace=False, source_cache=None,
            root=ROOT):
    manifest = load_manifest(root)
    if agent not in TARGETS:
        raise ValueError('Agente não suportado: ' + agent)
    project = Path(project).resolve()
    if not project.is_dir():
        raise ValueError('O diretório do projeto precisa existir.')
    if not core_only and shutil.which('git') is None:
        raise ValueError('Git é necessário para instalar as skills comunitárias.')
    entries = []
    with tempfile.TemporaryDirectory(prefix='jade-stage-') as temp:
        stage = Path(temp)
        for name in manifest['localSkills']:
            staged = stage / 'skills' / name
            staged.parent.mkdir(exist_ok=True)
            copy_skill(root / 'skills' / name, staged, name)
            entries.append((staged, TARGETS[agent] + '/' + name))
        if not core_only:
            for index, source in enumerate(manifest['sources']):
                source_root = stage / ('source-' + str(index))
                cached = Path(source_cache) / source['revision'] if source_cache else None
                if cached and cached.is_dir():
                    if run_git('-C', cached, 'rev-parse', 'HEAD') != source['revision']:
                        raise ValueError('Cache com revisão incorreta.')
                    if run_git('-C', cached, 'status', '--porcelain', '--untracked-files=all'):
                        raise ValueError('Cache contém alterações locais.')
                    import tarfile, io
                    archive = subprocess.run(['git', '-C', str(cached), 'archive', source['revision'],
                                              '--', *[s['path'] for s in source['skills']]],
                                             check=True, capture_output=True, timeout=120).stdout
                    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
                        for member in tar.getmembers():
                            safe_relative(member.name)
                            if not (member.isfile() or member.isdir()):
                                raise ValueError('Cache contém entrada não regular.')
                        tar.extractall(source_root)
                else:
                    checkout(source, source_root)
                for item in source['skills']:
                    source_path = source_root / item['path']
                    if not source_path.resolve().is_relative_to(source_root.resolve()):
                        raise ValueError('Skill fora da fonte.')
                    staged = stage / 'skills' / item['name']
                    copy_skill(source_path, staged, item['name'])
                    entries.append((staged, TARGETS[agent] + '/' + item['name']))
        if agent == 'claude-code':
            entries.append((root / '.claude/agents/jade.md', '.claude/agents/jade.md'))
        else:
            entries.append((root / 'AGENT-PROMPT.md', 'JADE.md'))
        entries.append((root / 'jade.project.example.json', 'jade.project.example.json'))
        entries.append((root / '.mcp.example.json', '.mcp.jade.example.json'))
        changes = []
        for source, relative in entries:
            target = guarded_destination(project, relative)
            same = target.exists() and fingerprint(target) == fingerprint(source)
            if target.exists() and not same and not replace:
                raise ValueError('Arquivo existente diferente: ' + relative +
                                 '. Revise e use --replace para atualizar com backup.')
            if not same:
                changes.append((source, target, relative))
        receipt = {'bundleVersion': manifest['bundleVersion'], 'agent': agent,
                   'mode': 'core-only' if core_only else 'full',
                   'files': {rel: fingerprint(src) for src, rel in entries},
                   'sources': [] if core_only else manifest['sources']}
        receipt_rel = '.jade/installation-' + agent + '.json'
        receipt_path = guarded_destination(project, receipt_rel)
        receipt_temp = stage / 'receipt.json'
        receipt_temp.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
        if not receipt_path.exists() or fingerprint(receipt_path) != fingerprint(receipt_temp):
            changes.append((receipt_temp, receipt_path, receipt_rel))
        backup_root = None
        committed = []
        try:
            for source, target, relative in changes:
                backup = None
                if target.exists():
                    if backup_root is None:
                        guarded_destination(project, '.jade/backups')
                        (project / '.jade/backups').mkdir(parents=True, exist_ok=True)
                        backup_root = Path(tempfile.mkdtemp(prefix='install-', dir=project / '.jade/backups'))
                    backup = backup_root / relative
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(target, backup) if target.is_dir() else shutil.copy2(target, backup)
                committed.append((target, backup))
                if target.exists():
                    shutil.rmtree(target) if target.is_dir() else target.unlink()
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(source, target) if source.is_dir() else shutil.copy2(source, target)
        except BaseException:
            for target, backup in reversed(committed):
                if target.exists():
                    shutil.rmtree(target) if target.is_dir() else target.unlink()
                if backup:
                    shutil.copytree(backup, target) if backup.is_dir() else shutil.copy2(backup, target)
            raise
        count = len(manifest['localSkills']) + (0 if core_only else sum(len(s['skills']) for s in manifest['sources']))
        return {'skills': count, 'mode': receipt['mode'], 'project': str(project),
                'backup': str(backup_root) if backup_root else None}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('agent', nargs='?', default='claude-code', choices=TARGETS)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--core-only', action='store_true', help='Instalar só as quatro skills próprias, sem rede.')
    parser.add_argument('--replace', action='store_true', help='Atualizar arquivos diferentes, mantendo backup.')
    parser.add_argument('--source-cache', type=Path, help='Checkouts limpos nomeados pelo SHA para instalação offline.')
    args = parser.parse_args()
    try:
        result = install(args.project, args.agent, args.core_only, args.replace, args.source_cache)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print('Instalação concluída. Autentique os conectores no cliente antes de usá-los.')
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print('Instalação não concluída: ' + str(error), file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
