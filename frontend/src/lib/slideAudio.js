// Время озвучки показанного слайда: секунды от начала его абзаца, пока этот
// слайд играет (в том числе на паузе), иначе null. Анимации читают его, чтобы
// двигаться синхронно с голосом; без звука они идут по собственным таймерам.
import { createContext, useContext } from "react";

export const SlideAudioContext = createContext(null);

export function useSlideAudioTime() {
  return useContext(SlideAudioContext);
}
