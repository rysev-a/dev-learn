//! Формы карточки устройства: общие кирпичики (поле, список, флажок, кнопка) и основные настройки — интерфейсы, шлюз,
//! маршруты, NAT, файрвол, слушающие порты, порты коммутатора и таблица MAC. Формы меняют сеть теми же функциями
//! крейта, что и терминал, поэтому результат одинаков. Закрытые устройства (`locked`) показываются только для чтения.

use leptos::prelude::*;
use netlab::term::{add_route, del_route, get_gateway, set_gateway, set_up};
use netlab::types::{Device, FwAction, NatAction, Proto, Service};

use super::lab::Lab;
use super::logic;

/// Устройство, которое настраивает форма: выбранное в карточке. Копируется как набор сигналов.
#[derive(Clone, Copy)]
pub struct Ctx {
    pub lab: Lab,
    id: StoredValue<String>,
    /// устройство закрыто: формы только показывают настройки
    pub ro: bool,
}

impl Ctx {
    pub fn new(lab: Lab, id: &str) -> Ctx {
        let ro = lab.device(id).is_some_and(|d| d.locked);
        Ctx { lab, id: StoredValue::new(id.to_string()), ro }
    }

    pub fn id(&self) -> String {
        self.id.get_value()
    }

    /// Прочитать устройство (в реактивном контексте — подписка на сеть).
    pub fn read<R>(&self, f: impl FnOnce(&Device) -> R) -> Option<R> {
        let id = self.id.get_value();
        self.lab.net.with(|n| n.devices.get(&id).map(f))
    }

    /// Изменить устройство: цели пересчитываются, черновик сохраняется.
    pub fn edit<R>(&self, f: impl FnOnce(&mut Device) -> R) -> Option<R> {
        if self.ro {
            return None;
        }
        self.lab.edit_device(&self.id.get_value(), f)
    }

    /// Выполнить команду терминала на этом устройстве; вернуть её вывод.
    pub fn exec(&self, line: &str) -> String {
        self.lab.form_exec(&self.id.get_value(), line)
    }
}

/* ---- кирпичики ---- */

/// Однострочное поле; `digits > 0` — только цифры, не больше столько знаков; `on_commit` — на потерю фокуса и Enter.
#[component]
pub fn TextIn(
    value: RwSignal<String>,
    #[prop(optional)] placeholder: &'static str,
    #[prop(optional)] class: &'static str,
    #[prop(optional)] label: &'static str,
    #[prop(optional)] disabled: bool,
    #[prop(optional)] digits: usize,
    #[prop(optional, into)] on_commit: Option<Callback<()>>,
) -> impl IntoView {
    // blur приходит, когда форма уже уничтожена (смена устройства при фокусе в поле): тогда сигнал формы мёртв — фиксировать нечего
    let commit = move || {
        if let (Some(c), true) = (on_commit, value.try_get_untracked().is_some()) {
            c.run(());
        }
    };
    view! {
        <input
            class=class
            prop:value=move || value.get()
            placeholder=placeholder
            disabled=disabled
            aria-label=label
            spellcheck="false"
            on:input=move |e| {
                let raw = event_target_value(&e);
                if digits > 0 {
                    let clean = logic::digits(&raw, digits);
                    if clean != raw {
                        event_target::<web_sys::HtmlInputElement>(&e).set_value(&clean);
                    }
                    value.set(clean);
                } else {
                    value.set(raw);
                }
            }
            on:blur=move |_| commit()
            on:keydown=move |e| {
                if e.key() == "Enter" {
                    commit();
                }
            }
        />
    }
}

/// Выпадающий список: пары «значение — подпись».
#[component]
pub fn Pick(
    options: Vec<(String, String)>,
    #[prop(into)] value: Signal<String>,
    on_pick: Callback<String>,
    #[prop(optional)] disabled: bool,
    #[prop(optional)] label: &'static str,
) -> impl IntoView {
    let items = options
        .into_iter()
        .map(|(v, text)| {
            let cur = v.clone();
            view! { <option value=v prop:selected=move || value.get() == cur>{text}</option> }
        })
        .collect_view();
    view! {
        <select disabled=disabled aria-label=label on:change=move |e| on_pick.run(event_target_value(&e))>{items}</select>
    }
}

