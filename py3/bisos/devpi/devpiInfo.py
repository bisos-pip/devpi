# -*- coding: utf-8 -*-

""" #+begin_org
* ~[Summary]~ :: =CS-Lib= The single source of the facts of this host's devpi installation.
#+end_org """

""" #+begin_org
* [[elisp:(org-cycle)][| ~Description~ |]] :: Facts shared by devpi-sbom.pcs, devpiUsage-sbom.pcs, devpiAdmin.cs,
quickDevpi.cs, devpi-sysd.pcs, devpi-accounts-sysd.pcs, devpi-here-dns.pcs and devpi-wvd.pcs: the
account, the isolated venv and its hash-pinned set, the paths, the EnvironmentFile, the fqdn, the banna
port, the logins and the index.
** Pure: importing this module has no side effects and touches no host state.
** devpi-server (with its devpi-web plugin, the web UI) is a Python package index. In a rawBisosCbm
materialization it is *minimal*: no PyPI mirror (devpi-init --no-root-pypi) and 4 threads --- 74 MB
instead of about 500 MB (the mirror indexes all of PyPI's project names at start). A real devpi, with
the mirror, typically runs in a dedicated VM and is configured there.
** Logins (rawBisos convention, insecure by design): root / devpi (devpi's superuser) and admin / devpi,
the owner of the index admin/dev. Only root and admin may create users and indexes (--restrict-modify).
** Status: Starting point.
** /[[elisp:(org-cycle)][| Planned Improvements |]]/ :
*** TODO The "secure it" layer: real passwords, HTTPS, listening beyond loopback.
#+end_org """

####+BEGIN: b:prog:file/proclamations :outLevel 1
""" #+begin_org
* *[[elisp:(org-cycle)][| Proclamations |]]* :: Libre-Halaal Software --- Part Of BISOS ---  Poly-COMEEGA Format.
** This is Libre-Halaal Software. © Neda Communications, Inc. Subject to AGPL.
** It is part of BISOS (ByStar Internet Services OS)
** Best read and edited  with Blee in Poly-COMEEGA (Polymode Colaborative Org-Mode Enhance Emacs Generalized Authorship)
#+end_org """
####+END:

