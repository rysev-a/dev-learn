"""Docker-песочница: запуск пользовательского кода с тестами.

Режимы: func (вызов функции с аргументами), stdout (сравнение вывода) и
stdout с необязательным скрытым "driver" — код, который выполняется после
решения ученика в том же пространстве имён (для классов, файлов, генераторов).

Код ученика и сгенерированный harness пишутся во временную директорию,
она монтируется в контейнер read-only. Сеть выключена, лимиты по памяти,
CPU и числу процессов, общий таймаут. Итог harness печатает одной строкой
«RESULT_JSON:<json>» — по ней и разбираем результат.
"""

import json
import subprocess
import tempfile
from pathlib import Path

IMAGE = "python:3.13-slim"
RUST_IMAGE = "rust:1.97-slim"
RUST_TIMEOUT_SEC = 60
RUST_MEMORY = "1g"
RUST_CPUS = "2.0"
RUST_COMPILE_ERR_LIMIT = 3000
C_IMAGE = RUST_IMAGE  # в образе rust:slim есть gcc 14, libc и санитайзеры
C_DEFAULT_FLAGS = "-std=gnu11 -O1 -g0 -Wall"
TIMEOUT_SEC = 25
MEMORY = "256m"
CPUS = "1.0"
PIDS_LIMIT = "64"

MARK = "RESULT_JSON:"

# Harness для режима «функция»: импортирует solution.py, вызывает функцию
# с аргументами из тестов и сравнивает возвращённое значение с ожидаемым.
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
        {{"ok": False, "error": "Код падает при запуске:\n" + load_error}}
    ] * {n}
