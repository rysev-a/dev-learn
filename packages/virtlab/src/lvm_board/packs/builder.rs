//! Shared building blocks of the scenario packs: a board builder.

use super::super::{next_pos, Edge, Kind, Node, Param, Topology};

pub(crate) fn s(text: &str) -> String {
    text.to_string()
}

/// Board builder: objects get places by their kind, links are added by identifiers. Parameters that equal the default of the kind stay unset
/// (the data files and the drafts stay small, and a start board and a reference board do not differ by a parameter that merely repeats its default).
#[derive(Clone, Default)]
pub(crate) struct B {
    pub(crate) t: Topology,
}

impl B {
    fn put(&mut self, id: &str, kind: Kind, name: &str, params: &[(&str, &str)]) -> &mut Self {
        let (x, y) = next_pos(&self.t, kind);
        let mut n = Node::new(id, kind, name, x, y);
        for (key, value) in params {
            if n.param_text(key) != *value {
                n.params.insert((*key).into(), Param::Str((*value).into()));
            }
        }
        self.t.nodes.push(n);
        self
    }

    /// A disk of `gib` GiB.
    pub(crate) fn disk(&mut self, id: &str, name: &str, gib: u32) -> &mut Self {
        self.put(id, Kind::Disk, name, &[("size", &gib.to_string())])
    }

    /// A physical volume made of a disk.
    pub(crate) fn pv(&mut self, id: &str, name: &str, disk: &str) -> &mut Self {
        self.put(id, Kind::Pv, name, &[]).link(&[(disk, id)])
    }

    /// A volume group of the given extent size (MiB) with physical volumes.
    pub(crate) fn vg(&mut self, id: &str, name: &str, pe: u32, pvs: &[&str]) -> &mut Self {
        self.put(id, Kind::Vg, name, &[("pe", &pe.to_string())]);
        for pv in pvs {
            self.link(&[(pv, id)]);
        }
        self
    }

    /// A logical volume carved from a group.
    pub(crate) fn lv(&mut self, id: &str, name: &str, vg: &str, gib: u32, mirror: u32) -> &mut Self {
        self.put(id, Kind::Lv, name, &[("size", &gib.to_string()), ("mirror", &mirror.to_string())]).link(&[(vg, id)])
    }

    /// A thin pool carved from a group (`meta` MiB of metadata).
    pub(crate) fn pool(&mut self, id: &str, name: &str, vg: &str, gib: u32, meta: u32) -> &mut Self {
        self.put(id, Kind::ThinPool, name, &[("size", &gib.to_string()), ("meta", &meta.to_string())]).link(&[(vg, id)])
    }

    /// A thin volume of a pool.
    pub(crate) fn thin(&mut self, id: &str, name: &str, pool: &str, gib: u32) -> &mut Self {
        self.put(id, Kind::ThinLv, name, &[("size", &gib.to_string())]).link(&[(pool, id)])
    }

    /// A snapshot of a volume.
    pub(crate) fn snap(&mut self, id: &str, name: &str, origin: &str, gib: u32) -> &mut Self {
        self.put(id, Kind::Snapshot, name, &[("size", &gib.to_string())]).link(&[(origin, id)])
    }

    /// A filesystem on a volume.
    pub(crate) fn fs(&mut self, id: &str, name: &str, volume: &str, ty: &str, gib: u32) -> &mut Self {
        self.put(id, Kind::Fs, name, &[("type", ty), ("size", &gib.to_string())]).link(&[(volume, id)])
    }

    /// A VM whose disks are the given volumes.
    pub(crate) fn vm(&mut self, id: &str, name: &str, volumes: &[&str]) -> &mut Self {
        self.put(id, Kind::Vm, name, &[]);
        for v in volumes {
            self.link(&[(v, id)]);
        }
        self
    }

    /// Change a parameter of an object (to the default too: the parameter is then removed).
    pub(crate) fn param(&mut self, id: &str, key: &str, value: &str) -> &mut Self {
        let n = self.t.nodes.iter_mut().find(|n| n.id == id).expect("object");
        n.params.remove(key);
        if n.param_text(key) != value {
            n.params.insert(key.into(), Param::Str(value.into()));
        }
        self
    }

    pub(crate) fn link(&mut self, pairs: &[(&str, &str)]) -> &mut Self {
        for (a, b) in pairs {
            self.t.edges.push(Edge::new(a, b));
        }
        self
    }

    pub(crate) fn done(&self) -> Topology {
        self.t.clone()
    }
}

/// One 100 GiB disk in a group `vg` with the 50 GiB volume `data` and its filesystem.
pub(crate) fn one_disk() -> B {
    let mut b = B::default();
    b.disk("d1", "sda", 100).pv("pv1", "pv1", "d1").vg("vg", "vg0", 4, &["pv1"]).lv("data", "data", "vg", 50, 1).fs(
        "fs-data", "ext4", "data", "ext4", 50,
    );
    b
}

#[cfg(test)]
mod tests {
    use super::super::super::{evaluate, problems, VolStatus, Workload};
    use super::*;

    #[test]
    fn the_helpers_build_valid_boards_and_leave_defaults_unset() {
        let b = one_disk();
        let t = b.done();
        assert!(problems(&t).is_empty(), "{:?}", problems(&t).into_iter().map(|p| p.text).collect::<Vec<_>>());
        assert_eq!(t.node("d1").map(|n| n.params.len()), Some(0), "100 GiB is the default size of a disk");
        assert_eq!(t.node("vg").map(|n| n.params.len()), Some(0), "4 MiB is the default extent size");
        assert_eq!(t.node("data").map(|n| n.params.len()), Some(1), "50 GiB differs from 10, one copy is the default");
        let ev = evaluate(&t, &Workload::default());
        assert_eq!(ev.volume("data").map(|v| v.status), Some(VolStatus::Ok));
        for (i, a) in t.nodes.iter().enumerate() {
            for n in &t.nodes[i + 1..] {
                assert!((a.x - n.x).abs() >= 92.0 || (a.y - n.y).abs() >= 60.0, "{} and {}", a.id, n.id);
            }
        }
    }
}
