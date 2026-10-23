// Тонкая обёртка над fetch для JSON API: ошибки приходят как Error с текстом от сервера.

export class ApiError extends Error {
  readonly status: number;
  readonly detail: unknown;

  constructor(message: string, status: number, detail: unknown) {
    super(message);
    this.status = status;
    this.detail = detail;
  }
}

// Сессия: Python-бэкенд держит её в HttpOnly-cookie, бэкенд на axum (общие crates lab) выдаёт токен при входе —
// он хранится в localStorage и уходит заголовком Authorization: Bearer. Клиент работает с обоими.
const TOKEN_KEY = "say-token";

export const getToken = (): string | null => {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
};

export const setToken = (token: string | null): void => {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token);
    else localStorage.removeItem(TOKEN_KEY);
  } catch {
    /* хранилище недоступно — токен живёт до перезагрузки только в cookie-режиме */
  }
};

interface ValidationIssue {
  loc?: (string | number)[];
  msg?: string;
}

const FIELD_MESSAGES: Record<string, string> = {
  email: "Введите корректный email",
  login: "Логин: 3–32 символа — латиница, цифры, «_», «.», «-»",
  password: "Пароль: от 6 до 128 символов",
};

// человекочитаемое сообщение из ответа FastAPI (detail — строка или список ошибок валидации)
function messageOf(detail: unknown, fallback: string): string {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail) && detail.length) {
    const first = detail[0] as ValidationIssue;
    const field = first?.loc?.[first.loc.length - 1];
    return (typeof field === "string" && FIELD_MESSAGES[field]) || first?.msg || fallback;
  }
  return fallback;
}

export interface ApiOptions {
  method?: "GET" | "POST" | "PUT" | "DELETE";
  body?: unknown;
  keepalive?: boolean;
}

export async function api<T = unknown>(
  path: string,
  { method = "GET", body, keepalive }: ApiOptions = {},
): Promise<T> {
  const init: RequestInit = { method };
  const headers: Record<string, string> = {};
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    init.body = JSON.stringify(body);
  }
  if (Object.keys(headers).length) init.headers = headers;
  if (keepalive !== undefined) init.keepalive = keepalive;
  const res = await fetch(path, init);
  if (res.status === 401 && !path.startsWith("/api/auth/")) {
    // сессия истекла: AuthProvider вернёт пользователя на форму входа
    window.dispatchEvent(new Event("say-unauthorized"));
  }
  if (res.status === 204) return null as T;
  // у FastAPI ошибка в `detail`, у бэкенда на axum — `detail` (наши маршруты) или `error` (crates lab)
  let data: { detail?: unknown; error?: unknown } | null = null;
  try {
    data = await res.json();
  } catch {
    /* пустой или не JSON */
  }
  if (!res.ok)
    throw new ApiError(
      messageOf(data?.detail ?? data?.error, `Ошибка ${res.status}`),
      res.status,
      data?.detail ?? data?.error,
    );
  return data as T;
}
