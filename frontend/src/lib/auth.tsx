import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import type { User } from "../types.ts";
import { api } from "./api.ts";

/* Текущий пользователь. user: undefined — ещё узнаём, null — не вошёл. Сессия
   живёт в HttpOnly-cookie, а клиент лишь спрашивает /api/auth/me. */

interface AuthValue {
  user: User | null | undefined;
  login: (ident: string, password: string) => Promise<void>;
  register: (email: string, loginName: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
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
    api<User>("/api/auth/me")
      .then(setUser)
      .catch(() => setUser(null));
    const onExpired = () => setUser(null);
    window.addEventListener("say-unauthorized", onExpired);
    return () => window.removeEventListener("say-unauthorized", onExpired);
  }, []);

  const login = useCallback(
    async (ident: string, password: string) =>
      setUser(
        await api<User>("/api/auth/login", {
          method: "POST",
          body: { login: ident, password },
        }),
      ),
    [],
  );

  const register = useCallback(
    async (email: string, loginName: string, password: string) =>
      setUser(
        await api<User>("/api/auth/register", {
          method: "POST",
          body: { email, login: loginName, password },
        }),
      ),
    [],
  );

  const logout = useCallback(async () => {
    try {
      await api("/api/auth/logout", { method: "POST" });
    } finally {
      setUser(null);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
