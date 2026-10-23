//! Сессия: токен и личность вошедшего пользователя. Токен выдаёт `/api/auth/login`, хранится в `localStorage`
//! (ключ `say-token`) и уходит в каждый запрос заголовком `Authorization: Bearer`.

use api::{dto::Identity, ApiError, Client};
use leptos::{prelude::*, task::spawn_local};

use crate::settings;

#[derive(Clone, Copy)]
pub struct Session {
    pub token: RwSignal<Option<String>>,
    pub identity: RwSignal<Option<Identity>>,
    /// проверка сохранённого токена закончилась
    pub checked: RwSignal<bool>,
}

impl Session {
    fn forget(&self) {
        settings::write(settings::TOKEN, None);
        self.token.set(None);
        self.identity.set(None);
    }

    fn remember(&self, id: Identity) {
        if let Some(token) = &id.token {
            settings::write(settings::TOKEN, Some(token));
            self.token.set(Some(token.clone()));
        }
        self.identity.set(Some(id));
    }

    pub async fn login(&self, client: &Client, email: &str, password: &str) -> Result<(), ApiError> {
        let id = client.login(email.trim(), password).await?;
        self.remember(id);
        Ok(())
    }

    /// Регистрация и сразу вход (подтверждение почты входу не мешает).
    pub async fn register(&self, client: &Client, email: &str, name: &str, password: &str) -> Result<(), ApiError> {
        client.signup(email.trim(), password, name.trim()).await?;
        self.login(client, email, password).await
    }

    pub fn logout(&self, client: Client) {
        let me = *self;
        spawn_local(async move {
            let _ = client.logout().await;
            me.forget();
        });
    }
}

/// Создаёт сессию и клиент API, кладёт их в контекст и проверяет сохранённый токен.
pub fn provide_session() -> Session {
    let session = Session { token: RwSignal::new(settings::read(settings::TOKEN).filter(|t| !t.is_empty())), identity: RwSignal::new(None), checked: RwSignal::new(false) };
    let client = Client::new(move || session.token.get_untracked(), move || session.forget());
    provide_context(session);
    crate::hooks::install_client(client.clone());
    if session.token.get_untracked().is_some() {
        spawn_local(async move {
            match client.me().await {
                Ok(id) => session.identity.set(Some(id)),
                Err(_) => session.forget(),
            }
            session.checked.set(true);
        });
    } else {
        session.checked.set(true);
    }
    session
}
