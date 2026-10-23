//! Загрузка данных в компонентах: состояние запроса как сигнал.

use std::future::Future;

use api::{ApiError, Client};
use leptos::{prelude::*, task::spawn_local};

/// Состояние загрузки.
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

/// Запоминает клиент API приложения (вызывается один раз при старте сессии).
pub fn install_client(client: Client) {
    CLIENT.with(|c| *c.borrow_mut() = Some(client));
}

/// Клиент API приложения. Не из контекста Leptos: он нужен и в асинхронных задачах, и в таймерах, где владельца уже нет.
pub fn client() -> Client {
    CLIENT.with(|c| c.borrow().clone()).expect("клиент API не установлен: сессия не создана")
}

/// Загружает данные при каждом изменении ключа: `key()` вернул `None` — ничего не грузим (состояние `Loading`);
/// ответ устаревшего запроса отбрасывается.
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