####+BEGIN: b:prog:file/particulars :authors ("./inserts/authors-mb.org")
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: Authors, version
** This File: /bisos/git/bxRepos/bisos-pip/devpi/py3/bisos/devpi/devpiInfo.py
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """
####+END:

import dataclasses
import pathlib

from bisos.banna import tcpPorts as bannaTcpPorts


def _bannaPortNu(portName: str) -> int:
    """The registry, bisos.banna, is authoritative: never hardcode these ports."""
    return bannaTcpPorts.tcpPortsAssignedList.tcpPortsList[portName].portNu


@dataclasses.dataclass(frozen=True)
class DevpiInfo:
    """The facts of this host's devpi installation. Built once, as devpiInfo below."""

    acctName: str = "devpi"

    # devpi is an exception to asc, in a venv of its own under /bisos/venv/py3/isolated/.
    # Reason (2026-10-16): devpi-server 6.20.3 requires setuptools<=81 (and pyramid 2.1 <82), while
    # asc has setuptools 84.0.0; installing into asc would downgrade it (the asc guard refuses).
    # Move back to asc, and delete this venv, when devpi-server accepts the setuptools in asc.
    venv: pathlib.Path = pathlib.Path("/bisos/venv/py3/isolated/devpiServer")
    venvPython: str = "/usr/bin/python3.13"   # asc's base (asc/pyvenv.cfg)
    devpiServerVersion: str = "6.20.3"
    devpiWebVersion: str = "5.1.1"

    # The whole resolved set, each sha256 checked against PyPI's published digest. Several wheels are
    # binary (CPython 3.13, x86_64), so the set is for amd64 + Python 3.13 only.
    reqsArch: str = "amd64"
    reqs: tuple = (
        ("chameleon", "4.6.0", "f674cab262d7b8a26c38574e06f513e91f60c129887ff5ab6a3a2a46c03dd925"),
        ("pastedeploy", "3.1.0", "76388ad53a661448d436df28c798063108f70e994ddc749540d733cdbd1b38cf"),
        ("whoosh", "2.7.4", "aa39c3c3426e3fd107dcb4bde64ca1e276a65a889d9085a6e4b54ba82420a852"),
        ("anyio", "4.15.1", "6152fdbbf9a77fdec97731721bebf7c4c44f7c29b424b0065826173efc7ed101"),
        ("argon2-cffi", "25.1.0", "fdc8b074db390fccb6eb4a3604ae7231f219aa669a2652e0f20e16ba513d5741"),
        ("argon2-cffi-bindings", "26.1.0", "27f1821903e2ceadcb88ec2b45ef190897b7682449c772f4d9b53e42c520cf29"),
        ("attrs", "26.1.0", "c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309"),
        ("beautifulsoup4", "4.15.0", "d6f88de62e1d4e38ecb1077eb9724cd0eff29d2a08ca16a401e9b9e93f117cf9"),
        ("certifi", "2026.7.22", "62f22742b58a1a33014a2b6b706588a8d7e2a88ae7bd1a6ebe8c992928483775"),
        ("cffi", "2.1.1", "a931079504ecc49efed7744c476a5c343a92fabf66dec2db95edb1b2fdc770e2"),
        ("charset-normalizer", "3.5.2", "7218e8f32b0956cfcd048fd42d9d5779809745ca1d86113ca56f66e7ae1549c4"),
        ("comrak", "0.0.16", "5e2e960b2188efcc58f34034906e2eacadea67780b6edc4d501c522835b3d15a"),
        ("defusedxml", "0.7.1", "a352e7e428770286cc899e2542b6cdaedb2b4953ff269a210103ec58f6198a61"),
        ("devpi-common", "4.1.1", "8fda7e8965d3744b1184d6c426fd5caf1345ed74513db687beeb5ee0e63a675c"),
        ("devpi-server", "6.20.3", "4cdc372ce695ad45c7e5eb20f5eaf7e50fd5abe1991db3700f0e68b26e406e67"),
        ("devpi-web", "5.1.1", "13e1aa712b587a6328f728316d565e7e2b257f127502e08d32358710759efb5c"),
        ("docutils", "0.23", "25d013af9bf23bc1c7b2b093dff4208166c53a94786c9e447808335ef1185fea"),
        ("h11", "0.16.0", "63cf8bbe7522de3bf65932fda1d9c2772064ffb3dae62d55932da54b31cb6c86"),
        ("httpcore", "1.0.9", "2d400746a40668fc9dec9810239072b40b4484b640a8c38fd654a024c7a1bf55"),
        ("httpx", "0.28.1", "d909fcccc110f8c7faf814ca82a9a4d816bc5a6dbfea25d6591d6985b8ba59ad"),
        ("hupper", "1.12.1", "e872b959f09d90be5fb615bd2e62de89a0b57efc037bdf9637fb09cdf8552b19"),
        ("idna", "3.20", "ab7ae7122974553370f0bdb919e1a960b2cd1bc1ef0276416d896db81c14582c"),
        ("itsdangerous", "2.2.0", "c6242fc49e35958c8b15141343aa660db5fc54d4f13a1db01a3f5891b98700ef"),
        ("lazy", "2.0", "6bf06f6a71dbe6148f3948c6388b264772493972ad22fb958d24bb52e7e7ec9b"),
        ("legacy-cgi", "2.6.4", "7e235ce58bf1e25d1fc9b2d299015e4e2cd37305eccafec1e6bac3fc04b878cd"),
        ("nh3", "0.3.7", "70f5ac8626e899a4bab0ef74ca2f5bd602f49c7b739e6e5026b4afc6d63dac42"),
        ("packaging", "26.3", "d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c"),
        ("packaging-legacy", "23.0.post0", "6cd21cd283c09409349bccc10bb55bfd837b4aab86a7b0f87bfcb8dd9831a8a3"),
        ("passlib", "1.7.4", "aa6bca462b8d8bda89c70b382f0c298a20b5560af6cbfa2dce410c0a2fb669f1"),
        ("plaster", "1.1.2", "42992ab1f4865f1278e2ad740e8ad145683bb4022e03534265528f0c23c0df2d"),
        ("plaster-pastedeploy", "1.0.1", "ad3550cc744648969ed3b810f33c9344f515ee8d8a8cec18e8f2c4a643c2181f"),
        ("platformdirs", "4.13.3", "f6ad7f447f24f8a3b82cce5976387428bff894a0eca6c3488f4a17f153c130c4"),
        ("pluggy", "1.7.0", "7dd7b0d8832ba3cb632c306926ded123429211b83641b35dc5c41ad2d34f9bec"),
        ("py", "1.11.0", "607c53218732647dff4acdfcd50cb62615cedf612e72d1724fb1a0cc6405b378"),
        ("pycparser", "3.11", "51d5a8ba2be0bbe440b99d2112604c95bbbc3c2748a64260186c541e1729cd80"),
        ("pygments", "2.21.0", "2363c69b61c4a97c838da3b130dcd6468f4848992b21a82f2a63ec34377137d9"),
        ("pyramid", "2.1", "0aa62604221f6a8ac6e77a0faa02a5b7a294d6675f15581d8d416dffe2ac98e7"),
        ("pyramid-chameleon", "0.3", "d176792a50eb015d7865b44bd9b24a7bd0489fa9a5cebbd17b9e05048cef9017"),
        ("python-dateutil", "2.9.0.post0", "a8b2bc7bffae282281c8140a97d3aa9c14da0b136dfe83f850eea9a5f7470427"),
        ("readme-renderer", "46.0", "d0dae1f74bb273b534770cb4cccb6bb78735540afdb03c2146f4e19dcd412560"),
        ("repoze-lru", "0.8", "979a30d2e567e31f292009ba4467aa444c89ee0da3e3013980c35f1fb4f19d99"),
        ("requests", "2.34.2", "2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0"),
        ("ruamel-yaml", "0.19.1", "27592957fedf6e0b62f281e96effd28043345e0e66001f97683aa9a40c667c93"),
        ("setuptools", "81.0.0", "fdd925d5c5d9f62e4b74b30d6dd7828ce236fd6ed998a08d81de62ce5a6310d6"),
        ("six", "1.17.0", "4721f391ed90541fddacab5acf947aa0d3dc7d27b2e1e8eda2be8970586c3274"),
        ("soupsieve", "3.0.3", "fa30e3ba4809cb81ce1f3209f2fbe3e779fc445f0439bc147a0d7c4601743f21"),
        ("strictyaml", "1.7.3", "fb5c8a4edb43bebb765959e420f9b3978d7f1af88c80606c03fb420888f5d1c7"),
        ("translationstring", "1.4", "5f4dc4d939573db851c8d840551e1a0fb27b946afe3b95aafc22577eed2d6262"),
        ("typing-extensions", "4.16.0", "481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8"),
        ("urllib3", "2.8.0", "0cf3cae568d36aa9576b28dfb35f11328f1cb974ca7647d9475ebb86c75ac6e3"),
        ("venusian", "3.1.1", "0845808a985976acbceaa1fbb871c7fac4fb28ae75453232970e9c2c2866dbf4"),
        ("waitress", "3.0.2", "c56d67fd6e87c2ee598b76abdd4e96cfad1f24cacdea5078d382b1f9d7b5ed2e"),
        ("webob", "1.8.11", "4addd1d38d6a7fbe0eda22d45f25a40d74c8b290f3a99c0ac3d4023cf21f2da2"),
        ("zope-deprecation", "6.0", "ff72d51c88b516b9ddf2cfb826381cc49f99a6a89b7d35c97faca7bee3b46da6"),
        ("zope-interface", "8.7", "d30ed06ef78e9e1b41a50683b7d01727a3c363143c5bda09017e33f19827afc2"),
    )

    # The usage side: devpi-client (the devpi command), a CLI, through pipx (/bisos/pipx).
    clientVersion: str = "7.3.0"

    confDir: pathlib.Path = pathlib.Path("/etc/devpi")
    dataDir: pathlib.Path = pathlib.Path("/var/lib/devpi")

    # Read by systemd as root before the units drop to User=. root:acctName 640.
    envFile: pathlib.Path = pathlib.Path("/etc/default/devpi")

    listenIp: str = "127.0.0.1"
    fqdn: str = "devpi.here"
    threads: int = 4

    # rawBisos convention: user admin, password the service's name. root is devpi's superuser.
    rootPassword: str = "devpi"
    adminUser: str = "admin"
    adminPassword: str = "devpi"
    indexName: str = "dev"

    portNu: int = dataclasses.field(default_factory=lambda: _bannaPortNu('devpi'))

    def venvBin(self, name: str) -> pathlib.Path:
        return self.venv / "bin" / name

    @property
    def serverDir(self) -> pathlib.Path:
        """devpi's state: users, indexes, uploaded files. Owned by the account."""
        return self.dataDir / "server"

    @property
    def serverVersionFile(self) -> pathlib.Path:
        """Written by devpi-init. Its presence means the server directory is initialized."""
        return self.serverDir / ".serverversion"

    @property
    def accountsScript(self) -> pathlib.Path:
        """The script the devpi-accounts oneshot unit runs (accountsScriptContent())."""
        return self.confDir / "devpi-accounts.py"

    @property
    def listenAddr(self) -> str:
        return f"{self.listenIp}:{self.portNu}"

    @property
    def baseUrl(self) -> str:
        """The address humans browse (devpi-web) and clients use, through nginx."""
        return f"http://{self.fqdn}"

    @property
    def localUrl(self) -> str:
        """Straight to devpi-server, bypassing nginx."""
        return f"http://{self.listenAddr}"

    @property
    def index(self) -> str:
        return f"{self.adminUser}/{self.indexName}"

    @property
    def indexUrl(self) -> str:
        """What pip uses (the simple API of admin/dev)."""
        return f"{self.baseUrl}/{self.index}/+simple/"

    @property
    def uploadUrl(self) -> str:
        """What twine uses: --repository-url."""
        return f"{self.baseUrl}/{self.index}/"

    @property
    def pipIndexArgs(self) -> str:
        """pip arguments to use this index alone (--trusted-host: pip ignores plain HTTP otherwise)."""
        return f"--index-url {self.indexUrl} --trusted-host {self.fqdn}"

    @property
    def pipExtraIndexArgs(self) -> str:
        """pip arguments to use this index together with PyPI."""
        return f"--extra-index-url {self.indexUrl} --trusted-host {self.fqdn}"

    @property
    def clientBin(self) -> pathlib.Path:
        return pathlib.Path("/bisos/pipx/bin/devpi")


