import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { api } from "./api.js";

/* Текущий пользователь. user: undefined — ещё узнаём, null — не вошёл. Сессия
   живёт в HttpOnly-cookie, а клиент лишь спрашивает /api/auth/me. */

const AuthContext = createContext(null);

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(undefined);

  useEffect(() => {
    api("/api/auth/me")
      .then(setUser)
      .catch(() => setUser(null));
    const onExpired = () => setUser(null);
    window.addEventListener("say-unauthorized", onExpired);
    return () => window.removeEventListener("say-unauthorized", onExpired);
  }, []);

  const login = useCallback(
    async (ident, password) =>
      setUser(await api("/api/auth/login", { method: "POST", body: { login: ident, password } })),
    [],
  );

  const register = useCallback(
    async (email, loginName, password) =>
      setUser(
        await api("/api/auth/register", {
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
