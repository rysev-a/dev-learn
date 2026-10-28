//! Формы служб в карточке устройства: веб-сервер, TLS и хранилище доверия, прокси, балансировщик, обратный прокси, SSH,
//! VPN, DNS (клиент и сервер) и настройки TCP. Показываются по флагам `tools` упражнения и по тому, какие службы
//! запущены на устройстве. Меняют сеть командами терминала или напрямую — как и в React-версии.

use leptos::prelude::*;
use netlab::types::{Cc, HttpProto, LbAlgo};
use netlab::util::num_str;

use super::forms::{same, Btn, Check, Cross, Ctx, Msg, Pick, Section, TextIn};
use super::logic;

/// Адреса и удостоверяющие центры сети (имена для выпадающих списков).
fn authorities(ctx: Ctx) -> Vec<String> {
    ctx.lab.net.with(|n| n.pki.as_ref().map(|p| p.cas.keys().cloned().collect()).unwrap_or_default())
}

fn options(values: &[String]) -> Vec<(String, String)> {
    values.iter().map(|v| (v.clone(), v.clone())).collect()
}

/// Веб-сервер: протокол HTTP, маршруты и заголовки.
#[component]
pub fn WebServer(ctx: Ctx) -> impl IntoView {
    let path = RwSignal::new(String::new());
    let status = RwSignal::new("200".to_string());
    let extra = RwSignal::new(String::new());
    let hp = RwSignal::new(String::new());
    let hn = RwSignal::new(String::new());
    let hv = RwSignal::new(String::new());
    let msg = RwSignal::new(String::new());
    let page = Memo::new(move |_| ctx.read(|d| d.http.as_ref().and_then(|h| h.page.as_ref()).map(|p| (p.count, p.kb))).flatten());
    let proto = Signal::derive(move || ctx.read(|d| d.http.as_ref().and_then(|h| h.protocol).unwrap_or(HttpProto::H1).id().to_string()).unwrap_or_default());
    let routes = Memo::new(move |_| {
        ctx.read(|d| {
            d.http
                .as_ref()
                .map(|h| {
                    h.routes
                        .iter()
                        .map(|r| {
                            let mut info = r.location.as_ref().map(|l| format!("→ {l}")).unwrap_or_default();
                            if !r.headers.is_empty() {
                                info.push_str(&r.headers.iter().map(|(n, v)| format!(" {n}: {v}")).collect::<Vec<_>>().join(";"));
                            }
                            (r.path.clone(), r.status.unwrap_or(200), info)
                        })
                        .collect::<Vec<_>>()
                })
                .unwrap_or_default()
        })
        .unwrap_or_default()
    });
    let add_route = Callback::new(move |()| {
        let st: u32 = status.get_untracked().parse().unwrap_or(0);
        msg.set(ctx.exec(&logic::web_route_command(&path.get_untracked(), st, &extra.get_untracked())));
    });
    let add_header = Callback::new(move |()| {
        msg.set(ctx.exec(&format!("web header {} {} {}", hp.get_untracked(), hn.get_untracked(), hv.get_untracked())));
    });
    let protocols = vec![("h1".to_string(), "HTTP/1.1".to_string()), ("h2".to_string(), "HTTP/2".to_string()), ("h3".to_string(), "HTTP/3".to_string())];
    view! {
        <div class="nl-sec">
            <h4>{i18n::tr("Web server (HTTP, port 80)")}</h4>
            {move || page.get().map(|(count, kb)| view! {
                <div class="nl-add">
                    <span class="nl-lbl">{i18n::tr("protocol")}</span>
                    <Pick
                        options=protocols.clone()
                        value=proto
                        disabled=ctx.ro
                        on_pick=Callback::new(move |v: String| {
                            let p = match v.as_str() {
                                "h2" => HttpProto::H2,
                                "h3" => HttpProto::H3,
                                _ => HttpProto::H1,
                            };
                            ctx.edit(|d| {
                                if let Some(h) = d.http.as_mut() {
                                    h.protocol = Some(p);
                                }
                            });
                        })
                    />
                    <span class="nl-lbl">{i18n::trf!("page: {0} resources of ~{1} KB", num_str(count + 1.0), num_str(kb))}</span>
                </div>
            })}
            <table class="nl-table">
                <tbody>
                    {move || routes.get().into_iter().enumerate().map(|(k, (p, st, info))| view! {
                        <tr>
                            <td>{p}</td>
                            <td>{st}</td>
                            <td>{info}</td>
                            <td>
                                {(!ctx.ro).then(|| view! {
                                    <Cross label=i18n::tr("Delete route") on_click=Callback::new(move |()| {
                                        ctx.edit(|d| {
                                            if let Some(h) = d.http.as_mut() {
                                                if k < h.routes.len() {
                                                    h.routes.remove(k);
                                                }
                                            }
                                        });
                                    }) />
                                })}
                            </td>
                        </tr>
                    }).collect_view()}
                </tbody>
            </table>
            {(!ctx.ro).then(|| view! {
                <div class="nl-add">
                    <TextIn value=path placeholder=i18n::tr("/path") />
                    <TextIn value=status class="nl-prefix wide" digits=3 label=i18n::tr("Status code") />
                    <TextIn value=extra placeholder=i18n::tr("text or /target (for 30x)") />
                    <Btn label=i18n::tr("+ route") on_click=add_route />
                </div>
                <div class="nl-add">
                    <TextIn value=hp placeholder=i18n::tr("for path /logo.png") />
                    <TextIn value=hn placeholder=i18n::tr("Cache-Control header name") />
                    <TextIn value=hv placeholder=i18n::tr("value max-age=3600") />
                    <Btn label=i18n::tr("+ header") on_click=add_header />
                </div>
            })}
            <Msg msg=msg />
        </div>
    }
}