# A Singleton
devpiInfo = DevpiInfo()


def reqsContent(info: DevpiInfo = devpiInfo) -> str:
    """The hashed requirements file of devpi's isolated venv."""
    return "".join(f"{n}=={v} --hash=sha256:{h}\n" for n, v, h in info.reqs)


def isolatedVenvSetupScript(venv: pathlib.Path, python: str, reqs: str, arch: str) -> str:
    """Bash: an isolated venv, created once, then a hashed set installed into it. Idempotent.

    pip --require-hashes --no-deps: every file is checked against its pinned sha256, and nothing
    outside the set is pulled in. Satisfied pins are a no-op; a bumped set is applied. Refused on an
    architecture the hashes do not cover. (As bisos.pypiserver's browserVenvSetupScript.)
    """
    return f"""
set -e
a=$(dpkg --print-architecture)
[ "$a" = "{arch}" ] || {{ echo "{venv.name}: hashed set covers {arch} only, not $a" >&2; exit 1; }}
if [ ! -x {venv}/bin/pip ] ; then
    mkdir -p {venv.parent}
    {python} -m venv {venv}
fi
reqs=$(mktemp)
trap 'rm -f "$reqs"' EXIT
cat > "$reqs" <<'ISOLATED_REQS_EOF'
{reqs}ISOLATED_REQS_EOF
{venv}/bin/pip install --quiet --disable-pip-version-check --require-hashes --no-deps -r "$reqs"
{venv}/bin/pip check
"""


