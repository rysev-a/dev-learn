"""Задачи книги «Виртуализация»: глава 16 — Практика: QEMU/KVM своими руками и наблюдаемость."""

TASKS: dict[int, list[dict]] = {
    16: [
        {
            "id": "virt-kvm-stat-top",
            "mode": "func",
            "func": "kvm_stat_top",
            "title": "Лидеры kvm_stat",
            "statement": (
                "Напишите функцию kvm_stat_top(text, n): text — вывод kvm_stat в виде строк «имя "
                "счётчика, всего, в секунду», разделённых пробелами (например «kvm_exit  120000 "
                "3500»). Строки, где второе поле не целое число (заголовки, пустые), пропускайте. "
                "Верните список имён n счётчиков с наибольшим «всего»; при равенстве — по имени."
            ),
            "starter": "def kvm_stat_top(text, n):\n    pass\n",
            "tests": [
                {
                    "args": [
                        "kvm statistics\nevent total rate\nkvm_exit 120000 3500\nkvm_entry 119990 3499\nkvm_halt_exits 5000 100\n",
                        2,
                    ],
                    "expected": ["kvm_exit", "kvm_entry"],
                },
                {"args": ["", 3], "expected": []},
                {"args": ["a 10 1\nb 10 1\nc 5 1\n", 2], "expected": ["a", "b"]},
                {"args": ["x 1 0\n", 5], "expected": ["x"]},
                {
                    "args": ["Event Total Rate\nkvm_pio 700 5\nkvm_mmio 900 6\n", 1],
                    "expected": ["kvm_mmio"],
                },
            ],
            "hint": (
                "Разберите строку через split() и проверьте второе поле через isdigit()."
            ),
        },
        {
            "id": "virt-perf-report",
            "mode": "func",
            "func": "perf_report",
            "title": "Отчёт perf kvm stat",
            "statement": (
                "Напишите функцию perf_report(text): text — отчёт perf kvm stat report, где строки "
                "событий имеют вид «имя события, число выборок, доля выборок %, доля времени %, …» "
                "(поля разделены пробелами, проценты со знаком %). Остальные строки (заголовки, "
                "пустые) пропускайте. Верните список кортежей (имя события, доля времени числом с "
                "плавающей точкой), отсортированный по убыванию доли времени, а при равенстве — по "
                "имени."
            ),
            "starter": "def perf_report(text):\n    pass\n",
            "tests": [
                {
                    "args": [
                        "Event name Samples Samples% Time% Avg\nHLT 5231 40.1% 62.5% 180.4\nIO_INSTRUCTION 8021 61.5% 12.5% 23.9\nMSR_WRITE 1984 15.2% 4.0% 3.0\n"
                    ],
                    "expected": [
                        ("HLT", 62.5),
                        ("IO_INSTRUCTION", 12.5),
                        ("MSR_WRITE", 4.0),
                    ],
                },
                {"args": [""], "expected": []},
                {
                    "args": [
                        "EXTERNAL_INT 100 50.0% 8.3% 4.1\nHLT 100 50.0% 8.3% 100.0\n"
                    ],
                    "expected": [("EXTERNAL_INT", 8.3), ("HLT", 8.3)],
                },
                {"args": ["Total Samples: 5\n"], "expected": []},
                {
                    "args": ["EPT_VIOLATION 31 5.0% 2.2% 32.7\n"],
                    "expected": [("EPT_VIOLATION", 2.2)],
                },
            ],
            "hint": (
                "Событие — строка, где второе поле целое, а четвёртое оканчивается на «%»."
            ),
        },
        {
            "id": "virt-backing-chain",
            "mode": "func",
            "func": "backing_chain",
            "title": "Цепочка образов",
            "statement": (
                "Напишите функцию backing_chain(text): text — вывод qemu-img info --backing-chain: "
                "блоки, где есть строки «image: имя» и (не во всех) «backing file: имя (actual path: "
                "…)». Верните список имён образов в том порядке, в каком идут строки «image:» (сверху "
                "— текущий слой, снизу — базовый)."
            ),
            "starter": "def backing_chain(text):\n    pass\n",
            "tests": [
                {
                    "args": [
                        "image: l2.qcow2\nfile format: qcow2\nbacking file: l1.qcow2 (actual path: /v/l1.qcow2)\n\nimage: l1.qcow2\nfile format: qcow2\nbacking file: base.qcow2\n\nimage: base.qcow2\nfile format: qcow2\n"
                    ],
                    "expected": ["l2.qcow2", "l1.qcow2", "base.qcow2"],
                },
                {
                    "args": ["image: only.qcow2\nvirtual size: 20 GiB\n"],
                    "expected": ["only.qcow2"],
                },
                {"args": [""], "expected": []},
                {"args": ["file format: qcow2\nbacking file: x\n"], "expected": []},
                {"args": ["image: /a/b c.qcow2\n"], "expected": ["/a/b c.qcow2"]},
            ],
            "hint": ("Ищите строки, которые начинаются с «image:»."),
        },
        {
            "id": "virt-psi",
            "mode": "func",
            "func": "psi_status",
            "title": "Давление на ресурсы (PSI)",
            "statement": (
                "Напишите функцию psi_status(text, warn, crit): text — содержимое файла из "
                "/proc/pressure/ вида «some avg10=1.50 avg60=0.80 avg300=0.20 total=12345» и (не "
                "всегда) строка «full …». warn и crit — пороги для avg10 в процентах. Возьмите "
                'наибольшее значение avg10 среди всех строк и верните "crit", если оно не меньше '
                'crit; иначе "warn", если не меньше warn; иначе "ok". Пустой текст — "ok".'
            ),
            "starter": "def psi_status(text, warn, crit):\n    pass\n",
            "tests": [
                {
                    "args": [
                        "some avg10=1.50 avg60=0.80 avg300=0.20 total=12345\nfull avg10=0.20 avg60=0.10 avg300=0.00 total=99\n",
                        5,
                        20,
                    ],
                    "expected": "ok",
                },
                {
                    "args": ["some avg10=7.00 avg60=3 avg300=1 total=1\n", 5, 20],
                    "expected": "warn",
                },
                {
                    "args": ["some avg10=0.00 avg60=0.00 avg300=0.00 total=0\n", 5, 20],
                    "expected": "ok",
                },
                {
                    "args": [
                        "some avg10=2 avg60=1 avg300=1 total=1\nfull avg10=25.5 avg60=1 avg300=1 total=1\n",
                        5,
                        20,
                    ],
                    "expected": "crit",
                },
                {"args": ["", 5, 20], "expected": "ok"},
                {
                    "args": ["some avg10=5.00 avg60=0 avg300=0 total=0\n", 5, 20],
                    "expected": "warn",
                },
            ],
            "hint": ("Значение avg10 — число после «avg10=» в строке."),
        },
        {
            "id": "virt-domstats",
            "mode": "func",
            "func": "parse_domstats",
            "title": "Разбор virsh domstats",
            "statement": (
                "Напишите функцию parse_domstats(text): text — вывод virsh domstats для одной машины: "
                "строка «Domain: 'имя'» и строки вида «ключ=значение». Верните словарь «ключ → целое "
                "число» только для тех строк, где значение — целое число (отрицательные не бывают); "
                "остальные строки и пары пропускайте."
            ),
            "starter": "def parse_domstats(text):\n    pass\n",
            "tests": [
                {
                    "args": [
                        "Domain: 'web'\n  state.state=1\n  balloon.current=2097152\n  vcpu.current=4\n  net.0.name=vnet0\n"
                    ],
                    "expected": {
                        "state.state": 1,
                        "balloon.current": 2097152,
                        "vcpu.current": 4,
                    },
                },
                {"args": [""], "expected": {}},
                {"args": ["Domain: 'x'\n  a=1\n  b=\n  c=x=1\n"], "expected": {"a": 1}},
                {
                    "args": ["  cpu.time=123456789\n  vcpu.0.state=1\n"],
                    "expected": {"cpu.time": 123456789, "vcpu.0.state": 1},
                },
                {"args": ["no equals here\n  k=007\n"], "expected": {"k": 7}},
            ],
            "hint": (
                "Делите строки по первому знаку «=» и проверяйте значение через isdigit()."
            ),
        },
        {
            "id": "virt-first-check",
            "mode": "func",
            "func": "first_check",
            "title": "С чего начать диагностику",
            "statement": (
                "Напишите функцию first_check(symptom, facts): symptom — жалоба, facts — словарь "
                'логических фактов о машине ("virtio", "vhost", "multiqueue", "cache_none", "pinned", '
                '"kvm_access"). Верните код первой проверки. slow-net: нет virtio — "use-virtio"; '
                'иначе нет vhost — "enable-vhost"; иначе нет multiqueue — "enable-multiqueue"; иначе '
                '"profile-exits". slow-disk: нет virtio — "use-virtio"; иначе нет cache_none — '
                '"cache-none"; иначе "check-iothread". high-steal: нет pinned — "pin-vcpus"; иначе '
                '"reduce-overcommit". no-start: нет kvm_access — "fix-dev-kvm"; иначе '
                '"check-nested-and-cpu-model". Другая жалоба — "unknown".'
            ),
            "starter": "def first_check(symptom, facts):\n    pass\n",
            "tests": [
                {
                    "args": [
                        "slow-net",
                        {
                            "virtio": False,
                            "vhost": False,
                            "multiqueue": False,
                            "cache_none": False,
                            "pinned": False,
                            "kvm_access": True,
                        },
                    ],
                    "expected": "use-virtio",
                },
                {
                    "args": [
                        "slow-net",
                        {
                            "virtio": True,
                            "vhost": False,
                            "multiqueue": False,
                            "cache_none": False,
                            "pinned": False,
                            "kvm_access": True,
                        },
                    ],
                    "expected": "enable-vhost",
                },
                {
                    "args": [
                        "slow-net",
                        {
                            "virtio": True,
                            "vhost": True,
                            "multiqueue": True,
                            "cache_none": False,
                            "pinned": False,
                            "kvm_access": True,
                        },
                    ],
                    "expected": "profile-exits",
                },
                {
                    "args": [
                        "slow-disk",
                        {
                            "virtio": True,
                            "vhost": True,
                            "multiqueue": True,
                            "cache_none": False,
                            "pinned": False,
                            "kvm_access": True,
                        },
                    ],
                    "expected": "cache-none",
                },
                {
                    "args": [
                        "slow-disk",
                        {
                            "virtio": True,
                            "vhost": True,
                            "multiqueue": True,
                            "cache_none": True,
                            "pinned": False,
                            "kvm_access": True,
                        },
                    ],
                    "expected": "check-iothread",
                },
                {
                    "args": [
                        "high-steal",
                        {
                            "virtio": True,
                            "vhost": True,
                            "multiqueue": True,
                            "cache_none": True,
                            "pinned": True,
                            "kvm_access": True,
                        },
                    ],
                    "expected": "reduce-overcommit",
                },
                {
                    "args": [
                        "no-start",
                        {
                            "virtio": True,
                            "vhost": True,
                            "multiqueue": True,
                            "cache_none": True,
                            "pinned": True,
                            "kvm_access": False,
                        },
                    ],
                    "expected": "fix-dev-kvm",
                },
                {
                    "args": [
                        "boom",
                        {
                            "virtio": True,
                            "vhost": True,
                            "multiqueue": True,
                            "cache_none": True,
                            "pinned": True,
                            "kvm_access": True,
                        },
                    ],
                    "expected": "unknown",
                },
            ],
            "hint": (
                "Разберите каждую жалобу отдельной веткой и проверяйте факты по порядку."
            ),
        },
        {
            "id": "virt-virt-flags",
            "mode": "func",
            "func": "virt_flags",
            "title": "Признаки виртуализации в cpuinfo",
            "statement": (
                "Напишите функцию virt_flags(cpuinfo): cpuinfo — текст /proc/cpuinfo; в нём может "
                "быть несколько ядер, у каждого строка «flags : …». Из признаков найдите известные "
                "признаки виртуализации: vmx, ept, vpid (Intel) и svm, npt (AMD). Признак hypervisor "
                "означает, что вы внутри гостя. Верните кортеж (отсортированный список найденных "
                "признаков виртуализации без повторов, находимся ли мы в госте)."
            ),
            "starter": "def virt_flags(cpuinfo):\n    pass\n",
            "tests": [
                {
                    "args": [
                        "processor : 0\nflags : fpu vme vmx ept vpid\n\nprocessor : 1\nflags : fpu vme vmx ept vpid\n"
                    ],
                    "expected": (["ept", "vmx", "vpid"], False),
                },
                {
                    "args": ["flags : fpu svm npt hypervisor\n"],
                    "expected": (["npt", "svm"], True),
                },
                {"args": ["flags : fpu sse2\n"], "expected": ([], False)},
                {"args": [""], "expected": ([], False)},
                {
                    "args": ["flags : vmx hypervisor\nmodel name : x\n"],
                    "expected": (["vmx"], True),
                },
            ],
            "hint": (
                "Соберите все признаки из строк, начинающихся с flags, во множество."
            ),
        },
        {
            "id": "virt-user-data",
            "mode": "func",
            "func": "render_user_data",
            "title": "Файл начальной настройки cloud-init",
            "statement": (
                "Напишите функцию render_user_data(hostname, users, packages): hostname — имя машины, "
                "users — список [имя пользователя, публичный ключ], packages — список пакетов. "
                "Верните текст формата cloud-config со строками (перевод строки в конце): "
                "«#cloud-config», «hostname: <имя>», «users:», для каждого пользователя «  - name: "
                "<имя>», «    ssh_authorized_keys:», «      - <ключ>». Если пакеты есть, добавьте "
                "«packages:» и для каждого «  - <пакет>». Если пользователей нет, раздел users не "
                "выводите."
            ),
            "starter": "def render_user_data(hostname, users, packages):\n    pass\n",
            "tests": [
                {
                    "args": [
                        "web",
                        [["alice", "ssh-ed25519 AAAA"]],
                        ["qemu-guest-agent"],
                    ],
                    "expected": "#cloud-config\nhostname: web\nusers:\n  - name: alice\n    ssh_authorized_keys:\n      - ssh-ed25519 AAAA\npackages:\n  - qemu-guest-agent\n",
                },
                {"args": ["db", [], []], "expected": "#cloud-config\nhostname: db\n"},
                {
                    "args": ["x", [["a", "k1"], ["b", "k2"]], []],
                    "expected": "#cloud-config\nhostname: x\nusers:\n  - name: a\n    ssh_authorized_keys:\n      - k1\n  - name: b\n    ssh_authorized_keys:\n      - k2\n",
                },
                {
                    "args": ["y", [], ["htop", "curl"]],
                    "expected": "#cloud-config\nhostname: y\npackages:\n  - htop\n  - curl\n",
                },
                {
                    "args": ["z", [["root", "ssh-rsa BBBB"]], ["a", "b", "c"]],
                    "expected": "#cloud-config\nhostname: z\nusers:\n  - name: root\n    ssh_authorized_keys:\n      - ssh-rsa BBBB\npackages:\n  - a\n  - b\n  - c\n",
                },
            ],
            "hint": ("Собирайте список строк и соединяйте их через перевод строки."),
        },
    ],
}
