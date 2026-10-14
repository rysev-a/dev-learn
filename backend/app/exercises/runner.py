"""Docker-песочница: запуск пользовательского кода с тестами.

Код ученика и сгенерированный harness пишутся во временную директорию,
она монтируется в контейнер read-only. Сеть выключена, лимиты по памяти,
CPU и числу процессов, общий таймаут. Итог harness печатает одной строкой
«RESULT_JSON:<json>» — по ней и разбираем результат.
"""

import json
import subprocess
import tempfile
import traceback
from pathlib import Path

IMAGE = "python:3.13-slim"
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
error = None
try:
    code = open("/sandbox/solution.py", encoding="utf-8").read()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "solution.py", "exec"), {{"__name__": "__main__"}})
except Exception:
    error = traceback.format_exc(limit=3).strip()

got = buf.getvalue()
expected = {expected!r}
def norm(s):
    lines = [line.rstrip() for line in s.strip("\\n").split("\\n")]
    return lines
ok = error is None and norm(got) == norm(expected)
result = [{{"ok": ok, "got": got, "expected": expected, "error": error}}]
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
    expected = "\n".join(task["expected"]) + "\n"
    return HARNESS_STDOUT.format(expected=expected)


def run_task(task: dict, code: str) -> dict:
    """Возвращает {status, results, stdout, stderr}."""
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
