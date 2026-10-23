import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import type { User } from "../types.ts";
import { api, ApiError, setToken } from "./api.ts";

/* Текущий пользователь. user: undefined — ещё узнаём, null — не вошёл. Сессия
   живёт в HttpOnly-cookie, а клиент лишь спрашивает /api/auth/me. */

interface AuthValue {
  user: User | null | undefined;
  login: (ident: string, password: string) => Promise<void>;
  register: (email: string, loginName: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

/* Ответ бэкенда о пользователе: у Python — {id, email, login}; у бэкенда на axum — личность {user: {id, email, profile}, token?, …}. */
interface AxumUser {
  id: string;
  email: string;
  profile?: { name?: string };
}
type Reply = User | { user: AxumUser; token?: string };

function userOf(reply: Reply): User {
  if (!("user" in reply)) return reply;
  const u = reply.user;
  const name = u.profile?.name?.trim();
  return { id: u.id, email: u.email, login: name || u.email.split("@")[0] || u.email };
}

function remember(reply: Reply): User {
  if ("token" in reply && reply.token) setToken(reply.token);
  return userOf(reply);
}

const AuthContext = createContext<AuthValue | null>(null);

export const useAuth = (): AuthValue => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null | undefined>(undefined);

  useEffect(() => {
    api<Reply>("/api/auth/me")
      .then((r) => setUser(userOf(r)))
      .catch(() => setUser(null));
    const onExpired = () => {
      setToken(null);
      setUser(null);
    };
    window.addEventListener("say-unauthorized", onExpired);
    return () => window.removeEventListener("say-unauthorized", onExpired);
  }, []);

  const login = useCallback(
    // логин и email отправляем оба: Python принимает `login` (логин или email), бэкенд на axum — `email`
    async (ident: string, password: string) =>
      setUser(
        remember(
          await api<Reply>("/api/auth/login", {
            method: "POST",
            body: { login: ident, email: ident, password },
          }),
        ),
      ),
    [],
  );

  const register = useCallback(
    async (email: string, loginName: string, password: string) => {
      try {
        setUser(
          remember(
            await api<Reply>("/api/auth/register", {
              method: "POST",
              body: { email, login: loginName, password },
            }),
          ),
        );
      } catch (e) {
        // бэкенд на axum: регистрация — /signup (без сессии), затем обычный вход
        if (!(e instanceof ApiError) || (e.status !== 404 && e.status !== 405)) throw e;
        await api("/api/auth/signup", { method: "POST", body: { email, password, name: loginName } });
        setUser(
          remember(
            await api<Reply>("/api/auth/login", {
              method: "POST",
              body: { login: email, email, password },
            }),
          ),
        );
      }
    },
    [],
  );

  const logout = useCallback(async () => {
    try {
      await api("/api/auth/logout", { method: "POST" });
    } finally {
      setToken(null);
      setUser(null);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
