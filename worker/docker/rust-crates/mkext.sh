#!/bin/sh
# Строит /opt/ext/externs: по строке `--extern имя=путь` на каждый прямой крейт проекта /opt/deps
# (ровно те rlib, с которыми cargo собирал корневой крейт: у зависимостей бывает по две сборки с разными фичами).
set -eu
cd /opt/deps
mkdir -p /opt/ext
touch src/lib.rs
cargo build --release -v 2>&1 | grep -- '--crate-name deps' | grep -o -- '--extern [^ ]*' | grep -v 'extern deps=' | sed 's/--extern //; s/^/--extern /' | sed 's/`$//' | sed 's/\.rmeta$/.rlib/' | sort -u > /opt/ext/externs
cat /opt/ext/externs
