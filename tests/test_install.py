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
        self.assertEqual(result['skills'], 5)
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


class FigmaToCodeSkillTests(unittest.TestCase):
    """Garantias da skill jade-figma-to-code: descoberta, roteamento, MCP e ausência de regressão."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name) / 'projeto figma'
        self.project.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def test_skill_is_registered_as_local_core_skill(self):
        manifest = jade.load_manifest()
        self.assertIn('jade-figma-to-code', manifest['localSkills'])
        # Permanece uma skill local (sem rede); não vira fonte comunitária.
        community = {s['name'] for src in manifest['sources'] for s in src['skills']}
        self.assertNotIn('jade-figma-to-code', community)

    def test_skill_frontmatter_name_matches_directory(self):
        path = ROOT / 'skills' / 'jade-figma-to-code' / 'SKILL.md'
        self.assertTrue(path.is_file())
        self.assertEqual(jade.skill_name(path), 'jade-figma-to-code')

    def test_core_install_discovers_skill_without_network(self):
        result = jade.install(self.project, core_only=True)
        # 4 skills originais + a nova coordenadora = 5 skills próprias.
        self.assertEqual(result['skills'], 5)
        installed = self.project / '.claude/skills/jade-figma-to-code/SKILL.md'
        self.assertTrue(installed.is_file())

    def test_no_regression_original_four_skills_still_install(self):
        jade.install(self.project, core_only=True)
        for name in ('jade-workflow', 'jade-delivery', 'jade-frontend', 'frontend-quality-gate'):
            self.assertTrue((self.project / '.claude/skills' / name / 'SKILL.md').is_file(), name)

    def test_routing_triggers_on_figma_request(self):
        workflow = (ROOT / 'skills/jade-workflow/SKILL.md').read_text()
        self.assertIn('jade-figma-to-code', workflow)
        self.assertIn('Figma', workflow)
        frontend = (ROOT / 'skills/jade-frontend/SKILL.md').read_text()
        self.assertRegex(frontend, r'\|\s*Figma\s*\|.*jade-figma-to-code')
        engineering = (ROOT / 'skills/jade-frontend/references/engineering.md').read_text()
        self.assertIn('jade-figma-to-code', engineering)

    def test_skill_composes_instead_of_duplicating(self):
        body = (ROOT / 'skills/jade-figma-to-code/SKILL.md').read_text()
        # Compõe as skills oficiais por referência, não reescreve suas instruções.
        for ref in ('figma-design-to-code', 'ui-recon', 'spacing-system',
                    'code-review-and-quality', 'frontend-quality-gate'):
            self.assertIn(ref, body)
        self.assertLess(len(body.splitlines()), 500)

    def test_token_strategy_documented(self):
        body = (ROOT / 'skills/jade-figma-to-code/SKILL.md').read_text()
        for marker in ('Nível 1', 'Nível 2', 'Nível 3'):
            self.assertIn(marker, body)

    def test_mcp_unavailable_path_documented(self):
        body = (ROOT / 'skills/jade-figma-to-code/SKILL.md').read_text()
        self.assertIn('get_design_context', body)
        self.assertIn('BLOCKED', body)

    def test_figma_mcp_server_present_in_example(self):
        mcp = json.loads((ROOT / '.mcp.example.json').read_text())
        self.assertIn('figma', mcp['mcpServers'])
        self.assertEqual(mcp['mcpServers']['figma']['url'], 'https://mcp.figma.com/mcp')


if __name__ == '__main__':
    unittest.main()
