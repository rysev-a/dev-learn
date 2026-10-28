#!/bin/sh
# Builds /opt/ext/externs: one `--extern name=path` line per direct crate of the /opt/deps project
# (exactly the rlibs cargo used to build the root crate: dependencies may have two builds with different features).
set -eu
cd /opt/deps
mkdir -p /opt/ext
touch src/lib.rs
cargo build --release -v 2>&1 | grep -- '--crate-name deps' | grep -o -- '--extern [^ ]*' | grep -v 'extern deps=' | sed 's/--extern //; s/^/--extern /' | sed 's/`$//' | sed 's/\.rmeta$/.rlib/' | sort -u > /opt/ext/externs
cat /opt/ext/externs
