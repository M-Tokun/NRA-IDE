"""Exercise the PowerShell checker against isolated repositories in local_reports.

Fixtures are created inside the workspace and removed only after their resolved
paths have been checked. No demo source or index is changed by these tests.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / 'scripts/check_examples_links.ps1'
THEME = '33_boundary_and_history'
FIRST = '01_simultaneous_boundary_JP.html'
SECOND = '02_pre_rupture_history_JP.html'


class ExamplesLinkCheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shell = shutil.which('pwsh') or shutil.which('powershell')
        if cls.shell is None:
            raise unittest.SkipTest('PowerShell is required to execute the link checker')

    def setUp(self):
        self.scratch = (ROOT / 'local_reports').resolve()
        self.scratch.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='examples-links-', dir=self.scratch)
        self.fixture = Path(self.temp.name).resolve()
        self.assertTrue(self.fixture.is_relative_to(self.scratch))
        self.write('examples/README.md',
                   f'[guide](./{THEME}/README.md)\n[demo](./linked.html)\n'
                   '[remote](HTTPS://invalid.example/missing.html)\n'
                   '[mail](mailto:missing@example.invalid.md)\n')
        self.write('examples/README_JP.md', '')
        self.write('examples/index.html', '<a href="linked.html#part">demo</a>')
        self.write('examples/linked.html', '<p>linked</p>')
        self.write('examples/orphan.html', '<p>not listed in the root indexes</p>')
        self.write(f'examples/{THEME}/README.md',
                   f'[first]({FIRST})\n[second]({SECOND})\n'
                   '[history](history/original.md)\n'
                   '[reference](../../docs/reference.md)\n'
                   '[root document](../orphan.html)\n'
                   '[encoded](<説明%20%23資料.md#section> "title")\n')
        self.write(f'examples/{THEME}/{FIRST}',
                   "<a href='only_here.html'>local</a>"
                   "<a HREF='説明%20%23資料.md?a=1&amp;b=2#section'>encoded</a>"
                   "<a href='//invalid.example/missing.md'>external</a>")
        self.write(f'examples/{THEME}/{SECOND}', '<a href="README.md">guide</a>')
        self.write(f'examples/{THEME}/only_here.html', '<p>only in this folder</p>')
        self.write(f'examples/{THEME}/説明 #資料.md', '# reference')
        self.write(f'examples/{THEME}/history/original.md', '# preserved')
        self.write('docs/reference.md', '# reference outside examples, inside repo')
        self.write('examples/unrelated/ignored.html', '<a href="missing.html">outside scan</a>')

    def tearDown(self):
        # Verify the absolute target immediately before recursive fixture cleanup.
        target = Path(self.temp.name).resolve()
        self.assertTrue(target.is_relative_to(self.scratch))
        self.assertTrue(target.name.startswith('examples-links-'))
        self.temp.cleanup()

    def write(self, relative, content):
        target = (self.fixture / relative).resolve()
        self.assertTrue(target.is_relative_to(self.fixture))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8', newline='\n')
        return target

    def run_checker(self):
        return subprocess.run(
            [self.shell, '-NoLogo', '-NoProfile', '-NonInteractive', '-File',
             str(CHECKER), '-RepoRoot', str(self.fixture)],
            cwd=ROOT, capture_output=True, text=True, encoding='utf-8',
            errors='replace', timeout=30, check=False,
        )

    def test_relative_encoded_fragment_and_external_links(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('broken=0', result.stdout)
        self.assertIn('checked_documents=6', result.stdout)

    def test_nested_missing_target_is_not_satisfied_by_root_namesake(self):
        self.write('examples/root_only.html', '<p>wrong directory</p>')
        self.write(f'examples/{THEME}/{FIRST}', "<a href='root_only.html'>missing here</a>")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('broken=1', result.stdout)
        self.assertIn(FIRST, result.stdout)
        self.assertIn('root_only.html', result.stdout)

    def test_missing_markdown_target_is_reported(self):
        self.write(f'examples/{THEME}/{SECOND}', '<a href="history/missing.md">history</a>')
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('broken=1', result.stdout)
        self.assertIn('history/missing.md', result.stdout)

    def test_missing_required_theme_document_fails(self):
        target = (self.fixture / f'examples/{THEME}/{SECOND}').resolve()
        self.assertTrue(target.is_relative_to(self.fixture))
        target.unlink()
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(SECOND, result.stdout)
        self.assertIn('checked_documents=5', result.stdout)

    def test_directory_with_document_suffix_is_not_a_valid_target(self):
        directory = self.fixture / f'examples/{THEME}/directory.md'
        directory.mkdir()
        self.write(f'examples/{THEME}/{SECOND}', '<a href="directory.md">not a file</a>')
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('directory.md', result.stdout)

    def test_root_index_missing_html_is_still_reported(self):
        self.write('examples/index.html', '<a href="missing.html">missing</a>')
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('broken=1', result.stdout)
        self.assertIn('index.html -> missing.html', result.stdout)

    def test_orphan_detection_keeps_root_index_scope(self):
        # A theme-only reference to orphan.html must not count as a root-index entry.
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('orphan=1 checked_files=2', result.stdout)
        self.assertIn('orphan.html', result.stdout)
        self.assertNotIn('ignored.html', result.stdout)


if __name__ == '__main__':
    unittest.main()
