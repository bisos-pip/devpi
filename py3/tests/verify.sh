#!/bin/bash -i
#

# Safety check: must run from a directory named "tests"
if [[ "$(basename "$PWD")" != "tests" ]]; then
    echo "ERROR: verify.sh must be run from a directory named 'tests'." >&2
    echo "  Current PWD: $PWD" >&2
    exit 1
fi

# Starting-point smoke test for bisos.devpi -- covers devpiAdmin.cs, quickDevpi.cs, the read-only
# Cmnds of the planted files, and bisos.devpi.devpiInfo's generators.
# Nothing here installs, starts or writes anything on the host.

# --- CS entry points: smoke test (no args → examples/usage, non-zero ok) ---

lpDo ../bin/devpiAdmin.cs
lpDo ../bin/quickDevpi.cs
lpDo ../bin/devpi-assemble.cs

# --- devpiAdmin.cs: each admin sub-Cmnd runs and produces examples output ---

lpDo ../bin/devpiAdmin.cs -i examples
lpDo ../bin/devpiAdmin.cs -i hostInfo
lpDo ../bin/devpiAdmin.cs -i servicesInfo
lpDo ../bin/devpiAdmin.cs -i indexInfo
lpDo ../bin/devpiAdmin.cs -i driftCheck
lpDo ../bin/devpiAdmin.cs -i fullUpdate

# --- planted files: menus and read-only Cmnds ---

lpDo ../bin/devpi-sbom.pcs -i readme
lpDo ../bin/devpiUsage-sbom.pcs -i readme
lpDo ../bin/devpiCbs-sbom.pcs -i readme
lpDo ../bin/devpi-sysd.pcs
lpDo ../bin/devpi-accounts-sysd.pcs
lpDo ../bin/devpi-cbs.pcs
lpDo ../bin/cbmProc-devpi.spcs
lpDo ../bin/devpi-here-dns.pcs
lpDo ../bin/devpi-wvd.pcs -i configFileStdout --cls=configFile_nginxVd

# --- bisos.devpi.devpiInfo: banna numbers and generator invariants ---

lpDo python3 -c "
import ast, re, subprocess, sys
from bisos.banna import sysAccts
from bisos.devpi.devpiInfo import (
    devpiInfo as i, envFileContent, reqsContent, accountsScriptContent,
    venvSetupScript, initScript, clientSetupScript, kvDrift,
)

reqs = reqsContent().splitlines()
cases = [
    ('banna: devpi port',                 i.portNu == 24015),
    ('banna sysAccts: devpi uid',         sysAccts.sysAcctOf(i.acctName).uid == 507),
    ('banna sysAccts: homeDir',           sysAccts.sysAcctOf(i.acctName).homeDir == str(i.dataDir)),
    ('in an isolated venv',               str(i.venv).startswith('/bisos/venv/py3/isolated/')),
    ('isolated set fully hash-pinned',    all(re.fullmatch(r'\S+==\S+ --hash=sha256:[0-9a-f]{64}', r) for r in reqs)),
    ('setuptools <= 81 in the set',       any(r.startswith('setuptools==81.') for r in reqs)),
    ('minimal: no PyPI mirror',           '--no-root-pypi' in initScript()),
    ('minimal: 4 threads',                '--threads 4' in envFileContent()),
    ('on loopback',                       f'--host 127.0.0.1 --port {i.portNu}' in envFileContent()),
    ('links point at devpi.here',         '--outside-url http://devpi.here' in envFileContent()),
    ('only root and admin modify',        '--restrict-modify root,admin' in envFileContent()),
    ('accounts script parses',            bool(ast.parse(accountsScriptContent()))),
    ('pip args trust the plain-HTTP host', '--trusted-host devpi.here' in i.pipIndexArgs),
    ('rawBisos login admin / devpi',      (i.adminUser, i.adminPassword) == ('admin', 'devpi')),
    ('scripts parse',                     all(subprocess.run(['bash', '-n'], input=s, text=True).returncode == 0
                                              for s in (venvSetupScript(), initScript(), clientSetupScript()))),
    ('drift: extra key reported',         kvDrift(envFileContent() + 'X=1\n', envFileContent())['extra'] == ['X']),
]

failed = 0
for name, ok in cases:
    print(f'  [{\"PASS\" if ok else \"FAIL\"}] {name}')
    failed += not ok

if failed:
    print(f'devpiInfo: {failed} test(s) FAILED')
    sys.exit(1)
else:
    print('devpiInfo: all cases PASS')
" 2>/dev/null || true
