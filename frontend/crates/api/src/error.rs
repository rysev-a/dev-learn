use serde_json::Value;

/// Ошибка вызова API: статус (0 — нет связи) и текст для пользователя.
#[derive(Clone, Debug, PartialEq)]
pub struct ApiError {
    pub status: u16,
    pub message: String,
}

impl std::fmt::Display for ApiError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.message)
    }
}

impl std::error::Error for ApiError {}

const FIELD_MESSAGES: [(&str, &str); 3] = [
    ("email", "Введите корректный email"),
    ("login", "Логин: 3–32 символа — латиница, цифры, «_», «.», «-»"),
    ("password", "Пароль: от 6 до 128 символов"),
];

/// Человекочитаемое сообщение из тела ошибки: `detail` — строка или список ошибок валидации FastAPI, `error` — строка (crates lab).
pub fn message_of(body: &Value, status: u16) -> String {
    let fallback = || format!("Ошибка {status}");
    let detail = body.get("detail").or_else(|| body.get("error"));
    match detail {
        Some(Value::String(s)) => s.clone(),
        Some(Value::Array(items)) if !items.is_empty() => {
            let first = &items[0];
            let field = first.get("loc").and_then(Value::as_array).and_then(|l| l.last()).and_then(Value::as_str);
            field
                .and_then(|f| FIELD_MESSAGES.iter().find(|(k, _)| *k == f).map(|(_, m)| (*m).to_string()))
                .or_else(|| first.get("msg").and_then(Value::as_str).map(String::from))
                .unwrap_or_else(fallback)
        }
        _ => fallback(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn reads_detail_string_error_string_and_validation_lists() {
        assert_eq!(message_of(&json!({ "detail": "Нужно войти" }), 401), "Нужно войти");
        assert_eq!(message_of(&json!({ "error": "invalid email or password" }), 401), "invalid email or password");
        assert_eq!(message_of(&json!({ "detail": [{ "loc": ["body", "email"], "msg": "bad" }] }), 422), "Введите корректный email");
        assert_eq!(message_of(&json!({ "detail": [{ "loc": ["body", "zzz"], "msg": "странно" }] }), 422), "странно");
        assert_eq!(message_of(&json!({}), 500), "Ошибка 500");
        assert_eq!(message_of(&json!(null), 502), "Ошибка 502");
    }
}
