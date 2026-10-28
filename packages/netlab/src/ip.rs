//! IPv4 arithmetic: addresses are unsigned 32-bit numbers, subnets are "a.b.c.d/p".
//! A missing address (`None`) behaves as 0 in network computations, like `?? 0` in the original implementation.

/// Address from text "a.b.c.d" (no leading zeros); `None` if the text is not an address.
pub fn parse_ip(s: &str) -> Option<u32> {
    let s = s.trim();
    let mut n: u32 = 0;
    let mut count = 0;
    for part in s.split('.') {
        count += 1;
        if count > 4 || part.is_empty() || part.len() > 3 || !part.bytes().all(|b| b.is_ascii_digit()) {
            return None;
        }
        let o: u32 = part.parse().ok()?;
        if o > 255 || (part.len() > 1 && part.starts_with('0')) {
            return None;
        }
        n = n * 256 + o;
    }
    if count == 4 {
        Some(n)
    } else {
        None
    }
}

/// Address from an optional string.
pub fn parse_ip_opt(s: Option<&str>) -> Option<u32> {
    s.and_then(parse_ip)
}

/// Address text "a.b.c.d".
pub fn ip_str(n: u32) -> String {
    format!("{}.{}.{}.{}", n >> 24, (n >> 16) & 255, (n >> 8) & 255, n & 255)
}

/// Address text; missing is "0.0.0.0".
pub fn ip_str_opt(n: Option<u32>) -> String {
    ip_str(n.unwrap_or(0))
}

/// Mask of length `p` as a number (for `p` > 32 the shift is modulo 32, as in JavaScript).
pub fn mask_of(p: u32) -> u32 {
    if p == 0 {
        0
    } else {
        0xffff_ffffu32.wrapping_shl((32i32 - p as i32) as u32)
    }
}

/// "192.168.1.10/24" -> (address, prefix length).
pub fn parse_cidr(s: &str) -> Option<(u32, u32)> {
    let s = s.trim();
    let (a, p) = s.split_once('/')?;
    if a.is_empty() || !a.bytes().all(|b| b.is_ascii_digit() || b == b'.') {
        return None;
    }
    if p.is_empty() || p.len() > 2 || !p.bytes().all(|b| b.is_ascii_digit()) {
        return None;
    }
    let ip = parse_ip(a)?;
    let prefix: u32 = p.parse().ok()?;
    if prefix > 32 {
        return None;
    }
    Some((ip, prefix))
}

/// Mask "255.255.255.0" -> prefix length; `None` if the mask is non-contiguous.
pub fn prefix_of_mask(s: &str) -> Option<u32> {
    let n = parse_ip(s)?;
    (0..=32).find(|&p| mask_of(p) == n)
}

pub fn network_of(ip: Option<u32>, prefix: u32) -> u32 {
    ip.unwrap_or(0) & mask_of(prefix)
}

pub fn broadcast_of(ip: Option<u32>, prefix: u32) -> u32 {
    network_of(ip, prefix) | !mask_of(prefix)
}

/// Whether `ip` is within subnet `net/prefix`.
pub fn in_net(ip: Option<u32>, net: Option<u32>, prefix: u32) -> bool {
    network_of(ip, prefix) == network_of(net, prefix)
}

pub fn cidr_str(ip: Option<u32>, prefix: impl std::fmt::Display) -> String {
    format!("{}/{}", ip_str_opt(ip), prefix)
}

/// Subnet "a.b.c.d/p" from address and prefix.
pub fn net_str(ip: Option<u32>, prefix: u32) -> String {
    cidr_str(Some(network_of(ip, prefix)), prefix)
}

/// Private address (RFC 1918).
pub fn is_private(ip: Option<u32>) -> bool {
    in_net(ip, parse_ip("10.0.0.0"), 8) || in_net(ip, parse_ip("172.16.0.0"), 12) || in_net(ip, parse_ip("192.168.0.0"), 16)
}

/// Subnet "a.b.c.d/p", single address, "any" or absence -> (network, prefix).
pub fn parse_net(s: Option<&str>) -> Option<(u32, u32)> {
    match s {
        None | Some("any") | Some("0.0.0.0/0") => Some((0, 0)),
        Some(s) => {
            if let Some((ip, p)) = parse_cidr(s) {
                return Some((network_of(Some(ip), p), p));
            }
            parse_ip(s).map(|ip| (ip, 32))
        }
    }
}

/// Whether the address matches a subnet description (`None` in the description means "any"; unparsable means no).
pub fn in_net_str(ip: Option<u32>, spec: Option<&str>) -> bool {
    match parse_net(spec) {
        Some((net, p)) => in_net(ip, Some(net), p),
        None => false,
    }
}

/// MAC address from an ordinal number: 28:28:xx:xx:xx:xx.
pub fn mac_str(n: u32) -> String {
    format!("{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}", 40, 40, (n >> 24) & 255, (n >> 16) & 255, (n >> 8) & 255, n & 255)
}

/// Broadcast MAC.
pub const BCAST_MAC: &str = "ff:ff:ff:ff:ff:ff";

/// String looks like a MAC in the form "aa:bb:cc:dd:ee:ff".
pub fn is_mac(s: &str) -> bool {
    let parts: Vec<&str> = s.split(':').collect();
    parts.len() == 6 && parts.iter().all(|p| p.len() == 2 && p.bytes().all(|b| b.is_ascii_hexdigit()))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn address_parsing() {
        assert_eq!(parse_ip("10.0.0.1"), Some(0x0a00_0001));
        assert_eq!(parse_ip(" 10.0.0.1 "), Some(0x0a00_0001));
        assert_eq!(parse_ip("10.0.0.01"), None);
        assert_eq!(parse_ip("256.0.0.1"), None);
        assert_eq!(parse_ip("1.2.3"), None);
        assert_eq!(parse_ip("1.2.3.4.5"), None);
        assert_eq!(ip_str(0xc0a8_0101), "192.168.1.1");
    }

    #[test]
    fn subnets() {
        assert_eq!(parse_cidr("192.168.1.10/24"), Some((0xc0a8_010a, 24)));
        assert_eq!(parse_cidr("1.2.3.4/33"), None);
        assert_eq!(net_str(parse_ip("192.168.1.10"), 24), "192.168.1.0/24");
        assert_eq!(mask_of(0), 0);
        assert_eq!(mask_of(24), 0xffff_ff00);
        assert_eq!(prefix_of_mask("255.255.255.0"), Some(24));
        assert!(in_net_str(parse_ip("10.1.2.3"), Some("10.0.0.0/8")));
        assert!(is_private(parse_ip("172.20.0.1")));
        assert!(!is_private(parse_ip("172.32.0.1")));
        assert_eq!(parse_net(Some("10.1.2.3")), Some((0x0a01_0203, 32)));
    }

    #[test]
    fn mac() {
        assert_eq!(mac_str(1), "28:28:00:00:00:01");
        assert!(is_mac("28:28:00:00:00:01"));
    }
}