/// Варианты списка, у которых подпись равна значению.
pub fn same(values: &[&str]) -> Vec<(String, String)> {
    values.iter().map(|v| (v.to_string(), v.to_string())).collect()
}

/// Флажок с подписью.
#[component]
pub fn Check(
    #[prop(into)] checked: Signal<bool>,
    on_change: Callback<bool>,
    #[prop(into)] label: String,
    #[prop(optional)] disabled: bool,
    #[prop(optional)] class: &'static str,
) -> impl IntoView {
    view! {
        <label class=format!("nl-up {class}")>
            <input type="checkbox" prop:checked=move || checked.get() disabled=disabled on:change=move |e| on_change.run(event_target_checked(&e)) />
            {label}
        </label>
    }
}

/// Сообщение (ошибка или ответ терминала) под формой.
#[component]
pub fn Msg(msg: RwSignal<String>) -> impl IntoView {
    move || {
        let m = msg.get();
        (!m.is_empty()).then(|| view! { <em class="nl-err">{m}</em> })
    }
}

/// Кнопка «×» в строке списка.
#[component]
pub fn Cross(label: &'static str, on_click: Callback<()>) -> impl IntoView {
    view! { <button type="button" class="nl-x" aria-label=label on:click=move |_| on_click.run(())>"×"</button> }
}

/// Небольшая кнопка действия.
#[component]
pub fn Btn(#[prop(into)] label: Signal<String>, on_click: Callback<()>, #[prop(optional)] disabled: bool) -> impl IntoView {
    view! { <button type="button" class="quiz-btn ghost" disabled=disabled on:click=move |_| on_click.run(())>{move || label.get()}</button> }
}

/// Раздел формы с заголовком.
#[component]
pub fn Section(title: &'static str, children: Children) -> impl IntoView {
    view! { <div class="nl-sec"><h4>{title}</h4>{children()}</div> }
}

/* ---- интерфейсы ---- */

/// Интерфейсы устройства: адрес, маска, «вкл» и (если открыт инструмент) длина очереди.
#[component]
pub fn Interfaces(ctx: Ctx, queue: bool) -> impl IntoView {
    // строка живёт, пока есть интерфейс: при вводе адреса и маски она не пересоздаётся и фокус не теряется;
    // если сеть меняет что-то снаружи (терминал, «Сбросить»), поля подтягивают записанное (см. `IfaceRow`)
    let keys = Memo::new(move |_| ctx.read(|d| d.ifaces.iter().map(|i| (i.name.clone(), i.ip.clone(), i.prefix)).collect::<Vec<_>>()).unwrap_or_default());
    view! {
        <div class="nl-sec">
            <h4>"Интерфейсы"</h4>
            <For
                each=move || keys.get()
                key=|k| k.0.clone()
                children=move |(name, ip, prefix)| view! { <IfaceRow ctx=ctx name=name ip=ip prefix=prefix queue=queue /> }
            />
        </div>
    }
}

