//! Session: token and identity of the signed-in user. The token is issued by `/api/auth/login`, stored in `localStorage`
//! (key `cs-core-token`) and sent with every request in the `Authorization: Bearer` header.

use api::{dto::Identity, ApiError, Client};
use leptos::{prelude::*, task::spawn_local};

use crate::settings;

#[derive(Clone, Copy)]
pub struct Session {
    pub token: RwSignal<Option<String>>,
    pub identity: RwSignal<Option<Identity>>,
    /// checking the saved token has finished
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

    /// Registration and immediate sign-in (email confirmation does not prevent signing in).
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

/// Creates the session and API client, puts them in the context and checks the saved token.
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