/// TLS-сертификат сервера: выпуск, цепочка и версии протокола.
#[component]
pub fn TlsServer(ctx: Ctx) -> impl IntoView {
    let cas = authorities(ctx);
    let cn = RwSignal::new(String::new());
    let issuer = RwSignal::new("PublicIntCA".to_string());
    let days = RwSignal::new("90".to_string());
    let chain = RwSignal::new("PublicIntCA".to_string());
    let msg = RwSignal::new(String::new());
    let about = Memo::new(move |_| {
        ctx.read(|d| {
            d.tls.as_ref().map(|t| {
                (
                    format!("CN={} · SAN: {}", t.cert.cn, t.cert.san.join(", ")),
                    i18n::trf!("issuer {0} · until {1}", t.cert.issuer, t.cert.not_after),
                    i18n::trf!("chain: {0} · TLS versions {1}", if t.chain.is_empty() { i18n::tr("(own certificate only)").to_string() } else { t.chain.join(" → ") }, t.versions.join(", ")),
                )
            })
        })
        .flatten()
    });
    let versions = Memo::new(move |_| ctx.read(|d| d.tls.as_ref().map(|t| t.versions.clone()).unwrap_or_default()).unwrap_or_default());
    let issue = Callback::new(move |()| {
        msg.set(ctx.exec(&format!("tls cert new {} --issuer {} --days {}", cn.get_untracked(), issuer.get_untracked(), days.get_untracked())));
    });
    let chain_add = Callback::new(move |()| msg.set(ctx.exec(&format!("tls chain add {}", chain.get_untracked()))));
    let chain_clear = Callback::new(move |()| msg.set(ctx.exec("tls chain clear")));
    let version_boxes = ["1.0", "1.1", "1.2", "1.3"]
        .into_iter()
        .map(|v| {
            view! {
                <Check
                    checked=Signal::derive(move || versions.with(|l| l.iter().any(|x| x == v)))
                    on_change=Callback::new(move |on| {
                        ctx.edit(|d| {
                            if let Some(t) = d.tls.as_mut() {
                                t.versions = logic::toggle_tls_version(&t.versions, v, on);
                            }
                        });
                    })
                    label=v
                />
            }
        })
        .collect_view();
    view! {
        <div class="nl-sec">
            <h4>{i18n::tr("TLS certificate")}</h4>
            {move || about.get().map(|(a, b, c)| view! { <p class="nl-none">{a}<br />{b}<br />{c}</p> })}
            {(!ctx.ro).then(|| view! {
                <div class="nl-add">
                    <TextIn value=cn placeholder=i18n::tr("names separated by spaces: example.org www.example.org") />
                    <Pick options=options(&cas) value=issuer on_pick=Callback::new(move |v| issuer.set(v)) />
                    <TextIn value=days class="nl-prefix wide" digits=5 label=i18n::tr("Days") />
                    <Btn label=i18n::tr("issue") on_click=issue />
                </div>
                <div class="nl-add">
                    <span class="nl-lbl">{i18n::tr("to chain:")}</span>
                    <Pick options=options(&cas) value=chain on_pick=Callback::new(move |v| chain.set(v)) />
                    <Btn label=i18n::tr("+ add") on_click=chain_add />
                    <Btn label=i18n::tr("clear") on_click=chain_clear />
                </div>
                <div class="nl-add">
                    <span class="nl-lbl">{i18n::tr("versions:")}</span>
                    {version_boxes}
                </div>
            })}
            <Msg msg=msg />
        </div>
    }
}

