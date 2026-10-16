"""Код-задачи книги «Виртуализация» (book 17), ключ — номер главы.

Идеи виртуализации моделируются на Python: условия Попека и Голдберга, ловушки и
виртуальные регистры, двоичная трансляция, гипервызовы, VMCS и жизненный цикл VMX,
уровни исключений ARM и режимы RISC-V; обход таблиц страниц, EPT и TLB, баллонинг и KSM,
очереди virtio, IOMMU, VFIO и SR-IOV; вызовы KVM, образы qcow2 и слои, живая миграция, NUMA и
планирование vCPU; контейнеры и cgroups, microVM и облако, побочные каналы, RMP и аттестация;
вложенная виртуализация и разбор вывода инструментов QEMU/KVM.
Проверка — режим func: возвращаемое значение.
"""

from app.exercises.virt_tasks.labs import LAB_TASKS
from app.exercises.virt_tasks import (
    ch01,
    ch02,
    ch03,
    ch04,
    ch05,
    ch06,
    ch07,
    ch08,
    ch09,
    ch10,
    ch11,
    ch12,
    ch13,
    ch14,
    ch15,
    ch16,
)

VIRT_TASKS: dict[int, list[dict]] = {
    **ch01.TASKS,
    **ch02.TASKS,
    **ch03.TASKS,
    **ch04.TASKS,
    **ch05.TASKS,
    **ch06.TASKS,
    **ch07.TASKS,
    **ch08.TASKS,
    **ch09.TASKS,
    **ch10.TASKS,
    **ch11.TASKS,
    **ch12.TASKS,
    **ch13.TASKS,
    **ch14.TASKS,
    **ch15.TASKS,
    **ch16.TASKS,
}

# интерактивные упражнения (симуляторы) идут первыми в списке своей главы
for _ch, _labs in LAB_TASKS.items():
    VIRT_TASKS[_ch] = _labs + VIRT_TASKS.get(_ch, [])