#[component]
fn IfaceRow(ctx: Ctx, name: String, ip: Option<String>, prefix: u8, queue: bool) -> impl IntoView {
    let ip = RwSignal::new(ip.unwrap_or_default());
    let pre = RwSignal::new(prefix.to_string());
    let err = RwSignal::new(String::new());
    let queue_len = RwSignal::new(ctx.read(|d| d.iface(&name).and_then(|i| i.txqueuelen)).flatten().unwrap_or(1000).to_string());
    // записанные в сети адрес и маска; когда они меняются, поля показывают новое (то, что ввели сами, уже совпадает)
    let stored = {
        let name = name.clone();
        Memo::new(move |_| ctx.read(|d| d.iface(&name).map(|i| (i.ip.clone().unwrap_or_default(), i.prefix.to_string()))).flatten())
    };
    Effect::new(move |prev: Option<Option<(String, String)>>| {
        let now = stored.get();
        if let (Some(Some((prev_ip, prev_pre))), Some((ip_now, pre_now))) = (&prev, &now) {
            if prev_ip != ip_now {
                ip.set(ip_now.clone());
            }
            if prev_pre != pre_now {
                pre.set(pre_now.clone());
            }
        }
        now
    });
    let mac = {
        let name = name.clone();
        move || ctx.read(|d| d.iface(&name).map(|i| i.mac.clone())).flatten().unwrap_or_default()
    };
    let up = {
        let name = name.clone();
        move || ctx.read(|d| d.iface(&name).map(|i| i.up)).flatten().unwrap_or(true)
    };
    let commit = {
        let name = name.clone();
        Callback::new(move |()| {
            if ctx.ro {
                return;
            }
            err.set(String::new());
            let (ip, pre) = (ip.get_untracked(), pre.get_untracked());
            if let Some(Some(e)) = ctx.edit(|d| logic::commit_iface_addr(d, &name, &ip, &pre)) {
                err.set(e);
            }
        })
    };
    let toggle = {
        let name = name.clone();
        Callback::new(move |on: bool| {
            ctx.edit(|d| set_up(d, &name, on));
        })
    };
    let set_queue = {
        let name = name.clone();
        Callback::new(move |()| {
            let v: u32 = queue_len.get_untracked().parse().unwrap_or(0);
            if (1..=10000).contains(&v) {
                ctx.edit(|d| {
                    if let Some(i) = d.iface_mut(&name) {
                        i.txqueuelen = Some(v);
                    }
                });
            }
        })
    };
    let aria_ip = format!("IP {name}");
    view! {
        <div class="nl-iface">
            <div class="nl-iface-name"><b>{name}</b><small>{mac}</small></div>
            <input
                prop:value=move || ip.get()
                on:input=move |e| ip.set(event_target_value(&e))
                on:blur=move |_| if ip.try_get_untracked().is_some() { commit.run(()) }
                on:keydown=move |e| {
                    if e.key() == "Enter" {
                        commit.run(());
                    }
                }
                placeholder="IP-адрес"
                disabled=ctx.ro
                aria-label=aria_ip
                spellcheck="false"
            />
            <span class="nl-slash">"/"</span>
            <TextIn value=pre class="nl-prefix" digits=2 disabled=ctx.ro label="Маска" on_commit=commit />
            <Check checked=Signal::derive(up) on_change=toggle label="вкл" disabled=ctx.ro />
            {queue.then(|| view! {
                <label class="nl-up">
                    "очередь"
                    <TextIn value=queue_len class="nl-prefix wide" digits=5 disabled=ctx.ro label="Очередь" on_commit=set_queue />
                    "пакетов"
                </label>
            })}
            {move || {
                let e = err.get();
                (!e.is_empty()).then(|| view! { <em class="nl-err">{e}</em> })
            }}
        </div>
    }
}

/// Шлюз по умолчанию (компьютеры и серверы).
#[component]
pub fn Gateway(ctx: Ctx) -> impl IntoView {
    let gw = RwSignal::new(ctx.read(get_gateway).unwrap_or_default());
    let err = RwSignal::new(String::new());
    let commit = Callback::new(move |()| {
        if ctx.ro {
            return;
        }
        err.set(String::new());
        if let Some(Some(e)) = ctx.edit(|d| set_gateway(d, Some(gw.get_untracked().trim()))) {
            err.set(e);
        }
    });
    view! {
        <div class="nl-sec">
            <label class="nl-field">
                <span>"Шлюз по умолчанию"</span>
                <TextIn value=gw placeholder="например 192.168.0.1 (пусто — шлюза нет)" disabled=ctx.ro on_commit=commit />
                <Msg msg=err />
            </label>
        </div>
    }
}

/// Пересылка пакетов между интерфейсами (ip_forward) у маршрутизаторов.
#[component]
pub fn Forwarding(ctx: Ctx) -> impl IntoView {
    view! {
        <div class="nl-sec">
            <Check
                checked=Signal::derive(move || ctx.read(|d| d.forward).unwrap_or(false))
                on_change=Callback::new(move |on| {
                    ctx.edit(|d| d.forward = on);
                })
                label="пересылать пакеты между интерфейсами (ip_forward)"
                disabled=ctx.ro
            />
        </div>
    }
}

