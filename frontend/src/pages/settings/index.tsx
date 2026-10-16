import { useState } from "react";
import { useAuth } from "../../lib/auth.tsx";
import { useProgress, type ResetScope } from "../../lib/progress.tsx";
import { KEYS, readSetting, writeSetting, type Theme } from "../../lib/settings.ts";

// Страница настроек: внешний вид хранится в браузере, прогресс и аккаунт — в кабинете.
export default function SettingsPage({ theme, setTheme }: { theme: Theme; setTheme: (t: Theme) => void }) {
  const { user, logout } = useAuth();
  const progress = useProgress();
  const [aside, setAside] = useState(() => readSetting(KEYS.aside) === "1");
  const [anim, setAnim] = useState(() => readSetting(KEYS.anim) !== "0");
  const [done, setDone] = useState<ResetScope | null>(null); // какой сброс только что выполнен

  function toggleAside() {
    writeSetting(KEYS.aside, aside ? "0" : "1");
    setAside(!aside);
  }

  function toggleAnim() {
    writeSetting(KEYS.anim, anim ? "0" : null);
    setAnim(!anim);
  }

  async function reset(scope: ResetScope, question: string) {
    if (!window.confirm(question)) return;
    await progress.reset(scope);
    (await import("../../lab/hydrate.ts")).forgetLab(user?.id ?? 0); // слепок решений лаборатории
    setDone(scope);
  }

  return (
    <main className="set-page">
      <section className="set-card">
        <h2>Настройки</h2>
        <p className="set-sub">
          Внешний вид хранится в этом браузере и применяется сразу; прогресс — в
          вашем кабинете на сервере.
        </p>

        <h3 className="set-group">Аккаунт</h3>
        <div className="set-row">
          <div className="set-row-text">
            <span className="set-row-title">{user?.login}</span>
            <span className="set-row-desc">
              {user?.email}. Прогресс, ответы и история попыток хранятся в
              кабинете и доступны с любого браузера.
            </span>
          </div>
          <button className="quiz-btn ghost" onClick={logout}>
            Выйти
          </button>
        </div>

        <h3 className="set-group">Внешний вид</h3>
        <Row
          title="Светлая тема"
          text="Переключает тёмную и светлую палитру интерфейса и слайдов."
          on={theme === "light"}
          onChange={() => setTheme(theme === "dark" ? "light" : "dark")}
        />
        <Row
          title="Свёрнутое меню разделов"
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

        <h3 className="set-group">Прогресс</h3>
        <div className="set-row">
          <div className="set-row-text">
            <span className="set-row-title">Сбросить прогресс упражнений</span>
            <span className="set-row-desc">
              Удаляет статусы задач, черновики кода и историю попыток. Вопросы и
              слайды не затрагиваются.
              {done === "practice" && <b className="set-done"> Готово.</b>}
            </span>
          </div>
          <button
            className="quiz-btn ghost"
            onClick={() =>
              reset(
                "practice",
                "Удалить решения, черновики и историю попыток во всех упражнениях?",
              )
            }
          >
            Сбросить
          </button>
        </div>
        <div className="set-row">
          <div className="set-row-text">
            <span className="set-row-title">Сбросить весь прогресс</span>
            <span className="set-row-desc">
              Обнуляет дашборд на главной: просмотренные слайды, ответы на
              вопросы и упражнения.
              {done === "all" && <b className="set-done"> Готово.</b>}
            </span>
          </div>
          <button
            className="quiz-btn ghost"
            onClick={() =>
              reset(
                "all",
                "Обнулить весь прогресс: слайды, вопросы и упражнения?",
              )
            }
          >
            Сбросить всё
          </button>
        </div>
      </section>
    </main>
  );
}

function Row({ title, text, on, onChange }: { title: string; text: string; on: boolean; onChange: () => void }) {
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
