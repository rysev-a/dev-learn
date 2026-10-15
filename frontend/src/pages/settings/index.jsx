import { useState } from "react";
import {
  KEYS,
  clearPractice,
  readSetting,
  writeSetting,
} from "../../lib/settings.js";

// Страница настроек: всё хранится в этом браузере и применяется сразу.
export default function SettingsPage({ theme, setTheme }) {
  const [aside, setAside] = useState(() => readSetting(KEYS.aside) === "1");
  const [anim, setAnim] = useState(() => readSetting(KEYS.anim) !== "0");
  const [cleared, setCleared] = useState(null);

  function toggleAside() {
    writeSetting(KEYS.aside, aside ? "0" : "1");
    setAside(!aside);
  }

  function toggleAnim() {
    writeSetting(KEYS.anim, anim ? "0" : null);
    setAnim(!anim);
  }

  function reset() {
    if (
      window.confirm(
        "Удалить решения, статусы и черновики кода во всех упражнениях?",
      )
    )
      setCleared(clearPractice());
  }

  return (
    <main className="set-page">
      <section className="set-card">
        <h2>Настройки</h2>
        <p className="set-sub">
          Хранятся в этом браузере и применяются сразу. К прогрессу курса не
          относятся.
        </p>

        <h3 className="set-group">Внешний вид</h3>
        <Row
          title="Светлая тема"
          text="Переключает тёмную и светлую палитру интерфейса и слайдов."
          on={theme === "light"}
          onChange={() => setTheme(theme === "dark" ? "light" : "dark")}
        />
        <Row
          title="Свёрнутое меню книг"
          text="Вместо названий в левом меню — колонка иконок. Можно переключать и кнопкой над меню."
          on={aside}
          onChange={toggleAside}
        />

        <h3 className="set-group">Слайды</h3>
        <Row
          title="Автопроигрывание анимаций"
          text="Схемы на слайдах сами проходят шаги по таймеру, когда озвучка выключена. Если отключить, схема сразу показывает итог, а шаги переключаются вручную."
          on={anim}
          onChange={toggleAnim}
        />

        <h3 className="set-group">Практика</h3>
        <div className="set-row">
          <div className="set-row-text">
            <span className="set-row-title">Сбросить прогресс упражнений</span>
            <span className="set-row-desc">
              Удаляет решённые задачи, статусы и черновики кода из этого
              браузера. Вопросы и слайды не затрагиваются.
              {cleared != null && (
                <b className="set-done"> Удалено записей: {cleared}.</b>
              )}
            </span>
          </div>
          <button className="quiz-btn ghost" onClick={reset}>
            Сбросить
          </button>
        </div>
      </section>
    </main>
  );
}

function Row({ title, text, on, onChange }) {
  return (
    <div className="set-row">
      <div className="set-row-text">
        <span className="set-row-title">{title}</span>
        <span className="set-row-desc">{text}</span>
      </div>
      <button
        type="button"
        role="switch"
        aria-checked={on}
        aria-label={title}
        className={`set-switch ${on ? "on" : ""}`}
        onClick={onChange}
      >
        <i />
      </button>
    </div>
  );
}
