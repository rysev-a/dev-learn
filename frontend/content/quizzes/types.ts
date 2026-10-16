/** Вопрос квиза в исходнике: answer — номер верного варианта, expl — пояснение, которое видно после ответа */
export interface QuizQuestion {
  q: string;
  options: string[];
  answer: number;
  expl: string;
}

export interface Quiz {
  kind: "theory";
  title: string;
  questions: QuizQuestion[];
}