/// Хранилище доверия (корневые центры сертификации) клиента.
#[component]
pub fn TrustStore(ctx: Ctx) -> impl IntoView {
    let cas = authorities(ctx);
    let trust = Memo::new(move |_| ctx.read(|d| d.trust.clone().unwrap_or_else(|| vec!["PublicRootCA".to_string()])).unwrap_or_default());
    let first_free = cas.iter().find(|c| !trust.get_untracked().contains(c)).or_else(|| cas.first()).cloned().unwrap_or_default();
    let pick = RwSignal::new(first_free);
    view! {
        <div class="nl-sec">
            <h4>{i18n::tr("Trust store (root CAs)")}</h4>
            <ul class="nl-rules">
                {move || trust.get().into_iter().map(|c| {
                    let name = c.clone();
                    view! {
                        <li>
                            <code>{c}</code>
                            {(!ctx.ro).then(|| view! {
                                <Cross label=i18n::tr("Remove") on_click=Callback::new(move |()| {
                                    let name = name.clone();
                                    ctx.edit(|d| {
                                        let cur = d.trust.clone().unwrap_or_else(|| vec!["PublicRootCA".to_string()]);
                                        d.trust = Some(cur.into_iter().filter(|x| *x != name).collect());
                                    });
                                }) />
                            })}
                        </li>
                    }
                }).collect_view()}
            </ul>
            {(!ctx.ro).then(|| view! {
                <div class="nl-add">
                    <Pick options=options(&cas) value=pick on_pick=Callback::new(move |v| pick.set(v)) />
                    <Btn label=i18n::tr("+ trust") on_click=Callback::new(move |()| {
                        let add = pick.get_untracked();
                        ctx.edit(|d| {
                            let mut cur = d.trust.clone().unwrap_or_else(|| vec!["PublicRootCA".to_string()]);
                            if !add.is_empty() && !cur.contains(&add) {
                                cur.push(add);
                            }
                            d.trust = Some(cur);
                        });
                    }) />
                </div>
            })}
        </div>
    }
}

