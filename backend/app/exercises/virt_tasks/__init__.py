"""Код-задачи книги «Виртуализация» (book 17), ключ — номер главы.

Идеи виртуализации моделируются на Python: условия Попека и Голдберга, ловушки и
виртуальные регистры, двоичная трансляция, гипервызовы, VMCS и жизненный цикл VMX,
уровни исключений ARM и режимы RISC-V; обход таблиц страниц, EPT и TLB, баллонинг и KSM,
очереди virtio, IOMMU, VFIO и SR-IOV. Проверка — режим func: возвращаемое значение.
"""

from app.exercises.virt_tasks import ch01, ch02, ch03, ch04, ch05, ch06, ch07

VIRT_TASKS: dict[int, list[dict]] = {
    **ch01.TASKS,
    **ch02.TASKS,
    **ch03.TASKS,
    **ch04.TASKS,
    **ch05.TASKS,
    **ch06.TASKS,
    **ch07.TASKS,
}
