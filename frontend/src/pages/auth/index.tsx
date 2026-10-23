import { useState, type FormEvent, type ReactNode } from "react";
import { useAuth } from "../../lib/auth.tsx";

/* Вход и регистрация. Пока идёт разработка, форма входа сразу заполнена данными
   student/student, а под ней две кнопки быстрого входа за готовых пользователей. */

// в продакшен-сборке (npm run build) временных пользователей нет: ни предзаполнения, ни кнопок
const QUICK = import.meta.env.DEV ? ["student", "programmer"] : [];

export default function AuthPage({ themeButton }: { themeButton: ReactNode }) {
  const { login, register } = useAuth();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // вход: логин или email + пароль (в dev-сборке по умолчанию student@mail.com / student)
  const [ident, setIdent] = useState(import.meta.env.DEV ? "student@mail.com" : "");
  const [password, setPassword] = useState(import.meta.env.DEV ? "student" : "");
  // регистрация
  const [email, setEmail] = useState("");
  const [loginName, setLoginName] = useState("");
  const [regPassword, setRegPassword] = useState("");

  async function submit(action: () => Promise<void>) {
    if (busy) return;
    setBusy(true);
    setError(null);
    try {
      await action();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      setBusy(false);
    }
  }

  const onLogin = (e: FormEvent) => {
    e.preventDefault();
    submit(() => login(ident, password));
  };

  const onRegister = (e: FormEvent) => {
    e.preventDefault();
    submit(() => register(email, loginName, regPassword));
  };

  // «Войти как …»: подставить значения в форму и отправить её
  // вход по email подходит обоим бэкендам (у бэкенда на axum логинов нет); пароль временных пользователей совпадает с именем
  const quick = (name: string) => {
    const email = `${name}@mail.com`;
    setIdent(email);
    setPassword(name);
    submit(() => login(email, name));
  };

  const switchMode = (m: "login" | "register") => {
    setMode(m);
    setError(null);
  };

  return (
    <div className="auth-page">
      <header className="auth-top">
        <span className="auth-logo">CS.Core</span>
        {themeButton}
      </header>

      <main className="auth-card">
        <div className="auth-tabs" role="tablist">
          <button
            role="tab"
            aria-selected={mode === "login"}
            className={`auth-tab ${mode === "login" ? "on" : ""}`}
            onClick={() => switchMode("login")}
          >
            Вход
          </button>
          <button
            role="tab"
            aria-selected={mode === "register"}
            className={`auth-tab ${mode === "register" ? "on" : ""}`}
            onClick={() => switchMode("register")}
          >
            Регистрация
          </button>
        </div>

        {mode === "login" ? (
          <form className="auth-form" onSubmit={onLogin}>
            <label className="auth-field">
              <span>Логин или email</span>
              <input
                value={ident}
                onChange={(e) => setIdent(e.target.value)}
                autoComplete="username"
                autoFocus
                required
              />
            </label>
            <label className="auth-field">
              <span>Пароль</span>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                required
              />
            </label>
            {error && <p className="auth-error">{error}</p>}
            <button className="quiz-btn auth-submit" disabled={busy}>
              {busy ? "Входим…" : "Войти"}
            </button>

            {QUICK.length > 0 && <div className="auth-quick">
              <span className="auth-quick-label">Временно, для разработки</span>
              {QUICK.map((name) => (
                <button
                  type="button"
                  key={name}
                  className="quiz-btn ghost"
                  disabled={busy}
                  onClick={() => quick(name)}
                >
                  войти как {name}
                </button>
              ))}
            </div>}
          </form>
        ) : (
          <form className="auth-form" onSubmit={onRegister}>
            <label className="auth-field">
              <span>Email</span>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="email"
                autoFocus
                required
              />
            </label>
            <label className="auth-field">
              <span>Логин</span>
              <input
                value={loginName}
                onChange={(e) => setLoginName(e.target.value)}
                autoComplete="username"
                pattern="[A-Za-z0-9_.\-]{3,32}"
                title="3–32 символа: латиница, цифры, «_», «.», «-»"
                required
              />
            </label>
            <label className="auth-field">
              <span>Пароль</span>
              <input
                type="password"
                value={regPassword}
                onChange={(e) => setRegPassword(e.target.value)}
                autoComplete="new-password"
                minLength={6}
                maxLength={128}
                title="От 6 символов"
                required
              />
            </label>
            {error && <p className="auth-error">{error}</p>}
            <button className="quiz-btn auth-submit" disabled={busy}>
              {busy ? "Создаём…" : "Создать аккаунт"}
            </button>
          </form>
        )}
      </main>
    </div>
  );
}
