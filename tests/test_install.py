import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import install as jade

class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.project = self.base / 'project with spaces'
        self.project.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def test_core_install_preserves_project_instructions(self):
        (self.project / 'AGENTS.md').write_text('existing rules')
        result = jade.install(self.project, core_only=True)
        self.assertEqual(result['skills'], 4)
        self.assertEqual((self.project / 'AGENTS.md').read_text(), 'existing rules')
        self.assertFalse((self.project / '.mcp.json').exists())
        self.assertTrue((self.project / '.claude/skills/jade-delivery/SKILL.md').is_file())

    def test_reinstallation_preserves_skill_bytes(self):
        jade.install(self.project, core_only=True)
        before = jade.fingerprint(self.project / '.claude')
        jade.install(self.project, core_only=True)
        self.assertEqual(before, jade.fingerprint(self.project / '.claude'))

    def test_conflict_does_not_partially_install(self):
        agent = self.project / '.claude/agents/jade.md'
        agent.parent.mkdir(parents=True)
        agent.write_text('custom agent')
        with self.assertRaisesRegex(ValueError, 'existente diferente'):
            jade.install(self.project, core_only=True)
        self.assertEqual(agent.read_text(), 'custom agent')
        self.assertFalse((self.project / '.claude/skills').exists())

    def test_replace_keeps_backup(self):
        agent = self.project / '.claude/agents/jade.md'
        agent.parent.mkdir(parents=True)
        agent.write_text('custom agent')
        result = jade.install(self.project, core_only=True, replace=True)
        self.assertEqual((Path(result['backup']) / '.claude/agents/jade.md').read_text(), 'custom agent')

    def test_symlink_destination_rejected(self):
        outside = self.base / 'outside'; outside.mkdir()
        (self.project / '.claude').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'simbólico'):
            jade.install(self.project, core_only=True)
        self.assertEqual(list(outside.iterdir()), [])

    def test_mid_write_failure_restores_existing_agent(self):
        agent = self.project / '.claude/agents/jade.md'
        agent.parent.mkdir(parents=True); agent.write_text('custom agent')
        original = shutil.copy2
        failed = [False]
        def fail_once(src, dst, *args, **kwargs):
            if Path(dst) == self.project / 'jade.project.example.json' and not failed[0]:
                failed[0] = True
                raise OSError('simulated disk failure')
            return original(src, dst, *args, **kwargs)
        with patch.object(jade.shutil, 'copy2', side_effect=fail_once):
            with self.assertRaisesRegex(OSError, 'simulated'):
                jade.install(self.project, core_only=True, replace=True)
        self.assertEqual(agent.read_text(), 'custom agent')
        self.assertFalse((self.project / '.claude/skills/jade-workflow').exists())

    def test_external_failure_leaves_project_unchanged(self):
        with patch.object(jade, 'checkout', side_effect=ValueError('unavailable revision')):
            with self.assertRaisesRegex(ValueError, 'unavailable'):
                jade.install(self.project)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_portable_install_does_not_replace_agents(self):
        (self.project / 'AGENTS.md').write_text('keep')
        jade.install(self.project, agent='codex', core_only=True)
        self.assertTrue((self.project / 'JADE.md').exists())
        self.assertTrue((self.project / '.agents/skills/jade-workflow/SKILL.md').exists())
        self.assertEqual((self.project / 'AGENTS.md').read_text(), 'keep')

    def test_mutable_revision_rejected(self):
        root = self.base / 'bundle'; root.mkdir()
        manifest = jade.load_manifest()
        manifest['sources'][0]['revision'] = 'main'
        (root / 'skills-lock.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'imutável'):
            jade.load_manifest(root)

    def test_duplicate_name_rejected(self):
        root = self.base / 'bundle'; root.mkdir()
        manifest = jade.load_manifest()
        manifest['localSkills'].append(manifest['localSkills'][0])
        (root / 'skills-lock.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'duplicados'):
            jade.load_manifest(root)

    def test_invalid_agent_cli_rejected(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/install.py'), 'invalid-agent'],
                                capture_output=True)
        self.assertEqual(result.returncode, 2)

if __name__ == '__main__':
    unittest.main()
