# My_compiler

A comprehensive compilation toolkit featuring two distinct compilers for different programming paradigms, developed by Sotiria Kastana and Sotiris Mpalatsias.

## Project Overview

This repository contains two complete compiler implementations:

1. **Starlet Compiler** - A compiler for a simplified C-like procedural language
2. **P++ Compiler** - A compiler for an object-oriented language with inheritance support

Both compilers demonstrate different aspects of compiler design, from lexical analysis and parsing to code generation and optimization.

---

## Starlet Compiler (`compiler_to_asemply/`)

### Language Overview
Starlet is a simplified C-like procedural programming language designed for educational purposes. It supports:

- **Variables & Data Types**: Integer variables with declaration syntax
- **Functions**: Parameter passing with `in`, `inout`, and `inandout` modes
- **Control Structures**: `if-then-else`, `while`, `dowhile`, `loop-endloop`
- **Special Statements**: `exit` (break from loops), `return`, `print`, `input`
- **Switch-like Constructs**: `forcase` and `incase` statements
- **Expressions**: Arithmetic operations with standard precedence

### Example Starlet Program
```starlet
program MAX 
    declare a,b,c,d;
    function max(in x,in y)
        if(x>y) then
            return x
        else
            return y
        endif
    endfunction;
    a := 1;
    b := 2;
    c := 3;
    d := 4;
    c:=max(in max(in a, in b),in max(in c,in d));
    print c
endprogram
```

### Compiler Features
- **Multi-target Code Generation**: Produces three output formats
  - `.asm` - Assembly code (MIPS-like assembly)
  - `.c` - Simplified C code
  - `.int` - Intermediate representation
- **Semantic Analysis**: Symbol table management with scope checking
- **Error Handling**: Comprehensive syntax and semantic error reporting with suggestions
- **Optimization**: Quad-based intermediate code generation

### Usage
```bash
python3 starletc.py -i program.stl
```

This generates:
- `program.asm` - Assembly code output
- `program.c` - C code translation  
- `program.int` - Intermediate code representation

---

## P++ Compiler (`compiler_to_c/`)

### Language Overview
P++ is an object-oriented programming language with Python-like syntax supporting:

- **Classes & Inheritance**: Single inheritance with method overriding
- **Constructors**: Multiple constructor overloading (`__init__`)
- **Method Overloading**: Multiple methods with same name, different parameters
- **Access Control**: Self-reference for instance variables and methods
- **Data Types**: `int`, `bool`, and custom class types
- **Control Structures**: `if-elif-else`, `while`, `break`
- **I/O Operations**: `in()` for input, `out()` for output

### Example P++ Program
```python
class Calculator:
    int result;;

    def __init__(self): Calculator
        self.result = 0;;

    def add(self, a, b): int
        return a + b;
    ;

    def main(self): -
        int x, y;
        in(x);
        in(y);
        self.result = self.add(x, y);
        out(self.result);
    ;
```

### Compiler Features
- **ANTLR4 Grammar**: Uses ANTLR4 for robust parsing and lexical analysis
- **C Code Generation**: Translates OOP constructs to equivalent C structures
- **Type System**: Static type checking with inheritance support
- **Memory Management**: Struct-based object representation in C

### Usage
```bash
# Generate parser/lexer from grammar
antlr4 -Dlanguage=Python3 -listener Ppp.g4

# Compile P++ program to C
python3 PppExecute.py example.ppp

# Compile and run generated C code
gcc exe.c
./a.out
```

This generates:
- `exe.c` - Main C source file
- `header.h` - Type definitions and declarations

---

## Project Structure

```
My_compiler/
├── README.md                          # This file
├── compiler_to_asemply/               # Starlet Compiler
│   ├── README.txt                     # Starlet-specific documentation
│   ├── compiler/
│   │   └── starletc.py               # Main Starlet compiler (1795 lines)
│   ├── examples/                      # Example .stl programs (10 files)
│   │   ├── test0.stl ... test7.stl   # Test programs
│   │   ├── max.stl                   # Maximum function example
│   │   ├── big_test.stl              # Complex program example
│   │   └── starlet_compiler_test.py  # Automated test suite
│   └── report.pdf                    # Technical report
└── compiler_to_c/                     # P++ Compiler  
    ├── README.txt                     # P++ specific documentation
    ├── Ppp.g4                        # ANTLR4 grammar definition (508 lines)
    ├── PppExecute.py                 # Main execution script
    ├── PppMyListener.py              # ANTLR listener for syntax tree
    └── examples/                      # Example .ppp programs (5 files)
        ├── test.ppp                  # Basic class example
        ├── calculator.ppp            # Calculator with methods
        ├── bookstore.ppp            # Complex inheritance example
        ├── TowerGame.ppp            # Game logic example
        └── MyShape.ppp              # Shape hierarchy example
```

## Technical Implementation

### Starlet Compiler Architecture
- **Recursive Descent Parser**: Hand-written parser with lookahead
- **Symbol Table**: Hierarchical scope management with offset calculation
- **Quad Generation**: Three-address code intermediate representation
- **Assembly Generation**: MIPS-like assembly with register allocation
- **Error Recovery**: Levenshtein distance for typo suggestions

### P++ Compiler Architecture  
- **ANTLR4 Parser**: Grammar-driven parsing with listener pattern
- **AST Processing**: Syntax tree traversal for code generation
- **Type System**: Object-oriented type checking and inheritance resolution
- **C Translation**: Struct-based OOP implementation in C

## Features Comparison

| Feature | Starlet | P++ |
|---------|---------|-----|
| **Paradigm** | Procedural | Object-Oriented |
| **Syntax** | C-like | Python-like |
| **Output** | Assembly + C + IR | C only |
| **Parser** | Hand-written | ANTLR4 |
| **Type System** | Simple integers | OOP with inheritance |
| **Error Handling** | Advanced with suggestions | Standard |

## Testing

### Starlet Testing
```bash
cd compiler_to_asemply/examples/
python3 starlet_compiler_test.py
```

### P++ Testing
Each example in `compiler_to_c/examples/` can be compiled and tested individually.

## Authors

- **Sotiria Kastana** (AM 2995, cse52995) - Co-developer of Starlet compiler
- **Sotiris Mpalatsias** (AM 3036, cse53036) - Lead developer, both compilers

## License

Educational project - see individual file headers for specific authorship details.