def venvSetupScript(info: DevpiInfo = devpiInfo) -> str:
    return isolatedVenvSetupScript(info.venv, info.venvPython, reqsContent(info), info.reqsArch)


def initScript(info: DevpiInfo = devpiInfo) -> str:
    """Bash: devpi-init the server directory, once, minimal: no root/pypi mirror, root's password set.

    Run as the account; skipped when .serverversion exists.
    """
    return f"""
if ! sudo test -f {info.serverVersionFile} ; then
    sudo -u {info.acctName} {info.venvBin("devpi-init")} --serverdir {info.serverDir} \\
        --no-root-pypi --root-passwd {info.rootPassword}
fi
"""


def clientSetupScript(info: DevpiInfo = devpiInfo) -> str:
    """Bash: devpi-client at its pin, through pipx. Idempotent; reinstalls on a version bump.

    bisos.sbom's pipxPkgsList ignores versions and skips installed packages (AI-Outputs.org).
    """
    probe = "import importlib.metadata as m; print(m.version('devpi-client'))"
    return f"""
set -e
current=$(/bisos/pipx/venvs/devpi-client/bin/python -c "{probe}" 2>/dev/null || true)
if [ "$current" != "{info.clientVersion}" ] ; then
    pipx install --force 'devpi-client=={info.clientVersion}'
fi
"""


def envFileContent(info: DevpiInfo = devpiInfo) -> str:
    """The content /etc/default/devpi is generated with. Written only when absent.

    ARGS is expanded by the unit's ExecStart as separate words ($ARGS). --outside-url makes the links
    devpi-web renders point at devpi.here; --restrict-modify lets only root and admin create users and
    indexes (devpi's default lets anyone).
    """
    return (
        f'ARGS="--serverdir {info.serverDir} --host {info.listenIp} --port {info.portNu}'
        f' --threads {info.threads} --outside-url {info.baseUrl}'
        f' --restrict-modify root,{info.adminUser}"\n'
        "# Add flags to ARGS above. No PyPI mirror (root/pypi): --no-root-pypi at init.\n"
    )


