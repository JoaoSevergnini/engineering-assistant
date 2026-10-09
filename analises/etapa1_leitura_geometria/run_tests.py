from pathlib import Path
import os,subprocess,json,re,hashlib
ROOT=Path(__file__).resolve().parents[2]
rows=[]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8')
for suite in ('beam_model','extrator_lst','beam_mapping','reinforcement_checks'):
    command=['py','-3.11','-m','unittest','discover','-s','tools/'+suite,'-p','test_*.py','-q']
    result=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8')
    output=result.stdout+result.stderr
    match=re.search(r'Ran (\d+) tests? in ([\d.]+)s',output)
    rows.append(dict(suite=suite,command=command,tests=int(match[1]) if match else None,seconds=float(match[2]) if match else None,
                     exit_code=result.returncode,passed=result.returncode==0,output=output))
    print(suite,rows[-1]['tests'],result.returncode,flush=True)
    if result.returncode:
        print(output,flush=True)
report=dict(suites=rows,total=sum(r['tests'] or 0 for r in rows),all_passed=all(r['passed'] for r in rows),
            interpreter='CPython 3.11',concretopy_modified=False,pranchas_modified=False)
Path(__file__).with_name('test_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if not report['all_passed']:raise SystemExit(1)
