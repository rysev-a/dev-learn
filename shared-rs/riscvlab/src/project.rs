//! Проект «собрать у себя на компьютере»: файлы программы, Makefile и README, упакованные в zip без сжатия.

use serde::{Deserialize, Serialize};

/// Файл проекта.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ProjectFile {
    /// имя файла
    pub name: String,
    /// содержимое файла
    pub content: String,
    /// что это за файл — для подписи на странице
    pub note: String,
}

const MAKEFILE: &str = "# Сборка программы для RISC-V (32 бита, команды RV32IM) обычным clang + lld.
CLANG ?= clang
FLAGS  = --target=riscv32 -march=rv32im -mabi=ilp32 -nostdlib -static -fuse-ld=lld

program: program.s
\t$(CLANG) $(FLAGS) -o program program.s

# запустить в эмуляторе qemu (режим «пользовательских программ»)
run: program
\tqemu-riscv32 ./program; echo \"код возврата: $$?\"

# посмотреть, какие 32-битные слова получились (сравните с листингом на сайте)
dump: program
\tllvm-objdump -d program

clean:
\trm -f program
";

const README: &str = "# Программа для RISC-V

Файл program.s — ваша программа на ассемблере RISC-V (то, что вы писали на сайте).
Точка входа — метка _start. Вывод — системный вызов write (a7 = 64),
завершение — exit (a7 = 93), как в Linux.

## Что нужно установить

macOS:
  brew install llvm lld qemu
  export PATH=\"$(brew --prefix llvm)/bin:$(brew --prefix lld)/bin:$PATH\"

Ubuntu / Debian:
  sudo apt install clang lld llvm qemu-user

## Сборка и запуск

  make run     # собрать и запустить, в конце покажет код возврата
  make dump    # дизассемблировать: увидеть настоящие 32-битные слова
  make clean

Если у вас GNU-инструментарий (riscv64-unknown-elf-gcc), сборка такая:
  riscv64-unknown-elf-gcc -march=rv32im -mabi=ilp32 -nostdlib -static -o program program.s
  qemu-riscv32 ./program
";

/// Файлы проекта, который можно собрать на своём компьютере.
pub fn project_files(source: &str) -> Vec<ProjectFile> {
    let program = if source.ends_with('\n') { source.to_string() } else { format!("{source}\n") };
    vec![
        ProjectFile { name: "program.s".into(), content: program, note: "ваша программа".into() },
        ProjectFile { name: "Makefile".into(), content: MAKEFILE.into(), note: "сборка: make run".into() },
        ProjectFile { name: "README.md".into(), content: README.into(), note: "что установить".into() },
    ]
}

/// Запись архива.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ZipEntry {
    /// имя файла
    pub name: String,
    /// содержимое файла
    pub content: String,
}

/// Файлы проекта как записи архива.
pub fn project_zip(files: &[ProjectFile]) -> Vec<ZipEntry> {
    files.iter().map(|f| ZipEntry { name: f.name.clone(), content: f.content.clone() }).collect()
}

fn crc_table() -> [u32; 256] {
    let mut t = [0u32; 256];
    for (n, slot) in t.iter_mut().enumerate() {
        let mut c = n as u32;
        for _ in 0..8 {
            c = if c & 1 != 0 { 0xedb8_8320 ^ (c >> 1) } else { c >> 1 };
        }
        *slot = c;
    }
    t
}

/// CRC-32 (как в zip).
pub fn crc32(data: &[u8]) -> u32 {
    let table = crc_table();
    let mut c = 0xffff_ffffu32;
    for b in data {
        c = table[((c ^ u32::from(*b)) & 0xff) as usize] ^ (c >> 8);
    }
    c ^ 0xffff_ffff
}

/// Минимальный zip без сжатия («store») — чтобы отдать проект одним файлом.
pub fn make_zip(entries: &[ZipEntry]) -> Vec<u8> {
    let mut out: Vec<u8> = Vec::new();
    let mut central: Vec<u8> = Vec::new();
    let u16le = |v: &mut Vec<u8>, n: u16| v.extend_from_slice(&n.to_le_bytes());
    let u32le = |v: &mut Vec<u8>, n: u32| v.extend_from_slice(&n.to_le_bytes());

    for e in entries {
        let name = e.name.as_bytes();
        let data = e.content.as_bytes();
        let crc = crc32(data);
        let offset = out.len() as u32;

        u32le(&mut out, 0x0403_4b50);
        u16le(&mut out, 20); // версия для распаковки
        u16le(&mut out, 0x0800); // имена в UTF-8
        u16le(&mut out, 0); // без сжатия
        u16le(&mut out, 0);
        u16le(&mut out, 0x21); // дата 1980-01-01
        u32le(&mut out, crc);
        u32le(&mut out, data.len() as u32);
        u32le(&mut out, data.len() as u32);
        u16le(&mut out, name.len() as u16);
        u16le(&mut out, 0);
        out.extend_from_slice(name);
        out.extend_from_slice(data);

        u32le(&mut central, 0x0201_4b50);
        u16le(&mut central, 20);
        u16le(&mut central, 20);
        u16le(&mut central, 0x0800);
        u16le(&mut central, 0);
        u16le(&mut central, 0);
        u16le(&mut central, 0x21);
        u32le(&mut central, crc);
        u32le(&mut central, data.len() as u32);
        u32le(&mut central, data.len() as u32);
        u16le(&mut central, name.len() as u16);
        u16le(&mut central, 0); // дополнительное поле
        u16le(&mut central, 0); // комментарий
        u16le(&mut central, 0); // номер диска
        u16le(&mut central, 0); // внутренние атрибуты
        u32le(&mut central, 0o100644 << 16); // права rw-r--r--
        u32le(&mut central, offset);
        central.extend_from_slice(name);
    }

    let central_offset = out.len() as u32;
    let central_size = central.len() as u32;
    out.extend_from_slice(&central);
    u32le(&mut out, 0x0605_4b50);
    u16le(&mut out, 0);
    u16le(&mut out, 0);
    u16le(&mut out, entries.len() as u16);
    u16le(&mut out, entries.len() as u16);
    u32le(&mut out, central_size);
    u32le(&mut out, central_offset);
    u16le(&mut out, 0);
    out
}