/// Таблица маршрутов с добавлением и удалением статических.
#[component]
pub fn Routes(ctx: Ctx) -> impl IntoView {
    let dst = RwSignal::new(String::new());
    let via = RwSignal::new(String::new());
    let err = RwSignal::new(String::new());
    let rows = Memo::new(move |_| ctx.read(logic::route_rows).unwrap_or_default());
    let add = Callback::new(move |()| {
        err.set(String::new());
        let (d, v) = (dst.get_untracked(), via.get_untracked());
        let (d, v) = (d.trim().to_string(), v.trim().to_string());
        let res = ctx.edit(|dev| add_route(dev, Some(if d.is_empty() { "default" } else { &d }), (!v.is_empty()).then_some(v.as_str()), None));
        match res.flatten() {
            Some(e) => err.set(e),
            None => {
                dst.set(String::new());
                via.set(String::new());
            }
        }
    });
    view! {
        <div class="nl-sec">
            <h4>"Таблица маршрутов"</h4>
            <table class="nl-table">
                <tbody>
                    {move || rows.get().into_iter().map(|r| {
                        let key = r.dst.clone();
                        view! {
                            <tr>
                                <td>{r.dst}</td>
                                <td>{r.via}</td>
                                <td>{r.dev}</td>
                                <td>
                                    {(!r.connected && !ctx.ro).then(|| view! {
                                        <Cross label="Удалить маршрут" on_click=Callback::new(move |()| {
                                            ctx.edit(|d| del_route(d, Some(&key)));
                                        }) />
                                    })}
                                </td>
                            </tr>
                        }
                    }).collect_view()}
                </tbody>
            </table>
            {(!ctx.ro).then(|| view! {
                <div class="nl-add">
                    <TextIn value=dst placeholder="сеть 10.0.0.0/24 или default" />
                    <TextIn value=via placeholder="через шлюз 10.0.1.1" />
                    <Btn label="+ маршрут" on_click=add />
                </div>
            })}
            <Msg msg=err />
        </div>
    }
}

/* ---- NAT ---- */

fn iface_names(ctx: Ctx) -> Vec<String> {
    ctx.read(|d| d.ifaces.iter().map(|i| i.name.clone()).collect()).unwrap_or_default()
}

/// NAT: MASQUERADE на внешнем интерфейсе и проброс порта.
#[component]
pub fn Nat(ctx: Ctx) -> impl IntoView {
    let names = iface_names(ctx);
    let last = names.last().cloned().unwrap_or_default();
    let out = RwSignal::new(last.clone());
    let inn = RwSignal::new(last);
    let proto = RwSignal::new("tcp".to_string());
    let port = RwSignal::new(String::new());
    let to = RwSignal::new(String::new());
    let msg = RwSignal::new(String::new());
    let masq = Memo::new(move |_| ctx.read(|d| d.nat.iter().find(|n| n.action == NatAction::Masquerade).map(|n| n.out.clone().unwrap_or_default())).flatten());
    let rules = Memo::new(move |_| {
        ctx.read(|d| {
            d.nat
                .iter()
                .map(|n| {
                    let mut p = vec![format!("{}:", n.chain.as_str()), n.action.as_str().to_string()];
                    if let Some(o) = &n.out {
                        p.push(format!("-o {o}"));
                    }
                    if let Some(i) = &n.iif {
                        p.push(format!("-i {i}"));
                    }
                    if let Some(dp) = n.dport {
                        p.push(format!("порт {dp}"));
                    }
                    if let Some(t) = &n.to {
                        p.push(format!("→ {t}"));
                    }
                    p.join(" ")
                })
                .collect::<Vec<_>>()
        })
        .unwrap_or_default()
    });
    let toggle = Callback::new(move |()| {
        let line = match masq.get_untracked() {
            Some(o) => format!("iptables -t nat -D POSTROUTING -o {o} -j MASQUERADE"),
            None => format!("iptables -t nat -A POSTROUTING -o {} -j MASQUERADE", out.get_untracked()),
        };
        msg.set(ctx.exec(&line));
    });
    let forward = Callback::new(move |()| {
        msg.set(ctx.exec(&format!(
            "iptables -t nat -A PREROUTING -i {} -p {} --dport {} -j DNAT --to-destination {}",
            inn.get_untracked(),
            proto.get_untracked(),
            port.get_untracked(),
            to.get_untracked()
        )));
    });
    let opts = move || names.iter().map(|n| (n.clone(), n.clone())).collect::<Vec<_>>();
    view! {
        <div class="nl-sec">
            <h4>"NAT"</h4>
            <div class="nl-add">
                <span class="nl-lbl">"MASQUERADE на интерфейсе"</span>
                <Pick options=opts() value=out on_pick=Callback::new(move |v| out.set(v)) disabled=ctx.ro />
                <Btn
                    label=Signal::derive(move || match masq.get() {
                        Some(o) => format!("выключить (сейчас {o})"),
                        None => "включить".to_string(),
                    })
                    on_click=toggle
                    disabled=ctx.ro
                />
            </div>
            <div class="nl-add">
                <span class="nl-lbl">"Проброс порта: вход"</span>
                <Pick options=opts() value=inn on_pick=Callback::new(move |v| inn.set(v)) disabled=ctx.ro />
                <Pick options=same(&["tcp"]) value=proto on_pick=Callback::new(move |v| proto.set(v)) disabled=ctx.ro />
                <TextIn value=port class="nl-prefix wide" digits=5 placeholder="порт" disabled=ctx.ro />
                <TextIn value=to placeholder="на 192.168.0.10:8080" disabled=ctx.ro />
                <Btn label="+ проброс" on_click=forward disabled=ctx.ro />
            </div>
            <ul class="nl-rules">
                {move || rules.get().into_iter().enumerate().map(|(k, text)| view! {
                    <li>
                        <code>{text}</code>
                        {(!ctx.ro).then(|| view! {
                            <Cross label="Удалить правило" on_click=Callback::new(move |()| {
                                ctx.edit(|d| {
                                    if k < d.nat.len() {
                                        d.nat.remove(k);
                                    }
                                });
                            }) />
                        })}
                    </li>
                }).collect_view()}
                {move || rules.with(Vec::is_empty).then(|| view! { <li class="nl-none">"правил NAT нет"</li> })}
            </ul>
            <Msg msg=msg />
        </div>
    }
}

