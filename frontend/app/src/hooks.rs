//! Data loading in components: request state as a signal.

use std::future::Future;

use api::{ApiError, Client};
use leptos::{prelude::*, task::spawn_local};

/// Loading state.
#[derive(Clone, Debug, PartialEq)]
pub enum Load<T> {
    Loading,
    Ready(T),
    Failed(String),
}

impl<T> Load<T> {
    pub fn ready(&self) -> Option<&T> {
        match self {
            Load::Ready(v) => Some(v),
            _ => None,
        }
    }
}

thread_local! {
    static CLIENT: std::cell::RefCell<Option<Client>> = const { std::cell::RefCell::new(None) };
}

/// Remembers the application's API client (called once at session start).
pub fn install_client(client: Client) {
    CLIENT.with(|c| *c.borrow_mut() = Some(client));
}

/// The application's API client. Not from the Leptos context: it is needed in async tasks and timers where the owner is already gone.
pub fn client() -> Client {
    CLIENT.with(|c| c.borrow().clone()).expect("API client not set: the session has not been created")
}

/// Loads data whenever the key changes: if `key()` returned `None` - nothing is loaded (state `Loading`);
/// the response of a stale request is discarded.
pub fn use_load<K, T, Fut>(key: impl Fn() -> Option<K> + 'static, fetch: impl Fn(Client, K) -> Fut + 'static) -> ReadSignal<Load<T>>
where
    K: Clone + 'static,
    T: Send + Sync + 'static,
    Fut: Future<Output = Result<T, ApiError>> + 'static,
{
    let (state, set) = signal(Load::Loading);
    let generation = StoredValue::new(0u64);
    Effect::new(move |_| {
        let Some(k) = key() else {
            set.set(Load::Loading);
            return;
        };
        generation.update_value(|g| *g += 1);
        let mine = generation.get_value();
        set.set(Load::Loading);
        let fut = fetch(client(), k);
        spawn_local(async move {
            let res = fut.await;
            if generation.try_get_value() == Some(mine) {
                set.set(match res {
                    Ok(v) => Load::Ready(v),
                    Err(e) => Load::Failed(e.message),
                });
            }
        });
    });
    state
}