_ACCOUNTS_SCRIPT = """\
import base64, json, sys, time, urllib.error, urllib.request
# Generated by devpi-sbom.pcs from bisos.devpi.devpiInfo. Rewritten on every sbom run.
BASE = "@BASE@"


def call(method, path, body=None, auth=None):
    req = urllib.request.Request(BASE + path, method=method,
                                 data=None if body is None else json.dumps(body).encode(),
                                 headers={"Accept": "application/json",
                                          "Content-Type": "application/json"})
    if auth:
        req.add_header("X-Devpi-Auth", base64.b64encode(("%s:%s" % auth).encode()).decode())
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None


def login(user, password):
    status, body = call("POST", "/+login", {"user": user, "password": password})
    if status != 200:
        sys.exit("devpi-accounts: login %s failed: %s" % (user, status))
    return (user, body["result"]["password"])


for _ in range(60):
    try:
        urllib.request.urlopen(BASE + "/+api", timeout=5)
        break
    except Exception:
        time.sleep(1)
else:
    sys.exit("devpi-accounts: devpi-server did not answer at " + BASE)

root = login("root", "@ROOTPW@")
status, _ = call("PUT", "/@ADMIN@", {"password": "@ADMINPW@"}, root)
if status not in (200, 201, 409):
    sys.exit("devpi-accounts: creating user @ADMIN@: %s" % status)
admin = login("@ADMIN@", "@ADMINPW@")
status, _ = call("GET", "/@INDEX@")
if status == 404:
    status, _ = call("PUT", "/@INDEX@", {"type": "stage", "bases": [], "volatile": True}, admin)
    if status not in (200, 201):
        sys.exit("devpi-accounts: creating index @INDEX@: %s" % status)
print("devpi-accounts: @ADMIN@ and @INDEX@ present")
"""


def accountsScriptContent(info: DevpiInfo = devpiInfo) -> str:
    """The devpi-accounts unit's script: the admin user and its index, created if absent. Idempotent.

    Standard library only, run by the isolated venv's python. Waits for the server, then over the
    HTTP API: logs in as root, creates admin (409 when it exists), logs in as admin, creates admin/dev
    (a volatile stage with no bases: uploads only, no mirror). Rewritten by the sbom on every run: it
    is code, not configuration. It cannot run in the assemble step: cbs_materialize runs sbom,
    assemble, then the units, so the server is not up yet then.
    """
    return (_ACCOUNTS_SCRIPT
            .replace("@BASE@", info.localUrl)
            .replace("@ROOTPW@", info.rootPassword)
            .replace("@ADMINPW@", info.adminPassword)
            .replace("@ADMIN@", info.adminUser)
            .replace("@INDEX@", info.index))


def sysdServiceLines(envFile: pathlib.Path, info: DevpiInfo = devpiInfo) -> str:
    """The identity lines every devpi unit has in its [Service] section."""
    return (
        f"User={info.acctName}\n"
        f"Group={info.acctName}\n"
        f"EnvironmentFile={envFile}\n"
    )


def _kvMap(text: str) -> dict[str, str]:
    """KEY=VALUE lines of an EnvironmentFile; comments and blank lines are skipped."""
    pairs: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        pairs[key.strip()] = value.strip()
    return pairs


def kvDrift(liveText: str, generatedText: str) -> dict[str, list]:
    """Compare a live KEY=VALUE file with its generator: missing, differs, extra."""
    expected = _kvMap(generatedText)
    live = _kvMap(liveText)
    return {
        "missing": [k for k in expected if k not in live],
        "differs": [(k, expected[k], live[k]) for k in expected if k in live and live[k] != expected[k]],
        "extra": [k for k in live if k not in expected],
    }


def unitDrift(unitText: str, envFile: pathlib.Path, info: DevpiInfo = devpiInfo) -> list[str]:
    """The identity lines (sysdServiceLines) that an installed unit file lacks."""
    present = {line.strip() for line in unitText.splitlines()}
    return [line for line in sysdServiceLines(envFile, info).splitlines() if line not in present]


####+BEGIN: b:py3:cs:framework/endOfFile :basedOn "classification"
""" #+begin_org
* [[elisp:(org-cycle)][| *End-Of-Editable-Text* |]] :: emacs and org variables and control parameters
#+end_org """

#+STARTUP: showall

### local variables:
### no-byte-compile: t
### end:
####+END:
