//! Web page load over HTTP/1.1, HTTP/2 and HTTP/3: a per-round model. A page is HTML and N resources;
//! we count handshakes, the number of request "rounds", transfer over the bottleneck and the cost of losses:
//! h1 is six connections, h2 is one TCP (a loss stalls all streams), h3 is QUIC (streams are independent).

use crate::ip::*;
use crate::sim::udp1;
use crate::transfer::{path_info, PathInfo};
use crate::types::*;
use crate::util::{num_str, to_fixed};

/// Load conditions: RTT (us), link (Mbit/s), loss probability, number of resources, their size (KB), HTTPS.
#[derive(Clone, Debug)]
pub struct PageEnv {
    pub rtt: f64,
    pub rate: f64,
    pub loss_p: f64,
    pub count: f64,
    pub kb: f64,
    pub https: bool,
}

/// Page load time for one HTTP version, us.
#[derive(Clone, Debug)]
pub struct PageModel {
    pub proto: HttpProto,
    pub total: f64,
    pub setup: f64,
    pub rounds: f64,
    pub xfer: f64,
    pub loss: f64,
    pub l: f64,
}

pub fn page_model(env: &PageEnv, proto: HttpProto) -> PageModel {
    let PageEnv { rtt, rate, loss_p, count, kb, https } = *env;
    let bytes = (count + 1.0) * kb * 1024.0;
    let l = (bytes / 1460.0) * loss_p; // expected number of lost packets
    let tcp_setup = rtt; // SYN → SYN-ACK
    let tls_setup = if https { rtt } else { 0.0 }; // TLS 1.3: one more round trip
    let xfer = ((bytes * 8.0) / (rate * 1e6)) * 1e6; // us over the bottleneck
    let slow = 3.0 * rtt; // window ramp-up
    let (setup, rounds, loss) = match proto {
        HttpProto::H1 => (tcp_setup + tls_setup, 1.0 + (count / 6.0).ceil(), (l * rtt) / 6.0), // HTML, then resources six at a time
        HttpProto::H2 => (tcp_setup + tls_setup, 2.0, l * rtt), // HTML and all resources at once; a loss stalls all streams
        HttpProto::H3 => (rtt, 2.0, l * rtt * 0.15),            // QUIC: transport and encryption in one round trip
    };
    let total = setup + rounds * rtt + xfer + (if proto == HttpProto::H1 { slow * 1.5 } else { slow }) + loss;
    PageModel { proto, total, setup, rounds, xfer, loss, l }
}

/// Load measurement outcome.
#[derive(Clone, Debug)]
pub enum PageloadResult {
    Failed(String),
    Ok { want: HttpProto, used: HttpProto, note: String, chosen: PageModel, all: Vec<PageModel>, env: PageEnv, ip: String },
}

/// Measure page load from device `dev_id` to server `dst`.
pub fn pageload(state: &mut NetState, dev_id: &str, dst: u32, https: bool) -> PageloadResult {
    let info = path_info(state, dev_id, dst);
    let PathInfo::Ok { dst_id, rtt0, rate, loss_p, .. } = info else {
        return PageloadResult::Failed(i18n::tr("no connection to the server").into());
    };
    let http = dst_id.as_deref().and_then(|id| state.devices.get(id)).and_then(|d| d.http.clone());
    let Some(page) = http.as_ref().and_then(|h| h.page.clone()) else {
        return PageloadResult::Failed(i18n::tr("the server has no page to measure").into());
    };
    let want = http.as_ref().and_then(|h| h.protocol).unwrap_or(HttpProto::H1);
    let mut used = want;
    let mut note = String::new();
    if want == HttpProto::H3 {
        let u = udp1(state, dev_id, dst, 443, 50001);
        if u.status != ProbeStatus::Reply {
            used = HttpProto::H2;
            note = i18n::tr("UDP/443 to the server is blocked or nobody is listening — the browser fell back to HTTP/2").into();
        }
    }
    let env = PageEnv { rtt: rtt0, rate, loss_p, count: page.count, kb: page.kb, https };
    let all: Vec<PageModel> = [HttpProto::H1, HttpProto::H2, HttpProto::H3].iter().map(|p| page_model(&env, *p)).collect();
    let chosen = all.iter().find(|x| x.proto == used).cloned().unwrap_or_else(|| all[0].clone());
    PageloadResult::Ok { want, used, note, chosen, all, env, ip: ip_str(dst) }
}

/// Output of the `pageload` command.
pub fn fmt_page(r: &PageloadResult) -> String {
    match r {
        PageloadResult::Failed(e) => format!("pageload: {e}"),
        PageloadResult::Ok { want, used, note, chosen, all, env, .. } => {
            let s = |us: f64| to_fixed(us / 1e6, 2);
            let arrow = if note.is_empty() { String::new() } else { format!(" → {}", used.name()) };
            let mut l = vec![
                i18n::trf!("page: {0} resources of ~{1} KB · RTT {2} ms · link {3} Mbit/s · loss {4}%", num_str(env.count + 1.0), num_str(env.kb), to_fixed(env.rtt / 1000.0, 0), num_str(env.rate), to_fixed(env.loss_p * 100.0, 1)),
                i18n::trf!("server offers: {0}{1}", want.name(), arrow),
                i18n::trf!("load: {0} s (handshakes {1}, {2} request rounds, transfer {3}, loss {4})", s(chosen.total), s(chosen.setup), num_str(chosen.rounds), s(chosen.xfer), s(chosen.loss)),
                String::new(),
                i18n::tr("for comparison:").to_string(),
            ];
            for x in all {
                l.push(i18n::trf!("  {0} {1} s{2}", format!("{:<9}", x.proto.name()), s(x.total), if x.proto == *used { i18n::tr("   ← current") } else { "" }));
            }
            if !note.is_empty() {
                l.push(String::new());
                l.push(note.clone());
            }
            l.join("\n")
        }
    }
}
