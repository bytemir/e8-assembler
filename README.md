# E8 Assembler

A lightweight Python assembler that translates human-readable **E8 assembly** (`.asm`) into a binary-ready hex format (`.bin`) for the **E8 Custom 8-bit CPU**. Each source line becomes one 3-byte instruction written as a space-separated string of hex values.

## Overview

The assembler reads a fixed input file, parses each line as an opcode plus two operands, and emits a corresponding 3-byte machine instruction. Output is written line-for-line to a `.bin` file, where each line has the form:

```
0x<opcode> 0x<operand1> 0x<operand2>
```

The E8 CPU uses a fixed **3-byte instruction format**: one opcode byte followed by two operand bytes. Registers serve dual roles as general-purpose data storage and as video channels when driving the display (A = red, B = green, C = blue, D = X coordinate, E = Y coordinate).

## Directory Configuration

Paths are **hardcoded** in the assembler script. To assemble a different program, change the `file_name` variable at the top of the script:

| Setting   | Value                          |
|-----------|--------------------------------|
| Input     | `tests/{file_name}.asm`        |
| Output    | `out/{file_name}.bin`          |
| Default   | `file_name = "example"`        |

Ensure both the `tests/` and `out/` directories exist before running the assembler. The script truncates the output file on each run, then appends one hex line per successfully parsed source line.

## Syntax and Constraints

### The 3-token rule

Every line in a `.asm` file **must contain exactly three space-separated tokens**:

```
<OPCODE> <OPERAND1> <OPERAND2>
```

The assembler splits each line on spaces and rejects any line that does not produce exactly three elements. If a malformed line is encountered, assembly **terminates immediately** and prints an error:

```
Expected: An Opcode and 2 Operands for line <N> instead only found <count>.
Terminating...
```

There is no support for comments, blank lines, labels, or alternate separators. Each non-empty line must be a complete instruction with two operands.

### Padding unused operands

Several instructions do not use both operand slots at the machine level, but the parser still requires two operands on every line. Use **`0`** as a placeholder where an operand is ignored by the CPU.

| Instruction category | Padding pattern              | Example        |
|----------------------|------------------------------|----------------|
| Unconditional / conditional jump | Second operand unused | `JMP 42 0`     |
| Memory load / store  | Second operand unused        | `LOAD 16 0`    |
| Screen operations    | Both operands unused         | `SCREEN_DRAW 0 0` |

### Operand types

| Operand kind   | Accepted values                          | Encoding                          |
|----------------|------------------------------------------|-----------------------------------|
| Register       | `A`, `B`, `C`, `D`, `E`                  | Mapped to `0x01`–`0x05`           |
| Immediate      | Non-negative decimal integer             | Encoded as `0x` + 2-digit hex     |
| Address / value| Non-negative decimal integer             | Same immediate encoding as above  |

Immediate and address values are converted to **two hex digits** (zero-padded). For example, decimal `10` becomes `0x0A`, and `255` becomes `0xFF`.

### Registers

| Register | Hex ID | General use     | Video mapping |
|----------|--------|-----------------|---------------|
| A        | `0x01` | Data            | Red channel   |
| B        | `0x02` | Data            | Green channel |
| C        | `0x03` | Data            | Blue channel  |
| D        | `0x04` | Data            | X coordinate  |
| E        | `0x05` | Data            | Y coordinate  |

## Instruction Set Reference

Each row shows the exact `.asm` syntax the assembler expects and the resulting `.bin` output.