else:
    fn = getattr(mod, {func!r}, None)
    if fn is None:
        results = [
            {{"ok": False, "error": "Функция {func} не найдена. Проверьте имя и регистр."}}
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

# Harness для режима «вывод»: запускает solution.py как программу,
# перехватывает stdout и сравнивает построчно (пробелы в концах строк
# не учитываются).
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
        # режим «драйвер»: код ученика только описывает классы/функции, а
        # скрытый драйвер печатает то, что сравнивается с ожидаемым
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


# Harness для режима «sql»: запрос ученика выполняется в SQLite на подготовленной
# базе (setup). Сравнивается результат последнего SELECT ученика либо контрольного
# запроса check (если задан) — как множество строк или по порядку (ordered).
# contains — подстроки, которые должны встретиться в результате (для планов запросов),
# forbid — подстроки, которых быть не должно.
HARNESS_SQL = r"""\
import json
import sqlite3

def cell(v):
    return round(v, 4) if isinstance(v, float) else v

def fmt(rows):
    return "\\n".join(" | ".join("NULL" if v is None else str(v) for v in r) for r in rows)

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
try:
    con = sqlite3.connect(":memory:", isolation_level=None)
    con.executescript(SETUP)
    code = open("/sandbox/solution.py", encoding="utf-8").read()
    last = None
    for st in statements(code):
        cur = con.execute(st)
        if cur.description is not None:
            last = [tuple(cell(v) for v in r) for r in cur.fetchall()]
    if CHECK:
        got = [tuple(cell(v) for v in r) for r in con.execute(CHECK).fetchall()]
    elif last is None:
        raise ValueError("Запрос ничего не вернул: нужен SELECT")
    else:
        got = last
except Exception as e:
    error = type(e).__name__ + ": " + str(e)

exp = [tuple(cell(v) for v in r) for r in EXPECTED]
if CONTAINS:
    text = fmt(got)
    ok = error is None and all(c in text for c in CONTAINS) and not any(f in text for f in FORBID)
    shown_expected = "в результате должно встретиться: " + ", ".join(CONTAINS)
    if FORBID:
        shown_expected += "; не должно быть: " + ", ".join(FORBID)
else:
    if ORDERED:
        ok = error is None and got == exp
    else:
        ok = error is None and sorted(got, key=repr) == sorted(exp, key=repr)
    shown_expected = fmt(exp)
result = [{"ok": ok, "got": fmt(got), "expected": shown_expected, "error": error}]
print("RESULT_JSON:" + json.dumps(result, ensure_ascii=False))
"""


def _enc(x):
    """Кортежи в тестах (аргументы и ожидаемое) едут через JSON с меткой —
    harness вернёт их кортежами, поэтому [1, 2] и (1, 2) различаются."""
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
    """Драйвер кладётся в собственный модуль: его `use` не конфликтуют с
    импортами ученика (явные импорты модуля важнее глобального `use super::*`),
    а имена из решения ученика доступны через `super`."""
    body = driver.strip("\n").replace("fn main(", "pub fn main(", 1)
    return (
        "mod __say_driver {\n"
        "    #[allow(unused_imports)]\n"
        "    use super::*;\n\n"
        f"{body}\n"
        "}\n\n"
        "fn main() {\n    __say_driver::main();\n}\n"
    )


def run_rust(task: dict, code: str) -> dict:
    """Режим «rust»: код ученика + скрытый драйвер (fn main) компилируются
    rustc в песочнице без сети; сравнивается построчный вывод программы.
    Ошибка компиляции показывается ученику как результат проверки."""
    source = code.rstrip() + "\n\n" + wrap_rust_driver(task["driver"])
    script = (
        "rustc --edition 2021 -O -C debuginfo=0 -o /tmp/prog /sandbox/main.rs 2>/tmp/err "
        "|| { echo COMPILE_ERROR; cat /tmp/err; exit 0; }; "
        "timeout 10 /tmp/prog 2>/tmp/run_err; code=$?; "
        'if [ $code -ne 0 ]; then echo "__EXIT__$code"; head -c 1500 /tmp/run_err; fi'
    )
    with tempfile.TemporaryDirectory(prefix="say-rs-") as td:
        sandbox = Path(td)
        (sandbox / "main.rs").write_text(source, encoding="utf-8")
        cmd = [
            "docker", "run", "--rm", "--network", "none",
            "--memory", RUST_MEMORY, "--cpus", RUST_CPUS, "--pids-limit", "256",
            "--read-only", "--tmpfs", "/tmp:rw,exec,size=256m",
            "-e", "HOME=/tmp",
            "-v", f"{sandbox}:/sandbox:ro", "-w", "/tmp",
            RUST_IMAGE, "sh", "-c", script,
        ]
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, errors="replace", timeout=RUST_TIMEOUT_SEC
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout", "results": [], "stdout": "",
                "stderr": f"Превышен лимит времени ({RUST_TIMEOUT_SEC} с).",
            }
        except FileNotFoundError:
            return _docker_failed(
                "Docker недоступен. Запустите Docker/OrbStack и попробуйте снова."
            )
    out = proc.stdout
    if proc.returncode != 0 and not out:
        return _docker_failed(proc.stderr.strip() or "Docker завершился с ошибкой", "error")
    expected = task["expected"]
    if out.startswith("COMPILE_ERROR"):
        err = out[len("COMPILE_ERROR"):].strip()[:RUST_COMPILE_ERR_LIMIT]
        res = [{"ok": False, "got": "", "expected": "\n".join(expected), "error": "Ошибка компиляции:\n" + err}]
    elif "__EXIT__" in out:
        body, _, rest = out.partition("__EXIT__")
        code_, _, msg = rest.partition("\n")
        res = [{"ok": False, "got": body, "expected": "\n".join(expected),
                "error": f"Программа завершилась с кодом {code_}.\n{msg.strip()}"}]
    else:
        got = [line.rstrip() for line in out.strip("\n").split("\n")] if out.strip() else []
        want = [line.rstrip() for line in expected]
        res = [{"ok": got == want, "got": "\n".join(got), "expected": "\n".join(want), "error": None}]
    return {"status": "ok", "results": res, "stdout": "", "stderr": ""}


