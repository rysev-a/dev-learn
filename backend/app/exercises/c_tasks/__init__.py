"""Код-задачи книги «От assembler к языку C» (book 16), ключ — номер главы.

Режим c: код ученика и скрытый драйвер (функция main) собираются в один файл
и компилируются gcc 14 в песочнице без сети (образ rust:1.97-slim: gcc, libc,
ASan/UBSan); сравнивается построчный вывод программы. Флаги по умолчанию —
`-std=gnu11 -O1 -Wall`, задача может задать свои через поле `flags`.
"""

from app.exercises.c_tasks import ch01_05, ch06, ch07, ch08, ch09, ch10, ch11, ch12, ch13, ch14

C_TASKS: dict[int, list[dict]] = {
    **ch01_05.TASKS,
    **ch06.TASKS,
    **ch07.TASKS,
    **ch08.TASKS,
    **ch09.TASKS,
    **ch10.TASKS,
    **ch11.TASKS,
    **ch12.TASKS,
    **ch13.TASKS,
    **ch14.TASKS,
}
