# SPDX-License-Identifier: MIT
"""Replay the sealed C1 promise probes in disposable old/new Git checkouts.

Use Python 3.13 and two separate, clean checkouts at the compared commits:
  python scripts/replay_upgrade_promise_mutants.py --old /tmp/old --new /tmp/new \
    --output /tmp/upgrade-mutant-results

The fixture preserves the independently sealed patches. One named test
per mutant establish baseline health, execution reach and retained protection.
No suite, security attestation or release operation is performed. Logs and JSON
results go only to --output; every engine patch is restored in finally.
"""
import argparse, json, os, subprocess, sys, time
from pathlib import Path
PYTHON=sys.executable
TEST='bootstrap/tests/test_upgrade.py::'
MAP={
'P1-hash':('TestLockfile::test_round_trip',)*2,
'P2-profile':('TestProfileSizedAssembly::test_profile_change_solo_to_multi_reincludes_region',)*2,
'P3-plan-write':('TestUpgradeModes::test_plan_writes_nothing',)*2,
'P4-valid-noop':('TestUpgradeModes::test_stage_then_apply',)*2,
'P4-accept-conflict':('TestUpgradeModes::test_apply_rejects_conflict_markers',)*2,
'P5-migration-tokens':('TestInitLockFullProfile::test_with_config_embeds_full_profile',)*2,
'P6-citation':('TestManifestHomeAndSelfHeal::test_r10_finds_manifest_in_cairn_home','TestManifestHomeAndSelfHeal::test_plan_reports_citation_status_through_public_command'),
'P6-precedence':('TestManifestHomeAndSelfHeal::test_r10_prefers_cairn_over_legacy','TestManifestHomeAndSelfHeal::test_plan_reports_citation_status_through_public_command'),
'P7-base':('TestUpgradeModes::test_finalize_preserves_verbatim_fork_detection',)*2,
'P8-preserve':('TestAdoptModule::test_adopt_advisory_fires_when_kept_file_differs',)*2,
'P8-accept-unknown':('TestAdoptModule::test_adopt_unknown_module_fails_closed',)*2,
'P9-allow':('TestLockfile::test_secret_token_guard','TestLockfile::test_public_writer_refuses_secret_tokens_without_writing_state'),
'P9-accept-secret':('TestAdoptModule::test_adopt_secret_shaped_required_token_refuses_closed',)*2,
}
CHILD=r'''
import json,sys,pytest
from pathlib import Path
source=str(Path(sys.argv[1]).resolve()); lines=set(); phases=[]; side_effects=[]
def tracer(frame,event,arg):
 if frame.f_code.co_filename == source:
  if event=='line': lines.add(frame.f_lineno)
  return tracer
 return None
class Outcomes:
 def pytest_runtest_teardown(self,item):
  project=item.funcargs.get('tmp_path')
  if project is not None:
   marker=project/'cairn-plan-mutant-write'
   if marker.is_file(): side_effects.append({'path':str(marker),'content':marker.read_text()})
 def pytest_runtest_logreport(self,report):
  phases.append([report.when,report.outcome])
sys.settrace(tracer)
code=pytest.main([sys.argv[2],'-q','--tb=short','-p','no:cacheprovider'],plugins=[Outcomes()])
sys.settrace(None)
Path(sys.argv[3]).write_text(json.dumps({'code':int(code),'lines':sorted(lines),'phases':phases,'side_effects':side_effects}))
raise SystemExit(int(code))
'''
def probe(root,node,source,out):
 started=time.monotonic()
 result=subprocess.run([PYTHON,'-c',CHILD,str(root/source),TEST+node,str(out.with_suffix('.trace.json'))],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},timeout=150)
 out.write_text(result.stdout)
 data=json.loads(out.with_suffix('.trace.json').read_text());data['seconds']=round(time.monotonic()-started,3)
 return data
def main():
 p=argparse.ArgumentParser();p.add_argument('--data',type=Path,default=Path(__file__).resolve().parents[1]/'bootstrap/tests/fixtures/upgrade_promise_mutants.json');p.add_argument('--old',type=Path,required=True);p.add_argument('--new',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--only',choices=tuple(MAP));a=p.parse_args()
 a.output.mkdir(exist_ok=True)
 sealed=json.loads(a.data.read_text()); records=[]
 if sys.version_info[:2] != (3,13): p.error('use canonical Python 3.13')
 if a.old.resolve() == a.new.resolve(): p.error('old and new must be separate checkouts')
 for root in (a.old,a.new):
  if subprocess.run(['git','-C',str(root),'diff','--quiet','HEAD']).returncode:
   p.error(f'checkout has tracked changes: {root}')
 for rel in {m['file'] for m in sealed['mutants']} | {'bootstrap/scaffold.py'}:
  if (a.old/rel).read_bytes() != (a.new/rel).read_bytes():
   p.error(f'engine source differs: {rel}')
 for idx,root in enumerate((a.old,a.new)):
  label=('old','new')[idx]
  for m in sealed['mutants']:
   if a.only and m['id'] != a.only: continue
   path=root/m['file'];original=path.read_text(); assert original.count(m['old'])==1
   node=MAP[m['id']][idx]
   # Each baseline probe uses unchanged committed bytes before its mutation.
   baseline=probe(root,node,Path(m['file']),a.output/f'{label}-{m["id"]}-baseline.log')
   assert baseline['code']==0 and ['call','passed'] in baseline['phases'],(m['id'],label,baseline)
   try:
    path.write_text(original.replace(m['old'],m['new'],1))
    mutated=probe(root,node,Path(m['file']),a.output/f'{label}-{m["id"]}-mutant.log')
   finally: path.write_text(original)
   assert mutated['code'] in (0,1) and mutated['phases'] in (
    [['setup','passed'],['call','passed'],['teardown','passed']],
    [['setup','passed'],['call','failed'],['teardown','passed']],
   ),(m['id'],label,mutated)
   line=m['line']; changed=set(range(line,line+len(m['new'].splitlines())))
   assert changed.intersection(mutated['lines']),(m['id'],label,'NOT REACHED')
   if m['id']=='P3-plan-write':
    assert mutated['side_effects'] and all(x['content']=='changed' for x in mutated['side_effects'])
   r={'id':m['id'],'version':label,'node':TEST+node,'baseline':baseline,'mutated':mutated,'hit_changed_lines':sorted(changed.intersection(mutated['lines']))}
   records.append(r);(a.output/'results.json').write_text(json.dumps(records,indent=2)+'\n')
   print(label,m['id'],'caught' if mutated['code'] else 'SURVIVED',r['hit_changed_lines'],flush=True)
 for root in (a.old,a.new):
  assert subprocess.run(['git','-C',str(root),'diff','--quiet','HEAD']).returncode==0
 # A surviving public behavior fault is unpassed even when both versions miss it.
 return int(any(r['version']=='new' and r['mutated']['code']==0 for r in records))
if __name__=='__main__': raise SystemExit(main())
