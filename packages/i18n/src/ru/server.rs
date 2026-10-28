//! Русские тексты сообщений сервера о проверке лабораторий (`backend/src/labs.rs`): английский ключ → перевод. Отсортировано по ключу.

pub static RU: &[(&str, &str)] = &[
    ("Exercise is damaged: {0}", "задание повреждено: {0}"),
    ("Goal not met: {0}", "цель не выполнена: {0}"),
    ("Scenario is damaged: {0}", "сценарий повреждён: {0}"),
    ("Solution could not be parsed: {0}", "решение не разобрано: {0}"),
    ("Solution not accepted", "решение не засчитано"),
];