/// HTTP-прокси: список запрещённых хостов.
#[component]
pub fn ProxyBox(ctx: Ctx) -> impl IntoView {
    let host = RwSignal::new(String::new());
    let msg = RwSignal::new(String::new());
    let port = Memo::new(move |_| ctx.read(|d| d.proxy.as_ref().and_then(|p| p.port).unwrap_or(3128)).unwrap_or(3128));
    let deny = Memo::new(move |_| ctx.read(|d| d.proxy.as_ref().map(|p| p.deny.clone()).unwrap_or_default()).unwrap_or_default());
    view! {
        <div class="nl-sec">
            <h4>{move || i18n::trf!("HTTP proxy (tcp/{0})", port.get())}</h4>
            <ul class="nl-rules">
                {move || deny.get().into_iter().enumerate().map(|(k, h)| view! {
                    <li>
                        <code>{i18n::trf!("blocked: {0}", h)}</code>
                        {(!ctx.ro).then(|| view! {
                            <Cross label=i18n::tr("Allow") on_click=Callback::new(move |()| {
                                ctx.edit(|d| {
                                    if let Some(p) = d.proxy.as_mut() {
                                        if k < p.deny.len() {
                                            p.deny.remove(k);
                                        }
                                    }
                                });
                            }) />
                        })}
                    </li>
                }).collect_view()}
                {move || deny.with(Vec::is_empty).then(|| view! { <li class="nl-none">{i18n::tr("nothing blocked")}</li> })}
            </ul>
            {(!ctx.ro).then(|| view! {
                <div class="nl-add">
                    <TextIn value=host placeholder=i18n::tr("host to block: social.example") />
                    <Btn label=i18n::tr("+ block") on_click=Callback::new(move |()| {
                        msg.set(ctx.exec(&format!("proxy deny {}", host.get_untracked())));
                        host.set(String::new());
                    }) />
                </div>
            })}
            <Msg msg=msg />
        </div>
    }
}

/// Балансировщик нагрузки: алгоритм, проверка здоровья и пул серверов.
#[component]
pub fn LbBox(ctx: Ctx) -> impl IntoView {
    let addr = RwSignal::new(String::new());
    let msg = RwSignal::new(String::new());
    let title = Memo::new(move |_| ctx.read(|d| d.lb.as_ref().map(|l| i18n::trf!("Load balancer {0}:{1}", l.vip, l.port))).flatten().unwrap_or_default());
    let algo = Signal::derive(move || {
        ctx.read(|d| match d.lb.as_ref().and_then(|l| l.algo) {
            Some(LbAlgo::Hash) => "hash",
            _ => "rr",
        })
        .unwrap_or("rr")
        .to_string()
    });
    let health = Signal::derive(move || ctx.read(|d| d.lb.as_ref().is_some_and(|l| l.health)).unwrap_or(false));
    let backends = Memo::new(move |_| ctx.read(|d| d.lb.as_ref().map(|l| l.backends.iter().map(|b| format!("{}:{}", b.ip, b.port)).collect::<Vec<_>>()).unwrap_or_default()).unwrap_or_default());
    view! {
        <div class="nl-sec">
            <h4>{move || title.get()}</h4>
            <div class="nl-add">
                <span class="nl-lbl">{i18n::tr("algorithm")}</span>
                <Pick
                    options=vec![("rr".to_string(), i18n::tr("round robin").to_string()), ("hash".to_string(), i18n::tr("sticky by client address").to_string())]
                    value=algo
                    disabled=ctx.ro
                    on_pick=Callback::new(move |v: String| {
                        let a = if v == "hash" { LbAlgo::Hash } else { LbAlgo::Rr };
                        ctx.edit(|d| {
                            if let Some(l) = d.lb.as_mut() {
                                l.algo = Some(a);
                            }
                        });
                    })
                />
                <Check
                    checked=health
                    on_change=Callback::new(move |on| {
                        ctx.edit(|d| {
                            if let Some(l) = d.lb.as_mut() {
                                l.health = on;
                            }
                        });
                    })
                    label=i18n::tr("health check")
                    disabled=ctx.ro
                />
            </div>
            <ul class="nl-rules">
                {move || backends.get().into_iter().enumerate().map(|(k, b)| view! {
                    <li>
                        <code>{b}</code>
                        {(!ctx.ro).then(|| view! {
                            <Cross label=i18n::tr("Remove from pool") on_click=Callback::new(move |()| {
                                ctx.edit(|d| {
                                    if let Some(l) = d.lb.as_mut() {
                                        if k < l.backends.len() {
                                            l.backends.remove(k);
                                        }
                                    }
                                });
                            }) />
                        })}
                    </li>
                }).collect_view()}
            </ul>
            {(!ctx.ro).then(|| view! {
                <div class="nl-add">
                    <TextIn value=addr placeholder=i18n::tr("server for the pool 10.0.1.12:80") />
                    <Btn label=i18n::tr("+ to pool") on_click=Callback::new(move |()| {
                        msg.set(ctx.exec(&format!("lb add {}", addr.get_untracked())));
                        addr.set(String::new());
                    }) />
                </div>
            })}
            <Msg msg=msg />
        </div>
    }
}

/// Обратный прокси и кэш: правила «хост и путь → сервер».
#[component]
pub fn RproxyBox(ctx: Ctx) -> impl IntoView {
    let host = RwSignal::new("*".to_string());
    let path = RwSignal::new(String::new());
    let backend = RwSignal::new(String::new());
    let msg = RwSignal::new(String::new());
    // (что совпадает, куда, кэшируется ли)
    let rules = Memo::new(move |_| {
        ctx.read(|d| {
            d.rproxy
                .as_ref()
                .map(|p| {
                    p.rules
                        .iter()
                        .map(|r| (format!("{}{}", r.host.as_deref().unwrap_or("*"), r.path.as_deref().unwrap_or("")), format!("→ {}", r.backend), r.cache))
                        .collect::<Vec<_>>()
                })
                .unwrap_or_default()
        })
        .unwrap_or_default()
    });
    view! {
        <div class="nl-sec">
            <h4>{i18n::tr("Reverse proxy / cache")}</h4>
            <table class="nl-table">
                <tbody>
                    {move || rules.get().into_iter().enumerate().map(|(k, (what, to, cache))| view! {
                        <tr>
                            <td>{what}</td>
                            <td>{to}</td>
                            <td>
                                <Check
                                    checked=cache
                                    on_change=Callback::new(move |on| {
                                        ctx.edit(|d| {
                                            if let Some(r) = d.rproxy.as_mut().and_then(|p| p.rules.get_mut(k)) {
                                                r.cache = on;
                                            }
                                        });
                                    })
                                    label=i18n::tr("cache")
                                    disabled=ctx.ro
                                />
                            </td>
                            <td>
                                {(!ctx.ro).then(|| view! {
                                    <Cross label=i18n::tr("Delete rule") on_click=Callback::new(move |()| {
                                        ctx.edit(|d| {
                                            if let Some(p) = d.rproxy.as_mut() {
                                                if k < p.rules.len() {
                                                    p.rules.remove(k);
                                                }
                                            }
                                        });
                                    }) />
                                })}
                            </td>
                        </tr>
                    }).collect_view()}
                </tbody>
            </table>
            {(!ctx.ro).then(|| view! {
                <div class="nl-add">
                    <TextIn value=host class="nl-prefix wide" label=i18n::tr("Host") />
                    <TextIn value=path placeholder=i18n::tr("/path") />
                    <TextIn value=backend placeholder=i18n::tr("server 10.0.2.10:8080") />
                    <Btn label=i18n::tr("+ rule") on_click=Callback::new(move |()| {
                        let h = host.get_untracked();
                        msg.set(ctx.exec(&format!("rproxy add {} {} {}", if h.is_empty() { "*" } else { &h }, path.get_untracked(), backend.get_untracked())));
                        path.set(String::new());
                        backend.set(String::new());
                    }) />
                </div>
            })}
            <Msg msg=msg />
        </div>
    }
}

