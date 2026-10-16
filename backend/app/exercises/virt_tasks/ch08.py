"""Задачи книги «Виртуализация»: глава 8 — KVM и QEMU: как ядро Linux становится гипервизором."""

TASKS: dict[int, list[dict]] = {
    8: [
        {
            "id": "virt-ioctl-order",
            "mode": "func",
            "func": "ioctl_order",
            "title": "Порядок вызовов к /dev/kvm",
            "statement": (
                "Напишите функцию ioctl_order(calls): calls — список вызовов QEMU к KVM по порядку: "
                '"CREATE_VM", "CREATE_VCPU", "SET_MEMORY" (область памяти гостя) и "RUN". Верните '
                'список из "ok" или "fail" для каждого вызова. CREATE_VM допустим один раз и первым. '
                "CREATE_VCPU и SET_MEMORY допустимы только после CREATE_VM. RUN допустим, если уже "
                "есть хотя бы один виртуальный процессор и хотя бы одна область памяти. Любой другой "
                "вызов, а также неизвестный — fail; неудачный вызов состояния не меняет."
            ),
            "starter": "def ioctl_order(calls):\n    pass\n",
            "tests": [
                {
                    "args": [["CREATE_VM", "CREATE_VCPU", "SET_MEMORY", "RUN"]],
                    "expected": ["ok", "ok", "ok", "ok"],
                },
                {"args": [["CREATE_VCPU"]], "expected": ["fail"]},
                {"args": [["CREATE_VM", "CREATE_VM"]], "expected": ["ok", "fail"]},
                {"args": [["CREATE_VM", "RUN"]], "expected": ["ok", "fail"]},
                {
                    "args": [["CREATE_VM", "SET_MEMORY", "RUN"]],
                    "expected": ["ok", "ok", "fail"],
                },
                {
                    "args": [
                        [
                            "CREATE_VM",
                            "CREATE_VCPU",
                            "CREATE_VCPU",
                            "SET_MEMORY",
                            "RUN",
                            "RUN",
                        ]
                    ],
                    "expected": ["ok", "ok", "ok", "ok", "ok", "ok"],
                },
                {"args": [[]], "expected": []},
                {"args": [["CREATE_VM", "BOOM"]], "expected": ["ok", "fail"]},
            ],
            "hint": (
                "Храните флаг созданной машины и счётчики vCPU и областей памяти."
            ),
        },
        {
            "id": "virt-vcpu-rr",
            "mode": "func",
            "func": "run_slices",
            "title": "Планировщик Linux и vCPU",
            "statement": (
                "Виртуальные процессоры планирует Linux как обычные потоки. Напишите функцию "
                "run_slices(threads, cores, slices): threads — список имён потоков в очереди, cores — "
                "число ядер, slices — число квантов времени. На каждом кванте первые cores потоков "
                "очереди (или все, если их меньше) получают по кванту и уходят в конец очереди в том "
                "же порядке. Верните словарь «имя → сколько квантов получил»."
            ),
            "starter": "def run_slices(threads, cores, slices):\n    pass\n",
            "tests": [
                {
                    "args": [["a", "b", "c", "d"], 2, 4],
                    "expected": {"a": 2, "b": 2, "c": 2, "d": 2},
                },
                {"args": [["a", "b", "c"], 2, 3], "expected": {"a": 2, "b": 2, "c": 2}},
                {"args": [["a"], 4, 5], "expected": {"a": 5}},
                {"args": [[], 2, 3], "expected": {}},
                {"args": [["a", "b"], 2, 3], "expected": {"a": 3, "b": 3}},
                {
                    "args": [["a", "b", "c", "d", "e"], 2, 5],
                    "expected": {"a": 2, "b": 2, "c": 2, "d": 2, "e": 2},
                },
                {"args": [["a", "b", "c"], 1, 6], "expected": {"a": 2, "b": 2, "c": 2}},
            ],
            "hint": (
                "Работайте со списком-очередью: срез в начале, затем добавление в конец."
            ),
        },
        {
            "id": "virt-exit-routing",
            "mode": "func",
            "func": "handle_exits",
            "title": "Куда уходят выходы",
            "statement": (
                "Напишите функцию handle_exits(exits, ioeventfd): exits — список выходов [причина, "
                "адрес], ioeventfd — список адресов с зарегистрированным ioeventfd. Ядро обрабатывает "
                "само причины EXTERNAL_INTERRUPT, HLT, CPUID, EPT_VIOLATION, MSR, а также MMIO по "
                "адресу из ioeventfd. Остальное уходит в QEMU. Верните кортеж (сколько обработало "
                "ядро, сколько ушло в QEMU, отсортированный список различных причин, ушедших в QEMU)."
            ),
            "starter": "def handle_exits(exits, ioeventfd):\n    pass\n",
            "tests": [
                {
                    "args": [[["HLT", 0], ["MMIO", 4096], ["IO", 96]], [4096]],
                    "expected": (2, 1, ["IO"]),
                },
                {
                    "args": [[["MMIO", 4096], ["MMIO", 8192]], [4096]],
                    "expected": (1, 1, ["MMIO"]),
                },
                {"args": [[], []], "expected": (0, 0, [])},
                {
                    "args": [[["CPUID", 0], ["MSR", 0], ["EPT_VIOLATION", 1]], []],
                    "expected": (3, 0, []),
                },
                {
                    "args": [[["IO", 1], ["IO", 2], ["SHUTDOWN", 0]], [1]],
                    "expected": (0, 3, ["IO", "SHUTDOWN"]),
                },
                {"args": [[["MMIO", 5]], [5]], "expected": (1, 0, [])},
            ],
            "hint": ("Для MMIO проверяйте адрес отдельно."),
        },
        {
            "id": "virt-qmp",
            "mode": "func",
            "func": "qmp_commands",
            "title": "Команды канала QMP",
            "statement": (
                "Напишите функцию qmp_commands(lines): lines — строки, каждая из которых должна быть "
                'JSON-объектом команды QMP вида {"execute": "имя", "arguments": {…}} (поле arguments '
                "может отсутствовать). Верните список кортежей (имя команды, число аргументов) для "
                "корректных команд по порядку. Строки, которые не разбираются как JSON, не являются "
                "объектом или не содержат строкового поля execute, пропускайте."
            ),
            "starter": "def qmp_commands(lines):\n    pass\n",
            "tests": [
                {
                    "args": [
                        [
                            '{"execute": "stop"}',
                            '{"execute": "blockdev-add", "arguments": {"node-name": "d0", "driver": "qcow2"}}',
                        ]
                    ],
                    "expected": [("stop", 0), ("blockdev-add", 2)],
                },
                {
                    "args": [
                        ["not json", '{"execute": 5}', "[]", '{"execute": "cont"}']
                    ],
                    "expected": [("cont", 0)],
                },
                {"args": [[]], "expected": []},
                {"args": [['{"arguments": {"a": 1}}']], "expected": []},
                {
                    "args": [
                        [
                            '{"execute": "migrate", "arguments": {"uri": "tcp:10.0.0.2:4444"}}',
                            '{"execute": "query-status"}',
                        ]
                    ],
                    "expected": [("migrate", 1), ("query-status", 0)],
                },
            ],
            "hint": ("Используйте json.loads и перехватывайте ошибку разбора."),
        },
        {
            "id": "virt-vm-xml",
            "mode": "func",
            "func": "vm_config",
            "title": "Описание машины в XML",
            "statement": (
                "Напишите функцию vm_config(xml): xml — упрощённое описание машины в стиле libvirt, "
                "например <domain><name>web</name><memory "
                'unit="GiB">2</memory><vcpu>4</vcpu><devices><disk/><disk/><interface/></devices></domain>. '
                'Верните словарь с ключами "name", "memory_mib" (память в МиБ: единицы KiB, MiB или '
                'GiB, по умолчанию KiB), "vcpus", "disks" (число элементов disk в devices) и "nics" '
                "(число элементов interface)."
            ),
            "starter": "def vm_config(xml):\n    pass\n",
            "tests": [
                {
                    "args": [
                        '<domain><name>web</name><memory unit="GiB">2</memory><vcpu>4</vcpu><devices><disk/><disk/><interface/></devices></domain>'
                    ],
                    "expected": {
                        "name": "web",
                        "memory_mib": 2048,
                        "vcpus": 4,
                        "disks": 2,
                        "nics": 1,
                    },
                },
                {
                    "args": [
                        '<domain><name>db</name><memory unit="MiB">512</memory><vcpu>1</vcpu><devices><disk/></devices></domain>'
                    ],
                    "expected": {
                        "name": "db",
                        "memory_mib": 512,
                        "vcpus": 1,
                        "disks": 1,
                        "nics": 0,
                    },
                },
                {
                    "args": [
                        "<domain><name>x</name><memory>1048576</memory><vcpu>2</vcpu><devices><interface/><interface/><disk/></devices></domain>"
                    ],
                    "expected": {
                        "name": "x",
                        "memory_mib": 1024,
                        "vcpus": 2,
                        "disks": 1,
                        "nics": 2,
                    },
                },
                {
                    "args": [
                        '<domain><name>empty</name><memory unit="KiB">4096</memory><vcpu>8</vcpu><devices/></domain>'
                    ],
                    "expected": {
                        "name": "empty",
                        "memory_mib": 4,
                        "vcpus": 8,
                        "disks": 0,
                        "nics": 0,
                    },
                },
            ],
            "hint": (
                "Используйте xml.etree.ElementTree; единицы переведите множителями."
            ),
        },
        {
            "id": "virt-qemu-cmd",
            "mode": "func",
            "func": "build_cmd",
            "title": "Командная строка QEMU",
            "statement": (
                'Напишите функцию build_cmd(cfg): cfg — словарь с полями "cpu" (строка), "smp" '
                '(число), "mem" (МиБ), "disks" (список [путь, формат]) и "nics" (число). Верните '
                'список аргументов: ["-machine", "q35,accel=kvm", "-cpu", cpu, "-smp", "<smp>", "-m", '
                '"<mem>M"], затем для каждого диска "-drive" и '
                '"file=<путь>,format=<формат>,cache=none", затем для каждой сетевой карты с номером i '
                'с нуля "-netdev" и "tap,id=n<i>,vhost=on" и "-device" и '
                '"virtio-net-pci,netdev=n<i>".'
            ),
            "starter": "def build_cmd(cfg):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {
                            "cpu": "host",
                            "smp": 4,
                            "mem": 8192,
                            "disks": [["a.qcow2", "qcow2"]],
                            "nics": 1,
                        }
                    ],
                    "expected": [
                        "-machine",
                        "q35,accel=kvm",
                        "-cpu",
                        "host",
                        "-smp",
                        "4",
                        "-m",
                        "8192M",
                        "-drive",
                        "file=a.qcow2,format=qcow2,cache=none",
                        "-netdev",
                        "tap,id=n0,vhost=on",
                        "-device",
                        "virtio-net-pci,netdev=n0",
                    ],
                },
                {
                    "args": [
                        {"cpu": "EPYC", "smp": 1, "mem": 512, "disks": [], "nics": 0}
                    ],
                    "expected": [
                        "-machine",
                        "q35,accel=kvm",
                        "-cpu",
                        "EPYC",
                        "-smp",
                        "1",
                        "-m",
                        "512M",
                    ],
                },
                {
                    "args": [
                        {
                            "cpu": "host",
                            "smp": 2,
                            "mem": 1024,
                            "disks": [["d0.raw", "raw"], ["d1.qcow2", "qcow2"]],
                            "nics": 2,
                        }
                    ],
                    "expected": [
                        "-machine",
                        "q35,accel=kvm",
                        "-cpu",
                        "host",
                        "-smp",
                        "2",
                        "-m",
                        "1024M",
                        "-drive",
                        "file=d0.raw,format=raw,cache=none",
                        "-drive",
                        "file=d1.qcow2,format=qcow2,cache=none",
                        "-netdev",
                        "tap,id=n0,vhost=on",
                        "-device",
                        "virtio-net-pci,netdev=n0",
                        "-netdev",
                        "tap,id=n1,vhost=on",
                        "-device",
                        "virtio-net-pci,netdev=n1",
                    ],
                },
            ],
            "hint": ("Собирайте список по частям в указанном порядке."),
        },
        {
            "id": "virt-sandbox",
            "mode": "func",
            "func": "check_sandbox",
            "title": "Проверка изоляции QEMU",
            "statement": (
                'Напишите функцию check_sandbox(cfg): cfg — словарь {"user": имя пользователя, '
                '"seccomp": bool, "selinux": bool, "apparmor": bool, "cgroup": bool}. Верните '
                'отсортированный список проблем: "root", если user равен "root"; "no-seccomp", если '
                'seccomp выключен; "no-mac", если выключены и selinux, и apparmor; "no-cgroup", если '
                "cgroup выключен. Если проблем нет — пустой список."
            ),
            "starter": "def check_sandbox(cfg):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {
                            "user": "qemu",
                            "seccomp": True,
                            "selinux": True,
                            "apparmor": False,
                            "cgroup": True,
                        }
                    ],
                    "expected": [],
                },
                {
                    "args": [
                        {
                            "user": "root",
                            "seccomp": False,
                            "selinux": False,
                            "apparmor": False,
                            "cgroup": False,
                        }
                    ],
                    "expected": ["no-cgroup", "no-mac", "no-seccomp", "root"],
                },
                {
                    "args": [
                        {
                            "user": "qemu",
                            "seccomp": True,
                            "selinux": False,
                            "apparmor": True,
                            "cgroup": False,
                        }
                    ],
                    "expected": ["no-cgroup"],
                },
                {
                    "args": [
                        {
                            "user": "root",
                            "seccomp": True,
                            "selinux": True,
                            "apparmor": True,
                            "cgroup": True,
                        }
                    ],
                    "expected": ["root"],
                },
                {
                    "args": [
                        {
                            "user": "nobody",
                            "seccomp": False,
                            "selinux": True,
                            "apparmor": False,
                            "cgroup": True,
                        }
                    ],
                    "expected": ["no-seccomp"],
                },
            ],
            "hint": ("Проверьте условия по очереди и отсортируйте результат."),
        },
        {
            "id": "virt-accel",
            "mode": "func",
            "func": "pick_accel",
            "title": "KVM или TCG",
            "statement": (
                "Напишите функцию pick_accel(host_arch, guest_arch, has_kvm): выберите ускоритель "
                "QEMU. Если архитектура гостя совпадает с архитектурой хоста и KVM доступен, верните "
                '"kvm" (команды гостя идут на процессор). Иначе верните "tcg" (программная трансляция '
                "каждой команды)."
            ),
            "starter": "def pick_accel(host_arch, guest_arch, has_kvm):\n    pass\n",
            "tests": [
                {"args": ["x86_64", "x86_64", True], "expected": "kvm"},
                {"args": ["x86_64", "x86_64", False], "expected": "tcg"},
                {"args": ["x86_64", "aarch64", True], "expected": "tcg"},
                {"args": ["aarch64", "aarch64", True], "expected": "kvm"},
                {"args": ["aarch64", "riscv64", False], "expected": "tcg"},
                {"args": ["riscv64", "riscv64", True], "expected": "kvm"},
            ],
            "hint": ("Два условия: одинаковая архитектура и наличие KVM."),
        },
    ],
}
