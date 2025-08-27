# My_compiler

Two small compilers in one repo:

- compiler_to_asemply: Starlet (a simplified C-like language) → MIPS-like assembly, plus simplified C and intermediate quads.
- compiler_to_c: P++ (a toy OO language with classes/inheritance) → C (exe.c + header.h) using ANTLR4.

## Repository layout
- `compiler_to_asemply/`
	- `compiler/starletc.py` — Starlet compiler entrypoint
	- `examples/*.stl` — sample Starlet programs
- `compiler_to_c/`
	- `Ppp.g4` — P++ grammar (ANTLR4, Python target, embedded codegen)
	- `PppExecute.py` — runs the pipeline and emits C code
	- `examples/*.ppp` — sample P++ programs

## Prerequisites
- Python 3.8+ (both projects)
- For compiler_to_c only:
	- Java 8+ and ANTLR4 tool (either `antlr4` on PATH or the .jar)
	- A C compiler (e.g., gcc/clang; on Windows you can use MSYS2/MinGW)

## Quickstart (Windows PowerShell)

### 1) Starlet → assembly/C (`compiler_to_asemply`)
This compiler generates three files next to your input: `.asm` (MIPS-like), `.c` (simplified C), `.int` (intermediate quads).

```powershell
cd .\compiler_to_asemply\compiler
python .\starletc.py -i ..\examples\test3.stl
```

Outputs (for `test3.stl`):
- `test3.asm`
- `test3.c`
- `test3.int`

Examples: `compiler_to_asemply/examples/*.stl`

### 2) P++ → C (`compiler_to_c`)
Step 1: Generate ANTLR Python artifacts.

```powershell
cd .\compiler_to_c
antlr4 -Dlanguage=Python3 -listener Ppp.g4
# If antlr4 is not on PATH, use the jar instead:
# java -jar antlr-4.x-complete.jar -Dlanguage=Python3 -listener Ppp.g4
```

Step 2: Parse an example and generate C (`exe.c`, `header.h`) and a parse trace (`tree.txt`).

```powershell
python .\PppExecute.py .\examples\calculator.ppp
```

Step 3: Build and run the generated C.

```powershell
gcc .\exe.c -o exe
.\n+```

Examples: `compiler_to_c/examples/*.ppp`

## Notes
- Starlet supports: program/declare, functions with parameter modes (in, inout, inandout), if/then/else, while, do-while, loop/exit, forcase/incase/default, return, print, input, and expressions.
- P++ supports: classes, inheritance, methods, `self`, constructors, int/bool, while/if, simple I/O. Methods are emitted as `Class__method__N(Class_t* self, ...)` and classes become `typedef struct Class_s { ... } Class_t;`.

## Troubleshooting
- "antlr4 not recognized": use the jar form with `java -jar antlr-4.x-complete.jar ...` or add ANTLR to PATH.
- "gcc not found": install a C toolchain (e.g., MSYS2/MinGW) or use an alternative compiler and adjust commands.