/// SSH: ключ хоста и пользователи сервера, ключ клиента.
#[component]
pub fn SshBox(ctx: Ctx) -> impl IntoView {
    let msg = RwSignal::new(String::new());
    let is_server = Memo::new(move |_| ctx.read(|d| d.ssh.is_some()).unwrap_or(false));
    let host_key = Memo::new(move |_| ctx.read(|d| d.ssh.as_ref().map(|s| s.host_key.clone())).flatten().unwrap_or_default());
    let password = Signal::derive(move || ctx.read(|d| d.ssh.as_ref().is_some_and(|s| s.password_auth)).unwrap_or(false));
    let users = Memo::new(move |_| {
        ctx.read(|d| {
            d.ssh
                .as_ref()
                .map(|s| s.users.iter().map(|(u, v)| format!("{u}: {}", if v.keys.is_empty() { i18n::tr("no keys").to_string() } else { v.keys.join(", ") })).collect::<Vec<_>>())
                .unwrap_or_default()
        })
        .unwrap_or_default()
    });
    let key = Memo::new(move |_| ctx.read(|d| d.ssh_key.clone()).flatten().unwrap_or_else(|| i18n::tr("no key").to_string()));
    view! {
        <div class="nl-sec">
            <h4>{move || format!("SSH {}", if is_server.get() { i18n::tr("server") } else { i18n::tr("client") })}</h4>
            {move || is_server.get().then(|| view! {
                <p class="nl-none">{i18n::trf!("host key: {0}", host_key.get())}</p>
                <Check
                    checked=password
                    on_change=Callback::new(move |on| {
                        ctx.edit(|d| {
                            if let Some(s) = d.ssh.as_mut() {
                                s.password_auth = on;
                            }
                        });
                    })
                    label=i18n::tr("allow password login")
                    disabled=ctx.ro
                />
                <ul class="nl-rules">
                    {move || users.get().into_iter().map(|u| view! { <li><code>{u}</code></li> }).collect_view()}
                </ul>
            })}
            <div class="nl-add">
                <span class="nl-lbl">{move || i18n::trf!("your key fingerprint: {0}", key.get())}</span>
                {move || (!is_server.get() && !ctx.ro).then(|| view! {
                    <Btn label=i18n::tr("generate key") on_click=Callback::new(move |()| msg.set(ctx.exec("ssh-keygen"))) />
                })}
            </div>
            <Msg msg=msg />
        </div>
    }
}

/// VPN-туннели: список и добавление.
#[component]
pub fn VpnBox(ctx: Ctx) -> impl IntoView {
    let name = RwSignal::new("wg0".to_string());
    let peer = RwSignal::new(String::new());
    let addr = RwSignal::new(String::new());
    let key = RwSignal::new(String::new());
    let msg = RwSignal::new(String::new());
    // (имя интерфейса, описание)
    let tunnels = Memo::new(move |_| {
        ctx.read(|d| {
            d.ifaces
                .iter()
                .filter_map(|i| {
                    let t = i.tun.as_ref()?;
                    Some((i.name.clone(), format!("{}: {}/{} ↔ {}", i.name, i.ip.clone().unwrap_or_default(), i.prefix, t.peer)))
                })
                .collect::<Vec<_>>()
        })
        .unwrap_or_default()
    });
    view! {
        <div class="nl-sec">
            <h4>{i18n::tr("VPN tunnels")}</h4>
            <ul class="nl-rules">
                {move || tunnels.get().into_iter().map(|(n, text)| view! {
                    <li>
                        <code>{text}</code>
                        {(!ctx.ro).then(|| view! {
                            <Cross label=i18n::tr("Delete tunnel") on_click=Callback::new(move |()| msg.set(ctx.exec(&format!("vpn del {n}")))) />
                        })}
                    </li>
                }).collect_view()}
                {move || tunnels.with(Vec::is_empty).then(|| view! { <li class="nl-none">{i18n::tr("no tunnels")}</li> })}
            </ul>
            {(!ctx.ro).then(|| view! {
                <div class="nl-add wrap">
                    <TextIn value=name class="nl-prefix wide" label=i18n::tr("Name") />
                    <TextIn value=peer placeholder=i18n::tr("peer public IP") />
                    <TextIn value=addr placeholder=i18n::tr("address 10.9.0.1/30") />
                    <TextIn value=key placeholder=i18n::tr("shared secret") />
                    <Btn label=i18n::tr("+ tunnel") on_click=Callback::new(move |()| {
                        msg.set(ctx.exec(&format!(
                            "vpn add {} --peer {} --address {} --key {}",
                            name.get_untracked(),
                            peer.get_untracked(),
                            addr.get_untracked(),
                            key.get_untracked()
                        )));
                    }) />
                </div>
            })}
            <Msg msg=msg />
        </div>
    }
}