/* ---- файрвол ---- */

/// Файрвол: политика цепочки FORWARD и правила.
#[component]
pub fn Firewall(ctx: Ctx) -> impl IntoView {
    let action = RwSignal::new("ACCEPT".to_string());
    let src = RwSignal::new(String::new());
    let dst = RwSignal::new(String::new());
    let proto = RwSignal::new(String::new());
    let port = RwSignal::new(String::new());
    let state = RwSignal::new(String::new());
    let msg = RwSignal::new(String::new());
    let policy = Signal::derive(move || ctx.read(|d| d.fw.policy.as_str().to_string()).unwrap_or_default());
    let rules = Memo::new(move |_| {
        ctx.read(|d| {
            d.fw
                .rules
                .iter()
                .map(|r| {
                    let mut p = vec![r.action.as_str().to_string()];
                    if let Some(x) = &r.proto {
                        p.push(x.clone());
                    }
                    if let Some(x) = &r.src {
                        p.push(format!("от {x}"));
                    }
                    if let Some(x) = &r.dst {
                        p.push(format!("к {x}"));
                    }
                    if let Some(x) = r.dport {
                        p.push(format!("порт {x}"));
                    }
                    if let Some(s) = r.state {
                        p.push(if s == netlab::types::ConnState::Established { "(установленные)".into() } else { "(новые)".into() });
                    }
                    p.join(" ")
                })
                .collect::<Vec<_>>()
        })
        .unwrap_or_default()
    });
    let add = Callback::new(move |()| {
        msg.set(ctx.exec(&logic::fw_rule_command(
            &action.get_untracked(),
            &proto.get_untracked(),
            &src.get_untracked(),
            &dst.get_untracked(),
            &port.get_untracked(),
            &state.get_untracked(),
        )));
    });
    view! {
        <div class="nl-sec">
            <h4>"Файрвол (цепочка FORWARD)"</h4>
            <div class="nl-add">
                <span class="nl-lbl">"Политика по умолчанию"</span>
                <Pick
                    options=same(&["ACCEPT", "DROP"])
                    value=policy
                    on_pick=Callback::new(move |v: String| {
                        if FwAction::parse(&v).is_some() {
                            msg.set(ctx.exec(&format!("iptables -P FORWARD {v}")));
                        }
                    })
                    disabled=ctx.ro
                />
            </div>
            <div class="nl-add wrap">
                <Pick options=same(&["ACCEPT", "DROP", "REJECT"]) value=action on_pick=Callback::new(move |v| action.set(v)) disabled=ctx.ro />
                <Pick
                    options=vec![("".into(), "любой протокол".into()), ("tcp".into(), "tcp".into()), ("icmp".into(), "icmp".into())]
                    value=proto
                    on_pick=Callback::new(move |v| proto.set(v))
                    disabled=ctx.ro
                />
                <TextIn value=src placeholder="откуда 192.168.0.0/24" disabled=ctx.ro />
                <TextIn value=dst placeholder="куда" disabled=ctx.ro />
                <TextIn value=port class="nl-prefix wide" digits=5 placeholder="порт" disabled=ctx.ro />
                <Pick
                    options=vec![
                        ("".into(), "любое состояние".into()),
                        ("NEW".into(), "новое соединение".into()),
                        ("ESTABLISHED,RELATED".into(), "уже установлено".into()),
                    ]
                    value=state
                    on_pick=Callback::new(move |v| state.set(v))
                    disabled=ctx.ro
                />
                <Btn label="+ правило" on_click=add disabled=ctx.ro />
            </div>
            <ol class="nl-rules">
                {move || rules.get().into_iter().enumerate().map(|(k, text)| view! {
                    <li>
                        <code>{text}</code>
                        {(!ctx.ro).then(|| view! {
                            <Cross label="Удалить правило" on_click=Callback::new(move |()| {
                                ctx.edit(|d| {
                                    if k < d.fw.rules.len() {
                                        d.fw.rules.remove(k);
                                    }
                                });
                            }) />
                        })}
                    </li>
                }).collect_view()}
                {move || rules.with(Vec::is_empty).then(|| view! { <li class="nl-none">{format!("правил нет — работает политика «{}»", policy.get())}</li> })}
            </ol>
            <Msg msg=msg />
        </div>
    }
}

