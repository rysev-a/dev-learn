// Тонкая обёртка над fetch для JSON API: ошибки приходят как Error с текстом от сервера.

export class ApiError extends Error {
  constructor(message, status, detail) {
    super(message);
    this.status = status;
    this.detail = detail;
  }
}

// человекочитаемое сообщение из ответа FastAPI (detail — строка или список ошибок валидации)
function messageOf(detail, fallback) {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail) && detail.length) {
    const FIELD = {
      email: "Введите корректный email",
      login: "Логин: 3–32 символа — латиница, цифры, «_», «.», «-»",
      password: "Пароль: от 6 до 128 символов",
    };
    const field = detail[0]?.loc?.[detail[0].loc.length - 1];
    return FIELD[field] || detail[0]?.msg || fallback;
  }
  return fallback;
}

export async function api(path, { method = "GET", body, keepalive } = {}) {
  const res = await fetch(path, {
    method,
    headers: body !== undefined ? { "Content-Type": "application/json" } : undefined,
    body: body !== undefined ? JSON.stringify(body) : undefined,
    keepalive,
  });
  if (res.status === 401 && !path.startsWith("/api/auth/")) {
    // сессия истекла: AuthProvider вернёт пользователя на форму входа
    window.dispatchEvent(new Event("say-unauthorized"));
  }
  if (res.status === 204) return null;
  let data = null;
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
  return data;
}