/// DNS-клиент: адрес сервера имён (resolv.conf).
#[component]
pub fn Resolver(ctx: Ctx) -> impl IntoView {
    let value = RwSignal::new(ctx.read(|d| d.resolver.clone()).flatten().unwrap_or_default());
    let err = RwSignal::new(String::new());
    let commit = Callback::new(move |()| {
        if ctx.ro {
            return;
        }
        err.set(String::new());
        if let Some(Some(e)) = ctx.edit(|d| logic::commit_resolver(d, &value.get_untracked())) {
            err.set(e);
        }
    });
    view! {
        <div class="nl-sec">
            <label class="nl-field">
                <span>{i18n::tr("DNS server (/etc/resolv.conf: nameserver)")}</span>
                <TextIn value=value placeholder=i18n::tr("for example 192.168.0.53") disabled=ctx.ro on_commit=commit />
                <Msg msg=err />
            </label>
        </div>
    }
}

/// DNS-сервер: записи, делегирование зон, корневой сервер резолвера.
#[component]
pub fn DnsServer(ctx: Ctx) -> impl IntoView {
    let name = RwSignal::new(String::new());
    let typ = RwSignal::new("A".to_string());
    let val = RwSignal::new(String::new());
    let zone = RwSignal::new(String::new());
    let ns = RwSignal::new(String::new());
    let msg = RwSignal::new(String::new());
    let recursive = Memo::new(move |_| ctx.read(|d| d.dns.as_ref().is_some_and(|x| x.recursive)).unwrap_or(false));
    let zones = Memo::new(move |_| {
        ctx.read(|d| d.dns.as_ref().map(|x| x.zones.iter().map(|z| if z.is_empty() { i18n::tr("root").to_string() } else { z.clone() }).collect::<Vec<_>>().join(", ")).unwrap_or_default())
            .unwrap_or_default()
    });
    let root = ctx.read(|d| d.dns.as_ref().and_then(|x| x.roots.first().cloned())).flatten().unwrap_or_default();
    let root = RwSignal::new(root);
    let records = Memo::new(move |_| {
        ctx.read(|d| d.dns.as_ref().map(|x| x.records.iter().map(|r| (r.name.clone(), r.typ.clone(), r.value.clone())).collect::<Vec<_>>()).unwrap_or_default()).unwrap_or_default()
    });
    let delegations = Memo::new(move |_| {
        ctx.read(|d| d.dns.as_ref().map(|x| x.delegations.iter().map(|r| (r.zone.clone(), r.ns.clone())).collect::<Vec<_>>()).unwrap_or_default()).unwrap_or_default()
    });
    view! {
        <div class="nl-sec">
            <h4>{move || i18n::trf!("DNS server {0}", if recursive.get() { i18n::tr("(recursive resolver)") } else { i18n::tr("(authoritative)") })}</h4>
            {move || {
                let z = zones.get();
                (!z.is_empty()).then(|| view! { <p class="nl-none">{i18n::trf!("zones: {0}", z)}</p> })
            }}
            {move || recursive.get().then(|| view! {
                <div class="nl-add">
                    <span class="nl-lbl">{i18n::tr("root server")}</span>
                    <TextIn
                        value=root
                        placeholder="198.41.0.4"
                        disabled=ctx.ro
                        on_commit=Callback::new(move |()| {
                            let r = root.get_untracked();
                            if !r.trim().is_empty() {
                                msg.set(ctx.exec(&format!("dns root {}", r.trim())));
                            }
                        })
                    />
                </div>
            })}
            <table class="nl-table">
                <tbody>
                    {move || records.get().into_iter().enumerate().map(|(k, (n, t, v))| view! {
                        <tr>
                            <td>{n}</td>
                            <td>{t}</td>
                            <td>{v}</td>
                            <td>
                                {(!ctx.ro).then(|| view! {
                                    <Cross label=i18n::tr("Delete record") on_click=Callback::new(move |()| {
                                        ctx.edit(|d| {
                                            if let Some(x) = d.dns.as_mut() {
                                                if k < x.records.len() {
                                                    x.records.remove(k);
                                                }
                                            }
                                        });
                                    }) />
                                })}
                            </td>
                        </tr>
                    }).collect_view()}
                    {move || delegations.get().into_iter().enumerate().map(|(k, (z, n))| view! {
                        <tr>
                            <td>{z}</td>
                            <td>"NS →"</td>
                            <td>{n}</td>
                            <td>
                                {(!ctx.ro).then(|| view! {
                                    <Cross label=i18n::tr("Remove delegation") on_click=Callback::new(move |()| {
                                        ctx.edit(|d| {
                                            if let Some(x) = d.dns.as_mut() {
                                                if k < x.delegations.len() {
                                                    x.delegations.remove(k);
                                                }
                                            }
                                        });
                                    }) />
                                })}
                            </td>
                        </tr>
                    }).collect_view()}
                </tbody>
            </table>
            {move || (!ctx.ro && !recursive.get()).then(|| view! {
                <div class="nl-add">
                    <TextIn value=name placeholder=i18n::tr("name shop.example.org") />
                    <Pick options=same(&["A", "CNAME", "MX", "TXT"]) value=typ on_pick=Callback::new(move |v| typ.set(v)) />
                    <TextIn value=val placeholder=i18n::tr("value") />
                    <Btn label=i18n::tr("+ record") on_click=Callback::new(move |()| {
                        msg.set(ctx.exec(&format!("dns add {} {} {}", name.get_untracked(), typ.get_untracked(), val.get_untracked())));
                        name.set(String::new());
                        val.set(String::new());
                    }) />
                </div>
                <div class="nl-add">
                    <TextIn value=zone placeholder=i18n::tr("delegate zone example.org") />
                    <TextIn value=ns placeholder=i18n::tr("to server 198.51.100.30") />
                    <Btn label=i18n::tr("+ delegation") on_click=Callback::new(move |()| {
                        msg.set(ctx.exec(&format!("dns delegate {} {}", zone.get_untracked(), ns.get_untracked())));
                        zone.set(String::new());
                        ns.set(String::new());
                    }) />
                </div>
            })}
            <Msg msg=msg />
        </div>
    }
}

