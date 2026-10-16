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
  if (body !== undefined) {
    init.headers = { "Content-Type": "application/json" };
    init.body = JSON.stringify(body);
  }
  if (keepalive !== undefined) init.keepalive = keepalive;
  const res = await fetch(path, init);
  if (res.status === 401 && !path.startsWith("/api/auth/")) {
    // сессия истекла: AuthProvider вернёт пользователя на форму входа
    window.dispatchEvent(new Event("say-unauthorized"));
  }
  if (res.status === 204) return null as T;
  let data: { detail?: unknown } | null = null;
  try {
    data = await res.json();
  } catch {
    /* пустой или не JSON */
  }
  if (!res.ok)
    throw new ApiError(
      messageOf(data?.detail, `Ошибка ${res.status}`),
      res.status,
      data?.detail,
    );
  return data as T;
}