/* ---- серверы и коммутаторы ---- */

/// Слушающие порты сервера.
#[component]
pub fn Services(ctx: Ctx) -> impl IntoView {
    let port = RwSignal::new(String::new());
    let proto = RwSignal::new("tcp".to_string());
    // (описание, привязан ли только к одному адресу)
    let rows = Memo::new(move |_| {
        ctx.read(|d| {
            d.services
                .iter()
                .map(|s| {
                    let local = s.bind.as_deref().is_some_and(|b| !b.is_empty() && b != "0.0.0.0");
                    let bind = if local { format!(" (только {})", s.bind.clone().unwrap_or_default()) } else { String::new() };
                    (format!("{}/{}{bind}", s.proto.as_str(), s.port), local)
                })
                .collect::<Vec<_>>()
        })
        .unwrap_or_default()
    });
    let add = Callback::new(move |()| {
        let Ok(p) = port.get_untracked().parse::<i64>() else { return };
        let proto = if proto.get_untracked() == "udp" { Proto::Udp } else { Proto::Tcp };
        ctx.edit(|d| d.services.push(Service { proto, port: p, bind: None, name: None }));
        port.set(String::new());
    });
    view! {
        <div class="nl-sec">
            <h4>"Слушающие порты"</h4>
            <ul class="nl-rules">
                {move || rows.get().into_iter().enumerate().map(|(k, (text, local))| view! {
                    <li>
                        <code>{text}</code>
                        {(!ctx.ro && local).then(|| view! {
                            <Btn label="слушать везде" on_click=Callback::new(move |()| {
                                ctx.edit(|d| {
                                    if let Some(s) = d.services.get_mut(k) {
                                        s.bind = Some("0.0.0.0".into());
                                    }
                                });
                            }) />
                        })}
                        {(!ctx.ro).then(|| view! {
                            <Cross label="Закрыть порт" on_click=Callback::new(move |()| {
                                ctx.edit(|d| {
                                    if k < d.services.len() {
                                        d.services.remove(k);
                                    }
                                });
                            }) />
                        })}
                    </li>
                }).collect_view()}
                {move || rows.with(Vec::is_empty).then(|| view! { <li class="nl-none">"ни один порт не слушает"</li> })}
            </ul>
            {(!ctx.ro).then(|| view! {
                <div class="nl-add">
                    <Pick options=same(&["tcp", "udp"]) value=proto on_pick=Callback::new(move |v| proto.set(v)) label="Протокол" />
                    <TextIn value=port class="nl-prefix wide" digits=5 placeholder="порт" />
                    <Btn label="+ слушать порт" on_click=add />
                </div>
            })}
        </div>
    }
}

