"""Docker sandbox: runs user code with tests.

Modes: func (call a function with arguments), stdout (output comparison) and
stdout with an optional hidden "driver" — code that runs after
the student's solution in the same namespace (for classes, files, generators).

Student code and the generated harness are written to a temp directory,
which is mounted into the container read-only. Network is off, with limits on memory,
CPU and process count, and an overall timeout. The harness prints the result as one line
"RESULT_JSON:<json>" — that is what we parse the result from.
"""

import json
import os
import subprocess
import tempfile
import threading
import uuid
from pathlib import Path

IMAGE = "python:3.13-slim"
RUST_IMAGE = "rust:1.97-slim"
# Image with prebuilt crates (tokio, axum, sqlx/SQLite, serde, tower, tungstenite…; docker/rust-crates/Dockerfile);
# used by tasks with a `crates` field — there is no network during a check, rustc gets --extern for the prebuilt rlibs
# from /opt/ext/externs (one `--extern name=path` line per direct crate).
RUST_CRATES_IMAGE = "cs-core-rust-crates:1"
# Tasks with `postgres: True` get a running PostgreSQL: the ready cluster from the image is copied to tmpfs
# (read-only root FS) and started as the postgres user on 127.0.0.1:5432 (trust, database chat);
# connection string is postgres://postgres@127.0.0.1/chat. No fsync: the data is disposable.
PG_START = (
    "cp -a /opt/pgdata /tmp/pgdata && "
    "runuser -u postgres -- /opt/pgbin/pg_ctl -D /tmp/pgdata -w -l /tmp/pg.log "
    "-o '-c listen_addresses=127.0.0.1 -c unix_socket_directories=/tmp -c fsync=off "
    "-c synchronous_commit=off -c full_page_writes=off -c shared_buffers=16MB -c max_connections=40' "
    "start >/dev/null || { echo COMPILE_ERROR; echo 'failed to start PostgreSQL'; cat /tmp/pg.log; exit 0; }; "
)
RUST_TIMEOUT_SEC = 60
RUST_MEMORY = "1g"
RUST_CPUS = "2.0"
RUST_COMPILE_ERR_LIMIT = 3000
C_IMAGE = RUST_IMAGE  # the rust:slim image has gcc 14, libc and sanitizers
C_DEFAULT_FLAGS = "-std=gnu11 -O1 -g0 -Wall"
JS_IMAGE = "node:22-alpine"
TIMEOUT_SEC = 25
MEMORY = "256m"
CPUS = "1.0"
PIDS_LIMIT = "64"

MARK = "RESULT_JSON:"

# --- running the container ---------------------------------------------------------------------
# How many bytes of stdout/stderr we accept from the student's program: the rest is discarded,
# and a container that floods the output is stopped (otherwise it would fill the checker process's memory).
OUTPUT_LIMIT = 1_000_000
CONTAINER_PREFIX = "cs-core-run-"
# Minimal privileges: everything the compiler and the program need is available without them.
HARDENING = [
    "--cap-drop", "ALL",
    "--security-opt", "no-new-privileges",
    "--ulimit", "core=0",
    "--ulimit", "nofile=1024:1024",
]
# PostgreSQL tasks need root inside the container to copy the cluster and start the database as postgres.
PG_CAPS = ["--cap-add", "CHOWN", "--cap-add", "DAC_OVERRIDE", "--cap-add", "FOWNER", "--cap-add", "SETUID", "--cap-add", "SETGID", "--cap-add", "KILL"]
NOBODY = ["--user", "65534:65534"]


def _remove_container(name: str) -> None:
    subprocess.run(["docker", "rm", "-f", name], capture_output=True, timeout=30)


def remove_stale_containers() -> int:
    """Removes check containers left over after a process crash (called at worker start)."""
    try:
        ids = subprocess.run(
            ["docker", "ps", "-aq", "--filter", f"name={CONTAINER_PREFIX}"], capture_output=True, text=True, timeout=30
        ).stdout.split()
        if ids:
            subprocess.run(["docker", "rm", "-f", *ids], capture_output=True, timeout=60)
        return len(ids)
    except (OSError, subprocess.SubprocessError):
        return 0


