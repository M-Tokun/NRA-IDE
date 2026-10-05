from __future__ import annotations
import contextlib, io, json, os, pathlib, shutil, subprocess, sys, tempfile, unittest
from unittest import mock
ROOT = pathlib.Path(__file__).resolve().parents[1]
GUARD = ROOT / 'skills' / 'agents-md-guard'
sys.path.insert(0, str(GUARD))
import _common, cline_adapter, cline_guard, cline_mark, cline_session_start

class ClineGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.contract = self.root / 'AGENTS.md'
        self.text = '# Contract\n全文を読む。\n'
        self.contract.write_text(self.text, encoding='utf-8')
        for name, value in (('AGENTS_MD_PATH', str(self.contract)), ('MARKER_ROOT', str(self.root / 'markers'))):
            patcher = mock.patch.object(_common, name, value); patcher.start(); self.addCleanup(patcher.stop)
    def invoke(self, fn, payload):
        raw = payload if isinstance(payload, str) else json.dumps(payload)
        out = io.StringIO()
        with mock.patch.object(sys, 'stdin', io.StringIO(raw)), contextlib.redirect_stdout(out): code = fn()
        return code, json.loads(out.getvalue()) if out.getvalue() else None
    def pre(self, name, args=None):
        return {'taskId':'test-1','preToolUse':{'toolName':name,'parameters':args or {}}}
    def post(self, args=None, result=None, success=True, name='readFile'):
        return {'taskId':'test-1','postToolUse':{'toolName':name,'parameters':args or {'path':'AGENTS.md'},'result':self.text if result is None else result,'success':success}}
    def test_nested_read_passes_but_mutations_require_current_contract(self):
        for name in cline_adapter.FILE_READ_TOOLS:
            _, out = self.invoke(cline_guard.main, self.pre(name, {'path':'AGENTS.md'})); self.assertFalse(out['cancel'])
        for name in cline_adapter.READ_TOOLS - cline_adapter.FILE_READ_TOOLS:
            _, out = self.invoke(cline_guard.main, self.pre(name)); self.assertTrue(out['cancel'])
        for name in ('bash','execute_command','run_commands','editor','apply_patch','mcp__server__write','future_tool','Read','Glob','WebFetch','read_many_files'):
            _, out = self.invoke(cline_guard.main, self.pre(name)); self.assertTrue(out['cancel'])
        _common.write_marker('cline','test-1')
        _, out = self.invoke(cline_guard.main,self.pre('bash',{'command':'git push origin HEAD'}))
        self.assertEqual(out,{'cancel':False})
    def test_unread_single_contract_only_and_marked_reads_resume(self):
        for args in ({'path':'AGENTS.md'}, {'paths':['AGENTS.md']}, {'paths':json.dumps(['AGENTS.md'])}, {'absolute_path':str(self.contract)}):
            _, out=self.invoke(cline_guard.main,self.pre('read_files',args));self.assertFalse(out['cancel'])
        for args in ({}, {'paths':['other.md']}, {'paths':['AGENTS.md','other.md']},
                     {'paths':['AGENTS.md','AGENTS.md']}, {'path':'AGENTS.md','offset':'0'},
                     {'paths':['AGENTS.md'],'path':'other.md'}, {'path':'AGENTS.md','limit':1},
                     {'path':'other/AGENTS.md'}, {'paths':['*.md']}, {'path':'AGENTS.md','startLine':'1'}):
            _, out=self.invoke(cline_guard.main,self.pre('read_files',args));self.assertTrue(out['cancel'])
        _common.write_marker('cline','test-1')
        for name in cline_adapter.READ_TOOLS:
            _, out=self.invoke(cline_guard.main,self.pre(name,{'path':'other.md'}));self.assertFalse(out['cancel'])
        self.contract.rename(self.root/'AGENTS.missing')
        _, out=self.invoke(cline_guard.main,self.pre('read_files',{'paths':['AGENTS.md']}));self.assertTrue(out['cancel'])

    def test_nested_full_response_marks_then_contract_change_invalidates(self):
        self.invoke(cline_mark.main,self.post())
        self.assertTrue(_common.is_marked('cline','test-1'))
        self.contract.write_text('# Changed',encoding='utf-8')
        _, out = self.invoke(cline_guard.main,self.pre('bash'));self.assertTrue(out['cancel'])
    def test_partial_failed_foreign_and_nonread_results_do_not_mark(self):
        cases=[self.post(success=False),self.post(result='# Contract'),
               self.post(args={'path':str(self.root/'other'/'AGENTS.md')}),self.post(name='bash'),
               self.post(args={'path':'AGENTS.md','offset':'0'}),
               self.post(args={'path':'AGENTS.md','startLine':'1'}),
               self.post(args={'path':'AGENTS.md','line_range':'1:1'}),
               self.post(args={'path':'AGENTS.md','file_path':'other.md'})]
        for payload in cases:
            self.invoke(cline_mark.main,payload);self.assertFalse(_common.is_marked('cline','test-1'))
    def test_read_files_single_path_supported_multiple_paths_not_marked(self):
        for paths in (['AGENTS.md'],json.dumps(['AGENTS.md'])):
            self.invoke(cline_mark.main,self.post(args={'paths':paths},name='read_files'))
            self.assertTrue(_common.is_marked('cline','test-1'));_common.invalidate_marker('cline','test-1')
        for paths in (['AGENTS.md','other.md'],'not-json',[],[{}]):
            self.invoke(cline_mark.main,self.post(args={'paths':paths},name='read_files'))
            self.assertFalse(_common.is_marked('cline','test-1'))
    def test_malformed_nested_and_conflicting_payloads_denied(self):
        cases=['{',[],{}, {'taskId':'../escape'}, {'taskId':'test-1','preToolUse':[]},
               {'taskId':'test-1','preToolUse':{'toolName':'bash','parameters':[]}},
               {**self.pre('bash'),'tool_name':'Read'},
               {**self.pre('bash'),'postToolUse':self.post()['postToolUse']}]
        for payload in cases:
            _, out = self.invoke(cline_guard.main,payload);self.assertTrue(out['cancel'])
    def test_omitted_empty_parameters_preserves_contract_and_host_permissions(self):
        payload={'taskId':'test-1','preToolUse':{'toolName':'filesystem-validation__list_allowed_directories'}}
        _,out=self.invoke(cline_guard.main,payload);self.assertTrue(out['cancel'])
        _common.write_marker('cline','test-1')
        _,out=self.invoke(cline_guard.main,payload);self.assertEqual(out,{'cancel':False})
        for value in (None,[],False,'{}'):
            bad={'taskId':'test-1','preToolUse':{'toolName':'filesystem-validation__list_allowed_directories','parameters':value}}
            _,out=self.invoke(cline_guard.main,bad);self.assertTrue(out['cancel'])
        _common.invalidate_marker('cline','test-1')
        _,out=self.invoke(cline_guard.main,{'taskId':'test-1','preToolUse':{'toolName':'read_files'}})
        self.assertTrue(out['cancel'])
        self.invoke(cline_mark.main,{'taskId':'test-1','postToolUse':{'toolName':'read_files','result':self.text,'success':True}})
        self.assertFalse(_common.is_marked('cline','test-1'))

    def test_start_and_resume_emit_entire_contract_then_mark(self):
        for event in ('TaskStart','TaskResume','agent_start','agent_resume'):
            _, out = self.invoke(cline_session_start.main,{'taskId':'test-1','hookName':event})
            self.assertFalse(out['cancel']);self.assertEqual(out['contextModification'],'AGENTS.md loaded\n\n'+self.text)
            self.assertTrue(_common.is_marked('cline','test-1'))
    def test_start_failure_invalidates_previous_marker(self):
        _common.write_marker('cline','test-1')
        with mock.patch.object(_common,'read_agents_md',side_effect=OSError()):
            _, out = self.invoke(cline_session_start.main,{'taskId':'test-1','hookName':'TaskStart'})
        self.assertTrue(out['cancel']);self.assertFalse(_common.is_marked('cline','test-1'))
        _, out = self.invoke(cline_session_start.main,{'taskId':'test-1','hookName':'PostToolUse'})
        self.assertTrue(out['cancel'])
    def test_utf16_context_limit_no_partial_marker(self):
        self.contract.write_text('😀'*25000,encoding='utf-8')
        _, out = self.invoke(cline_session_start.main,{'taskId':'test-1'})
        self.assertTrue(out['cancel']);self.assertFalse(_common.is_marked('cline','test-1'))
    def test_output_or_marker_failure_never_establishes_read(self):
        with mock.patch.object(_common,'write_marker',side_effect=OSError()):
            code,_=self.invoke(cline_session_start.main,{'taskId':'test-1'})
        self.assertEqual(code,2);self.assertFalse(_common.is_marked('cline','test-1'))
        output = io.StringIO()
        with mock.patch.object(sys,'stdin',io.StringIO('{"taskId":"test-1"}')),mock.patch.object(cline_adapter,'print',side_effect=OSError(),create=True),contextlib.redirect_stdout(output):
            self.assertEqual(cline_session_start.main(),0)
        self.assertTrue(json.loads(output.getvalue())['cancel'])
        self.assertFalse(_common.is_marked('cline','test-1'))
    def prepare_windows(self):
        shutil.copytree(GUARD,self.root/'skills'/'agents-md-guard',ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT/'.clinerules'/'hooks',self.root/'.clinerules'/'hooks')
        nested=self.root/'nested';nested.mkdir()
        return nested
    def ps(self,exe,event,payload,cwd,env=None):
        p=subprocess.run([exe,'-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',str(self.root/'.clinerules'/'hooks'/(event+'.ps1'))],input=json.dumps(payload),text=True,encoding='utf-8',capture_output=True,cwd=cwd,env=env,timeout=20)
        self.assertEqual(p.returncode,0,p.stderr)
        return json.loads(p.stdout.lstrip('\ufeff'))
    def test_windows_entrypoints_from_nested_directory(self):
        nested=self.prepare_windows()
        shells=[path for name in ('pwsh','powershell.exe') if (path:=shutil.which(name))]
        self.assertTrue(shells,'Windows integration requires PowerShell')
        for exe in shells:
            with self.subTest(shell=exe):
                marker=self.root/'.agent_state'/'agents_md_read'/'cline'/'test-1'
                if marker.exists():marker.write_text('{}',encoding='utf-8')
                self.assertTrue(self.ps(exe,'PreToolUse',self.pre('bash'),nested)['cancel'])
                self.assertFalse(self.ps(exe,'PreToolUse',self.pre('read_files',{'paths':['AGENTS.md']}),nested)['cancel'])
                self.assertFalse(self.ps(exe,'PostToolUse',self.post(),nested)['cancel'])
                self.assertFalse(self.ps(exe,'PreToolUse',self.pre('bash'),nested)['cancel'])
                out=self.ps(exe,'TaskStart',{'taskId':'test-1','hookName':'TaskStart'},nested)
                self.assertEqual(out['contextModification'],'AGENTS.md loaded\n\n'+self.text)
                self.assertFalse(self.ps(exe,'TaskResume',{'taskId':'test-1','hookName':'TaskResume'},nested)['cancel'])
                self.assertTrue(self.ps(exe,'PreToolUse',[],nested)['cancel'])
                no_args={'taskId':'test-1','preToolUse':{'toolName':'filesystem-validation__list_allowed_directories'}}
                self.assertFalse(self.ps(exe,'PreToolUse',no_args,nested)['cancel'])
                marker.write_text('{}',encoding='utf-8')
                self.assertTrue(self.ps(exe,'PreToolUse',no_args,nested)['cancel'])
    def test_windows_python_missing_and_bad_json_fail_closed(self):
        nested=self.prepare_windows();exe=shutil.which('pwsh') or shutil.which('powershell.exe');self.assertIsNotNone(exe)
        env=dict(os.environ);env['PATH']=str(self.root/'no-python')
        self.assertTrue(self.ps(exe,'PreToolUse',self.pre('bash'),nested,env)['cancel'])
        (self.root/'skills'/'agents-md-guard'/'cline_guard.py').write_text('print("{}")',encoding='utf-8')
        self.assertTrue(self.ps(exe,'PreToolUse',self.pre('bash'),nested)['cancel'])
        (self.root/'skills'/'agents-md-guard'/'cline_session_start.py').write_text('import sys; print(\'{"cancel":false,"contextModification":"unrecorded"}\'); sys.exit(2)',encoding='utf-8')
        out = self.ps(exe,'TaskStart',{'taskId':'test-1'},nested)
        self.assertTrue(out['cancel']);self.assertEqual(out.get('contextModification'),'')
    def test_kilo_project_shell_asks(self):
        cfg=json.loads((ROOT/'.kilo/kilo.jsonc').read_text(encoding='utf-8'))
        self.assertEqual(cfg['permission']['bash'],'ask')

if __name__=='__main__':unittest.main()