/// Порты коммутатора: включение, VLAN и trunk.
#[component]
pub fn SwitchPorts(ctx: Ctx) -> impl IntoView {
    let names = Memo::new(move |_| iface_names(ctx));
    view! {
        <div class="nl-sec">
            <h4>"Порты"</h4>
            <table class="nl-table">
                <tbody>
                    <For each=move || names.get() key=|n| n.clone() children=move |name| view! { <SwitchPort ctx=ctx name=name /> } />
                </tbody>
            </table>
        </div>
    }
}

#[component]
fn SwitchPort(ctx: Ctx, name: String) -> impl IntoView {
    let up = {
        let n = name.clone();
        move || ctx.read(|d| d.iface(&n).map(|i| i.up)).flatten().unwrap_or(true)
    };
    let trunk = {
        let n = name.clone();
        Signal::derive(move || ctx.read(|d| d.iface(&n).map(|i| i.trunk)).flatten().unwrap_or(false))
    };
    let vlan_text = {
        let n = name.clone();
        move || {
            ctx.read(|d| d.iface(&n).map(|i| if i.trunk { String::new() } else { i.vlan.unwrap_or(1).to_string() })).flatten().unwrap_or_default()
        }
    };
    let (n_up, n_vlan, n_trunk) = (name.clone(), name.clone(), name.clone());
    view! {
        <tr>
            <td>{name.clone()}</td>
            <td>
                <Check
                    checked=Signal::derive(up)
                    on_change=Callback::new(move |on| {
                        ctx.edit(|d| set_up(d, &n_up, on));
                    })
                    label="вкл"
                    disabled=ctx.ro
                />
            </td>
            <td>
                <label class="nl-up">
                    "VLAN"
                    <input
                        class="nl-prefix"
                        prop:value=vlan_text.clone()
                        disabled=move || ctx.ro || trunk.get()
                        aria-label=format!("VLAN {name}")
                        on:input=move |e| {
                            let raw = event_target_value(&e);
                            let clean = logic::digits(&raw, 4);
                            let v: u32 = clean.parse().unwrap_or(0);
                            if v >= 1 {
                                ctx.edit(|d| {
                                    if let Some(i) = d.iface_mut(&n_vlan) {
                                        i.vlan = Some(v);
                                    }
                                });
                            }
                            // поле показывает то, что записано в сети (пустое и нулевое значение не принимаются)
                            event_target::<web_sys::HtmlInputElement>(&e).set_value(&vlan_text());
                        }
                    />
                </label>
            </td>
            <td>
                <Check
                    checked=trunk
                    on_change=Callback::new(move |on| {
                        ctx.edit(|d| {
                            if let Some(i) = d.iface_mut(&n_trunk) {
                                i.trunk = on;
                            }
                        });
                    })
                    label="trunk"
                    disabled=ctx.ro
                />
            </td>
        </tr>
    }
}

/// Таблица MAC-адресов коммутатора (то, чему он научился на проходящих кадрах).
#[component]
pub fn MacTable(ctx: Ctx) -> impl IntoView {
    let rows = Memo::new(move |_| {
        let id = ctx.id();
        ctx.lab.net.with(|n| n.rt.mac.get(&id).map(|m| m.iter().map(|(mac, port)| (mac.clone(), port.clone())).collect::<Vec<_>>()).unwrap_or_default())
    });
    view! {
        <div class="nl-sec">
            <h4>"Таблица MAC-адресов"</h4>
            <table class="nl-table">
                <tbody>
                    {move || rows.get().into_iter().map(|(mac, port)| view! { <tr><td>{mac}</td><td>{port}</td></tr> }).collect_view()}
                </tbody>
            </table>
            {move || rows.with(Vec::is_empty).then(|| view! {
                <p class="nl-none">"Пока пусто: коммутатор учится на проходящих кадрах. Запустите ping между компьютерами."</p>
            })}
        </div>
    }
}
