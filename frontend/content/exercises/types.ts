/** Задача с вводом ответа: answers — принимаемые ответы (сравнение без учёта регистра и пробелов, числа — по значению) */
export interface PracticeTask {
  q: string;
  answers: string[];
  hint?: string;
}

export interface PracticeSet {
  kind: "practice";
  title: string;
  tasks: PracticeTask[];
}