/// Настройки TCP: окно приёма и алгоритм управления перегрузкой.
#[component]
pub fn TcpTune(ctx: Ctx) -> impl IntoView {
    let window = RwSignal::new(ctx.read(|d| d.rwnd).flatten().unwrap_or(64).to_string());
    let cc = Signal::derive(move || ctx.read(|d| d.cc.unwrap_or(Cc::Cubic).as_str().to_string()).unwrap_or_default());
    let commit = Callback::new(move |()| {
        let w: u32 = window.get_untracked().parse().unwrap_or(0);
        if w >= 4 {
            ctx.edit(|d| d.rwnd = Some(w));
        }
    });
    view! {
        <Section title=i18n::tr("TCP settings")>
            <div class="nl-add">
                <span class="nl-lbl">{i18n::tr("Receive window, KB")}</span>
                <TextIn value=window class="nl-prefix wide" digits=6 disabled=ctx.ro label=i18n::tr("Receive window") on_commit=commit />
                <span class="nl-lbl">{i18n::tr("algorithm")}</span>
                <Pick
                    options=same(&["reno", "cubic", "bbr"])
                    value=cc
                    disabled=ctx.ro
                    on_pick=Callback::new(move |v: String| {
                        let c = match v.as_str() {
                            "reno" => Cc::Reno,
                            "bbr" => Cc::Bbr,
                            _ => Cc::Cubic,
                        };
                        ctx.edit(|d| d.cc = Some(c));
                    })
                />
            </div>
        </Section>
    }
}