| Mnemonic       | Opcode | Operand 1              | Operand 2              | `.asm` example       | Output (hex bytes)        |
|----------------|--------|------------------------|------------------------|----------------------|---------------------------|
| `MOV`          | `0x00` | Register (`A`–`E`)     | Immediate value        | `MOV A 255`          | `0x00 0x01 0xFF`          |
| `JMP`          | `0x01` | Address (immediate)    | `0` (unused)           | `JMP 10 0`           | `0x01 0x0A 0x00`          |
| `ADD`          | `0x02` | Register (`A`–`E`)     | Immediate value        | `ADD B 5`            | `0x02 0x02 0x05`          |
| `SUB`          | `0x03` | Register (`A`–`E`)     | Immediate value        | `SUB C 1`            | `0x03 0x03 0x01`          |
| `MUL`          | `0x04` | Register (`A`–`E`)     | Immediate value        | `MUL D 2`            | `0x04 0x04 0x02`          |
| `DIV`          | `0x05` | Register (`A`–`E`)     | Immediate value        | `DIV E 4`            | `0x05 0x05 0x04`          |
| `LOAD`         | `0x06` | Address (immediate)    | `0` (unused)           | `LOAD 32 0`          | `0x06 0x20 0x00`          |
| `STORE`        | `0x07` | Address (immediate)    | `0` (unused)           | `STORE 32 0`         | `0x07 0x20 0x00`          |
| `JMPG`         | `0x08` | Address (immediate)    | `0` (unused)           | `JMPG 20 0`          | `0x08 0x14 0x00`          |
| `JMPZ`         | `0x09` | Address (immediate)    | `0` (unused)           | `JMPZ 8 0`           | `0x09 0x08 0x00`          |
| `RAM_WRITE`    | `0x0A` | Address (immediate)    | Value (immediate)      | `RAM_WRITE 4 99`     | `0x0A 0x04 0x63`          |
| `RAM_READ`     | `0x0B` | Address (immediate)    | Register / target      | `RAM_READ 4 1`       | `0x0B 0x04 0x01`          |
| `SCREEN_CLEAR` | `0x0C` | `0` (unused)           | `0` (unused)           | `SCREEN_CLEAR 0 0`   | `0x0C 0x00 0x00`          |
| `SCREEN_DRAW`  | `0x0D` | `0` (unused)           | `0` (unused)           | `SCREEN_DRAW 0 0`    | `0x0D 0x00 0x00`          |

### Instruction summaries

- **`MOV`** — Load an immediate value into a register.
- **`JMP`** — Unconditional jump to the given address.
- **`JMPG`** — Jump if greater than zero (conditional).
- **`JMPZ`** — Jump if equal to zero (conditional).
- **`ADD` / `SUB` / `MUL` / `DIV`** — Arithmetic on a register using an immediate operand.
- **`LOAD` / `STORE`** — Transfer data between CPU and addressed memory.
- **`RAM_WRITE` / `RAM_READ`** — Direct RAM access with two immediate operands.
- **`SCREEN_CLEAR`** — Clear the display buffer.
- **`SCREEN_DRAW`** — Render the current register state (RGB in A/B/C, position in D/E) to the screen.

## Usage

### Prerequisites

- Python 3.10 or later (required for `match` / `case` syntax)

### Step-by-step example

**1. Create the source file** at `tests/example.asm`:

```asm
MOV A 255
MOV B 128
MOV C 64
MOV D 10
MOV E 20
SCREEN_DRAW 0 0
```

This program sets pixel color to orange-ish RGB `(255, 128, 64)`, positions it at `(10, 20)`, and draws it to the screen.

**2. Run the assembler:**

```bash
python assembler.py
```

**3. Inspect the output** at `out/example.bin`:

```
0x00 0x01 0xFF
0x00 0x02 0x80
0x00 0x03 0x40
0x00 0x04 0x0A
0x00 0x05 0x14
0x0D 0x00 0x00
```

Each output line maps directly to one source line:

| Source line         | Meaning                          | Output              |
|---------------------|----------------------------------|---------------------|
| `MOV A 255`         | Red = 255                        | `0x00 0x01 0xFF`    |
| `MOV B 128`         | Green = 128                      | `0x00 0x02 0x80`    |
| `MOV C 64`          | Blue = 64                        | `0x00 0x03 0x40`    |
| `MOV D 10`          | X = 10                           | `0x00 0x04 0x0A`    |
| `MOV E 20`          | Y = 20                           | `0x00 0x05 0x14`    |
| `SCREEN_DRAW 0 0`   | Draw pixel at (D, E) with (A,B,C)| `0x0D 0x00 0x00`    |

On success, the assembler prints assembly time and the output path:

```
Finished Assembling in: 0.000123s, saved to "out/example.bin".
```

### Assembling a different program

1. Place your source at `tests/<name>.asm`.
2. Set `file_name = "<name>"` in the assembler script.
3. Run `python assembler.py`.
4. Load `out/<name>.bin` into the E8 CPU emulator or hardware loader.

## Project layout

```
.
├── assembler.py          # Main assembler script
├── tests/
│   └── example.asm       # Sample E8 assembly source
└── out/
    └── example.bin       # Generated hex instruction file
```

## Limitations

- **Fixed paths** — Input and output locations are set in code, not via command-line arguments.
- **Strict formatting** — Exactly three tokens per line; no comments, labels, or macro support.
- **No two-pass assembly** — Jump targets are numeric addresses, not symbolic labels.
- **Space-only splitting** — Multiple consecutive spaces produce empty tokens and fail the 3-token check.
- **Supported opcodes only** — Unrecognized mnemonics produce empty output lines rather than explicit errors.