def run_c(task: dict, code: str) -> dict:
    """Режим «c»: код ученика + скрытый драйвер (int main) собираются в один файл
    и компилируются gcc в песочнице без сети; сравнивается построчный вывод программы.
    Ошибка компиляции показывается ученику как результат проверки."""
    source = code.rstrip() + "\n\n" + task["driver"].strip("\n") + "\n"
    flags = task.get("flags", C_DEFAULT_FLAGS)
    script = (
        f"gcc {flags} -o /tmp/prog /sandbox/main.c -lm -lpthread 2>/tmp/err "
        "|| { echo COMPILE_ERROR; cat /tmp/err; exit 0; }; "
        "timeout 10 /tmp/prog 2>/tmp/run_err; code=$?; "
        'if [ $code -ne 0 ]; then echo "__EXIT__$code"; head -c 1500 /tmp/run_err; fi'
    )
    with tempfile.TemporaryDirectory(prefix="say-c-") as td:
        sandbox = Path(td)
        (sandbox / "main.c").write_text(source, encoding="utf-8")
        cmd = [
            "docker", "run", "--rm", "--network", "none",
            "--memory", RUST_MEMORY, "--cpus", RUST_CPUS, "--pids-limit", "256",
            "--read-only", "--tmpfs", "/tmp:rw,exec,size=256m",
            "-e", "HOME=/tmp",
            "-v", f"{sandbox}:/sandbox:ro", "-w", "/tmp",
            C_IMAGE, "sh", "-c", script,
        ]
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, errors="replace", timeout=RUST_TIMEOUT_SEC
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout", "results": [], "stdout": "",
                "stderr": f"Превышен лимит времени ({RUST_TIMEOUT_SEC} с).",
            }
        except FileNotFoundError:
            return _docker_failed(
                "Docker недоступен. Запустите Docker/OrbStack и попробуйте снова."
            )
    out = proc.stdout
    if proc.returncode != 0 and not out:
        return _docker_failed(proc.stderr.strip() or "Docker завершился с ошибкой", "error")
    expected = task["expected"]
    if out.startswith("COMPILE_ERROR"):
        err = out[len("COMPILE_ERROR"):].strip()[:RUST_COMPILE_ERR_LIMIT]
        res = [{"ok": False, "got": "", "expected": "\n".join(expected), "error": "Ошибка компиляции:\n" + err}]
    elif "__EXIT__" in out:
        body, _, rest = out.partition("__EXIT__")
        code_, _, msg = rest.partition("\n")
        res = [{"ok": False, "got": body, "expected": "\n".join(expected),
                "error": f"Программа завершилась с кодом {code_}.\n{msg.strip()}"}]
    else:
        got = [line.rstrip() for line in out.strip("\n").split("\n")] if out.strip() else []
        want = [line.rstrip() for line in expected]
        res = [{"ok": got == want, "got": "\n".join(got), "expected": "\n".join(want), "error": None}]
    return {"status": "ok", "results": res, "stdout": "", "stderr": ""}


def run_task(task: dict, code: str) -> dict:
    """Возвращает {status, results, stdout, stderr}."""
    if task["mode"] == "rust":
        return run_rust(task, code)
    if task["mode"] == "c":
        return run_c(task, code)
    with tempfile.TemporaryDirectory(prefix="say-ex-") as td:
        sandbox = Path(td)
        (sandbox / "solution.py").write_text(code, encoding="utf-8")
        (sandbox / "harness.py").write_text(_harness(task), encoding="utf-8")
        cmd = [
            "docker",
            "run",
            "--rm",
            "--network",
            "none",
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
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=TIMEOUT_SEC
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "results": [],
                "stdout": "",
                "stderr": f"Превышен лимит времени ({TIMEOUT_SEC} с). Возможно, бесконечный цикл.",
            }
        except FileNotFoundError:
            return {
                "status": "docker_error",
                "results": [],
                "stdout": "",
                "stderr": "Docker недоступен. Запустите Docker/OrbStack и попробуйте снова.",
            }

    if proc.returncode != 0:
        return {
            "status": "error",
            "results": [],
            "stdout": proc.stdout,
            "stderr": proc.stderr.strip()
            or f"Docker завершился с кодом {proc.returncode}",
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
            "stderr": "Песочница не вернула результат проверки.",
        }
    return {
        "status": "ok",
        "results": results,
        "stdout": "\n".join(out_lines).rstrip("\n"),
        "stderr": proc.stderr.strip(),
    }
