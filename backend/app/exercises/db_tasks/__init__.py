"""Код-задачи книги «Базы данных» (book 9), ключ — номер главы.

Два вида заданий: режим sql — запрос ученика выполняется в SQLite на готовой
базе (план запроса, индексы и состояние таблиц проверяются контрольным запросом),
и Python-симуляции того, что внутри баз: журнал и LSM, репликация, шардирование,
кэш. Остальные режимы — как в других книгах.
"""

from app.exercises.db_tasks import ch01, ch02, ch03, ch04, ch05, ch06, ch07, ch08, ch09, ch10, ch11, ch12, ch13, ch14, ch15, ch16, ch17, ch18, ch19, ch20, ch21, ch22, ch23, ch24, ch25, ch26, ch27, ch28, ch29, ch30, ch31, ch32

DB_TASKS: dict[int, list[dict]] = {
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
    **ch17.TASKS,
    **ch18.TASKS,
    **ch19.TASKS,
    **ch20.TASKS,
    **ch21.TASKS,
    **ch22.TASKS,
    **ch23.TASKS,
    **ch24.TASKS,
    **ch25.TASKS,
    **ch26.TASKS,
    **ch27.TASKS,
    **ch28.TASKS,
    **ch29.TASKS,
    **ch30.TASKS,
    **ch31.TASKS,
    **ch32.TASKS,
}