def _run_container(args: list[str], timeout: int) -> subprocess.CompletedProcess:
    """`docker run` with a name, an output cap and a guaranteed container stop.

    On timeout the docker client is killed while the container itself would keep running (an infinite loop
    would spin forever), so the container is stopped by name. Raises subprocess.TimeoutExpired."""
    name = CONTAINER_PREFIX + uuid.uuid4().hex[:12]
    proc = subprocess.Popen(
        ["docker", "run", "--rm", "--name", name, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    bufs: dict[str, bytearray] = {"out": bytearray(), "err": bytearray()}
    flooded = threading.Event()

    def pump(stream, key: str) -> None:
        fd = stream.fileno()
        buf = bufs[key]
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                return
            room = OUTPUT_LIMIT - len(buf)
            if room > 0:
                buf += chunk[:room]
            if len(chunk) > room and not flooded.is_set():
                flooded.set()
                threading.Thread(target=_remove_container, args=(name,), daemon=True).start()

    threads = [
        threading.Thread(target=pump, args=(proc.stdout, "out"), daemon=True),
        threading.Thread(target=pump, args=(proc.stderr, "err"), daemon=True),
    ]
    for t in threads:
        t.start()
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        _remove_container(name)
        proc.wait()
        raise
    finally:
        for t in threads:
            t.join(timeout=5)
        if proc.poll() is None:
            proc.kill()
    out = bufs["out"].decode("utf-8", errors="replace")
    err = bufs["err"].decode("utf-8", errors="replace")
    if flooded.is_set():
        err = (err + f"\nThe program output exceeded {OUTPUT_LIMIT // 1000} KB; execution stopped.").strip()
        return subprocess.CompletedProcess(proc.args, 1, out, err)
    return subprocess.CompletedProcess(proc.args, proc.returncode, out, err)


def _open_dir(sandbox: Path, files: dict[str, str]) -> None:
    """Sandbox files are readable by any user: the container runs unprivileged."""
    os.chmod(sandbox, 0o755)
    for name, text in files.items():
        f = sandbox / name
        f.write_text(text, encoding="utf-8")
        os.chmod(f, 0o644)

# Harness for "function" mode: imports solution.py, calls the function
# with the test arguments and compares the returned value with the expected one.
HARNESS_FUNC = r"""\
import contextlib
import importlib.util
import io
import json
import sys
import traceback

def _dec(x):
    if isinstance(x, dict):
        if set(x) == {{"__tuple__"}}:
            return tuple(_dec(i) for i in x["__tuple__"])
        return {{k: _dec(v) for k, v in x.items()}}
    if isinstance(x, list):
        return [_dec(i) for i in x]
    return x

results = []
load_error = None
spec = importlib.util.spec_from_file_location("solution", "/sandbox/solution.py")
mod = importlib.util.module_from_spec(spec)
try:
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
except Exception:
    load_error = traceback.format_exc(limit=3).strip()

if load_error is not None:
    results = [
        {{"ok": False, "error": "The code crashes on start:\n" + load_error}}
    ] * {n}
else:
    fn = getattr(mod, {func!r}, None)
    if fn is None:
        results = [
            {{"ok": False, "error": "Function {func} not found. Check the name and its case."}}
        ] * {n}
    else:
        tests = _dec(json.loads({tests!r}))
        for args, expected in tests:
            try:
                got = fn(*args)
                results.append({{
                    "ok": got == expected,
                    "args": repr(args),
                    "expected": repr(expected),
                    "got": repr(got),
                }})
            except Exception as e:
                results.append({{
                    "ok": False,
                    "args": repr(args),
                    "expected": repr(expected),
                    "error": "{{}}: {{}}".format(type(e).__name__, e),
                }})

print("RESULT_JSON:" + json.dumps(results, ensure_ascii=False))
"""

# Harness for "output" mode: runs solution.py as a program,
# captures stdout and compares line by line (trailing whitespace
# is ignored).
HARNESS_STDOUT = r"""\
import contextlib
import io
import json
import traceback

buf = io.StringIO()
pre = io.StringIO()
error = None
driver = {driver!r}
try:
    code = open("/sandbox/solution.py", encoding="utf-8").read()
    ns = {{"__name__": "__main__"}}
    if driver:
        # "driver" mode: the student's code only defines classes/functions, and
        # the hidden driver prints what is compared with the expected output
        with contextlib.redirect_stdout(pre):
            exec(compile(code, "solution.py", "exec"), ns)
        with contextlib.redirect_stdout(buf):
            exec(compile(driver, "driver.py", "exec"), ns)
    else:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, "solution.py", "exec"), ns)
except Exception:
    error = traceback.format_exc(limit=3).strip()

if pre.getvalue():
    print(pre.getvalue(), end="")
got = buf.getvalue()
expected = {expected!r}
def norm(s):
    lines = [line.rstrip() for line in s.strip("\\n").split("\\n")]
    return lines
ok = error is None and norm(got) == norm(expected)
result = [{{"ok": ok, "got": got, "expected": expected, "error": error}}]
print("RESULT_JSON:" + json.dumps(result, ensure_ascii=False))
"""


# Harness for "sql" mode: the student's query runs in SQLite on a prepared
# database (setup). The result of the student's last SELECT or of the check
# query (if given) is compared — as a set of rows or in order (ordered).
# contains — substrings that must appear in the result (for query plans),
# forbid — substrings that must not appear.
HARNESS_SQL = r"""\
import json
import sqlite3

def cell(v):
    return round(v, 4) if isinstance(v, float) else v

def fmt(rows):
    return "\n".join(" | ".join("NULL" if v is None else str(v) for v in r) for r in rows)

def table(rows):
    # columns are width-aligned: text left, numbers right, no trailing padding on the last column
    cells = [["NULL" if v is None else str(v) for v in r] for r in rows]
    if not cells:
        return ""
    n = max(len(r) for r in cells)
    widths = [max((len(r[j]) for r in cells if j < len(r)), default=0) for j in range(n)]
    num = [all(isinstance(r[j], (int, float)) or r[j] is None for r in rows if j < len(r)) for j in range(n)]
    lines = []
    for raw, r in zip(rows, cells):
        parts = []
        for j, v in enumerate(r):
            last = j == len(r) - 1
            parts.append(v.rjust(widths[j]) if num[j] else (v if last else v.ljust(widths[j])))
        lines.append(" | ".join(parts))
    return "\n".join(lines)

def statements(sql):
    buf, out = "", []
    for line in sql.splitlines(keepends=True):
        buf += line
        if sqlite3.complete_statement(buf):
            out.append(buf.strip())
            buf = ""
    if buf.strip():
        out.append(buf.strip())
    return out

error = None
got = []
cols = []
try:
    con = sqlite3.connect(":memory:", isolation_level=None)
    con.executescript(SETUP)
    code = open("/sandbox/solution.py", encoding="utf-8").read()
    last = None
    for st in statements(code):
        cur = con.execute(st)
        if cur.description is not None:
            last = [tuple(cell(v) for v in r) for r in cur.fetchall()]
            cols = [d[0] for d in cur.description]
    if CHECK:
        cur = con.execute(CHECK)
        cols = [d[0] for d in cur.description]
        got = [tuple(cell(v) for v in r) for r in cur.fetchall()]
    elif last is None:
        raise ValueError("The query returned nothing: a SELECT is needed")
    else:
        got = last
except Exception as e:
    error = type(e).__name__ + ": " + str(e)

exp = [tuple(cell(v) for v in r) for r in EXPECTED]
if CONTAINS:
    text = fmt(got)
    ok = error is None and all(c in text for c in CONTAINS) and not any(f in text for f in FORBID)
    shown_expected = "the result must contain: " + ", ".join(CONTAINS)
    if FORBID:
        shown_expected += "; must not contain: " + ", ".join(FORBID)
else:
    if ORDERED:
        ok = error is None and got == exp
    else:
        ok = error is None and sorted(got, key=repr) == sorted(exp, key=repr)
    shown_expected = table(exp)
result = [{
    "ok": ok,
    "got": table(got) if not CONTAINS else fmt(got),
    "expected": shown_expected,
    "error": error,
    "kind": "text" if CONTAINS else "rows",
    "ordered": ORDERED,
    "got_cols": cols,
    "got_rows": [list(r) for r in got[:LIMIT_ROWS]],
    "got_total": len(got),
    "exp_cols": EXPCOLS,
    "exp_rows": [list(r) for r in exp[:LIMIT_ROWS]],
    "exp_total": len(exp),
}]
print("RESULT_JSON:" + json.dumps(result, ensure_ascii=False, default=str))
"""


def _enc(x):
    """Tuples in tests (arguments and expected) travel through JSON with a tag —
    the harness returns them as tuples, so [1, 2] and (1, 2) are distinguished."""
    if isinstance(x, tuple):
        return {"__tuple__": [_enc(i) for i in x]}
    if isinstance(x, list):
        return [_enc(i) for i in x]
    if isinstance(x, dict):
        return {k: _enc(v) for k, v in x.items()}
    return x


def _harness(task: dict) -> str:
    if task["mode"] == "func":
        return HARNESS_FUNC.format(
            n=len(task["tests"]),
            func=task["func"],
            tests=json.dumps(
                [_enc([t["args"], t["expected"]]) for t in task["tests"]]
            ),
        )
    if task["mode"] == "sql":
        header = (
            f"SETUP = {task['setup']!r}\n"
            f"CHECK = {task.get('check', '')!r}\n"
            f"EXPECTED = {task.get('expected', [])!r}\n"
            f"EXPCOLS = {task.get('expected_cols', [])!r}\n"
            f"LIMIT_ROWS = 200\n"
            f"ORDERED = {bool(task.get('ordered', False))!r}\n"
            f"CONTAINS = {task.get('contains', [])!r}\n"
            f"FORBID = {task.get('forbid', [])!r}\n"
        )
        return header + HARNESS_SQL
    expected = "\n".join(task["expected"]) + "\n"
    return HARNESS_STDOUT.format(expected=expected, driver=task.get("driver", ""))


def _docker_failed(msg: str, status: str = "docker_error") -> dict:
    return {"status": status, "results": [], "stdout": "", "stderr": msg}


def wrap_rust_driver(driver: str) -> str:
    """The driver goes into its own module: its `use` items do not conflict with
    the student's imports (explicit module imports win over the glob `use super::*`),
    and names from the student's solution are available through `super`."""
    if "async fn main(" in driver:
        body = driver.strip("\n").replace("async fn main(", "pub async fn main(", 1)
    else:
        body = driver.strip("\n").replace("fn main(", "pub fn main(", 1)
    return (
        "mod __cs_core_driver {\n"
        "    #[allow(unused_imports)]\n"
        "    use super::*;\n\n"
        f"{body}\n"
        "}\n\n"
        "fn main() {\n    __cs_core_driver::main();\n}\n"
    )


# Compiled and script modes (rust, c, js) are checked the same way: the source is put in
# the sandbox directory, a network-less container builds and runs the program, and output is compared line by line.
_EXIT_TAIL = (
    "timeout 10 {run} 2>/tmp/run_err; code=$?; "
    'if [ $code -ne 0 ]; then echo "__EXIT__$code"; head -c 1500 /tmp/run_err; fi'
)
_COMPILE_OR_FAIL = "{compile} 2>/tmp/err || {{ echo COMPILE_ERROR; cat /tmp/err; exit 0; }}; "


def _run_program(
    task: dict,
    *,
    prefix: str,
    filename: str,
    source: str,
    image: str,
    script: str,
    image_missing_hint: str | None = None,
) -> dict:
    """Runs script in a container with the sandbox directory /sandbox (filename lives there) and
    compares the program output with task["expected"]. A compile error, a non-zero exit code
    and a timeout are shown to the student as the check result."""
    with tempfile.TemporaryDirectory(prefix=prefix) as td:
        sandbox = Path(td)
        _open_dir(sandbox, {filename: source})
        pg = bool(task.get("postgres"))
        cmd = [
            "--network", "none",
            "--memory", RUST_MEMORY, "--memory-swap", RUST_MEMORY, "--cpus", RUST_CPUS, "--pids-limit", "256",
            "--read-only", "--tmpfs", "/tmp:rw,exec,size=256m",
            *HARDENING, *(PG_CAPS if pg else NOBODY),
            "-e", "HOME=/tmp",
            "-v", f"{sandbox}:/sandbox:ro", "-w", "/tmp",
            image, "sh", "-c", script,
        ]
        try:
            proc = _run_container(cmd, RUST_TIMEOUT_SEC)
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout", "results": [], "stdout": "",
                "stderr": f"Time limit exceeded ({RUST_TIMEOUT_SEC} s).",
            }
        except FileNotFoundError:
            return _docker_failed(
                "Docker is unavailable. Start Docker/OrbStack and try again."
            )
    out = proc.stdout
    if proc.returncode != 0 and not out:
        if image_missing_hint and image_missing_hint.split(":")[0] in proc.stderr:
            return _docker_failed(image_missing_hint, "error")
        return _docker_failed(proc.stderr.strip() or "Docker failed", "error")
    expected = task["expected"]
    if out.startswith("COMPILE_ERROR"):
        err = out[len("COMPILE_ERROR"):].strip()[:RUST_COMPILE_ERR_LIMIT]
        res = [{"ok": False, "got": "", "expected": "\n".join(expected), "error": "Compilation error:\n" + err}]
    elif "__EXIT__" in out:
        body, _, rest = out.partition("__EXIT__")
        code_, _, msg = rest.partition("\n")
        res = [{"ok": False, "got": body, "expected": "\n".join(expected),
                "error": f"The program exited with code {code_}.\n{msg.strip()}"}]
    else:
        got = [line.rstrip() for line in out.strip("\n").split("\n")] if out.strip() else []
        want = [line.rstrip() for line in expected]
        res = [{"ok": got == want, "got": "\n".join(got), "expected": "\n".join(want), "error": None}]
    return {"status": "ok", "results": res, "stdout": "", "stderr": ""}


def run_rust(task: dict, code: str) -> dict:
    """"rust" mode: student code + hidden driver (fn main) compiled by rustc."""
    if task.get("standalone"):
        # the student writes the whole program (own fn main); only the output is checked
        source = code.rstrip() + "\n"
    else:
        source = code.rstrip() + "\n\n" + wrap_rust_driver(task["driver"])
    crates = bool(task.get("crates"))
    externs = ""
    if crates:
        externs = "-L dependency=/opt/deps/target/release/deps $(cat /opt/ext/externs)"
    script = (PG_START if task.get("postgres") else "") + _COMPILE_OR_FAIL.format(
        compile=f"rustc --edition 2021 -O -C debuginfo=0 {externs} -o /tmp/prog /sandbox/main.rs"
    ) + _EXIT_TAIL.format(run="/tmp/prog")
    return _run_program(
        task,
        prefix="cs-core-rs-",
        filename="main.rs",
        source=source,
        image=RUST_CRATES_IMAGE if crates else RUST_IMAGE,
        script=script,
        image_missing_hint=(
            "cs-core-rust-crates:1 is not built. Run once: "
            "docker build -t cs-core-rust-crates:1 backend/docker/rust-crates"
            if crates
            else None
        ),
    )


def run_c(task: dict, code: str) -> dict:
    """"c" mode: student code + hidden driver (int main) built into one file by gcc."""
    source = code.rstrip() + "\n\n" + task["driver"].strip("\n") + "\n"
    flags = task.get("flags", C_DEFAULT_FLAGS)
    script = _COMPILE_OR_FAIL.format(
        compile=f"gcc {flags} -o /tmp/prog /sandbox/main.c -lm -lpthread"
    ) + _EXIT_TAIL.format(run="/tmp/prog")
    return _run_program(
        task, prefix="cs-core-c-", filename="main.c", source=source, image=C_IMAGE, script=script
    )


def run_js(task: dict, code: str) -> dict:
    """"js" mode: student code + hidden driver — one module (.mjs, Node 22)."""
    source = code.rstrip() + "\n\n" + task["driver"].strip("\n") + "\n"
    script = _EXIT_TAIL.format(run="node --max-old-space-size=256 /sandbox/main.mjs")
    return _run_program(
        task, prefix="cs-core-js-", filename="main.mjs", source=source, image=JS_IMAGE, script=script
    )


def run_task(task: dict, code: str) -> dict:
    """Returns {status, results, stdout, stderr}."""
    if task["mode"] == "rust":
        return run_rust(task, code)
    if task["mode"] == "c":
        return run_c(task, code)
    if task["mode"] == "js":
        return run_js(task, code)
    with tempfile.TemporaryDirectory(prefix="cs-core-ex-") as td:
        sandbox = Path(td)
        _open_dir(sandbox, {"solution.py": code, "harness.py": _harness(task)})
        cmd = [
            "--network",
            "none",
            *HARDENING,
            *NOBODY,
            "--memory-swap",
            MEMORY,
            "--memory",
            MEMORY,
            "--cpus",
            CPUS,
            "--pids-limit",
            PIDS_LIMIT,
            "--read-only",
            "--tmpfs",
            "/tmp:rw,size=32m",
            "-e",
            "PYTHONDONTWRITEBYTECODE=1",
            "-e",
            "HOME=/tmp",
            "-v",
            f"{sandbox}:/sandbox:ro",
            "-w",
            "/sandbox",
            IMAGE,
            "python3",
            "harness.py",
        ]
        try:
            proc = _run_container(cmd, TIMEOUT_SEC)
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "results": [],
                "stdout": "",
                "stderr": f"Time limit exceeded ({TIMEOUT_SEC} s). The code may contain an infinite loop.",
            }
        except FileNotFoundError:
            return {
                "status": "docker_error",
                "results": [],
                "stdout": "",
                "stderr": "Docker is unavailable. Start Docker/OrbStack and try again.",
            }

    if proc.returncode != 0:
        return {
            "status": "error",
            "results": [],
            "stdout": proc.stdout,
            "stderr": proc.stderr.strip()
            or f"Docker exited with code {proc.returncode}",
        }

    out_lines = []
    results = None
    for line in proc.stdout.splitlines():
        if line.startswith(MARK):
            try:
                results = json.loads(line[len(MARK) :])
            except json.JSONDecodeError:
                results = None
            break
        out_lines.append(line)

    if results is None:
        return {
            "status": "error",
            "results": [],
            "stdout": proc.stdout,
            "stderr": "The sandbox did not return a check result.",
        }
    return {
        "status": "ok",
        "results": results,
        "stdout": "\n".join(out_lines).rstrip("\n"),
        "stderr": proc.stderr.strip(),
    }
