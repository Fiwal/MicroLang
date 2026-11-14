# MicroLang

MicroLang is a small compiled programming language written in Python.  The
compiler translates MicroLang source code to x86-64 NASM assembly and then
builds a Linux executable with GCC.

## Requirements and compiling files

The project requires Python 3, NASM, and GCC on Linux. The generated program
is an x86-64 Linux executable.

### Install the required tools

On Debian or Ubuntu:

```bash
sudo apt update
sudo apt install python3 nasm gcc
```

On Fedora:

```bash
sudo dnf install python3 nasm gcc
```

On Arch Linux:

```bash
sudo pacman -S python nasm gcc
```

Check that the tools are available:

```bash
python3 --version
nasm -v
gcc --version
```

### Compile a source file

```bash
python3 main.py path/to/program.ml
./program
```

If no path is supplied, the compiler asks for one interactively:

```bash
python3 main.py
Enter file path: path/to/program.ml
```

The current command-line compiler always creates:

| File | Purpose |
| --- | --- |
| `nasm_code.asm` | Generated NASM assembly. |
| `program.o` | Object file created by NASM. |
| `program` | Final executable. |

`main.py` checks that the supplied file exists before compilation. At the
moment `program`, `program.o`, and `nasm_code.asm` are overwritten on every
successful compilation.

## Basic syntax

Each instruction ends with `;`. Arguments follow the instruction name after
`:` and are separated with commas.

```text
instruction: first_argument, second_argument;
instruction_without_arguments;
```

Whitespace outside strings is ignored. A line comment begins with `#`.

```text
# This line is a comment
int: number, 10;
```

Strings may use double quotes or backticks. New lines inside a string become
`\n` in the generated output. Escape sequences such as `\"` are not currently
supported.

```text
print: "Hello, MicroLang!\n";
```

## Program structure

Every program must define a `main` function.

```text
fn: main, 0;
    print: "Hello, MicroLang!\n";
    return: 0;
endfn;
```

Function syntax is `fn: name, parameter_count;`. Parameters can be given
names with `name_parameter: name, index;`, where indexing starts at zero.

```text
fn: add_two, 2;
    name_parameter: a, 0;
    name_parameter: b, 1;
    add: a, b;
    return: a;
endfn;

fn: main, 0;
    add_two: 10, 32;
    print: return_value, "\n";
    return: 0;
endfn;
```

The return value of a function is available immediately after its call as
`return_value`. To copy it to a variable, attach `-get` to the call:

```text
int: result;
add_two: 10, 32;
-get: result;
print: result, "\n";
```

## Variables and values

MicroLang supports signed integer values and strings. Names must be valid
identifiers and cannot be language keywords.

Global variables are declared outside functions:

```text
int: counter;
int: limit, 10;
string: greeting, "Hello";
```

Local integer variables are declared inside functions:

```text
int: value;
int: total, 0;
```

`int` variables can be assigned with `set` and changed with arithmetic
instructions:

```text
set: total, 5;
add: total, 3;
sub: total, 1;
mul: total, 2;
div: total, 7;
mod: total, 3;
```

The first argument of an arithmetic instruction must be an integer variable.
The second may be an integer literal, integer variable, or `return_value`.

## Input and output

`print` accepts one or more integer or string values. `input` reads one integer
into an integer variable.

```text
int: age;
print: "Enter age: ";
input: age;
print: "Age: ", age, "\n";
```

## Conditions and loops

`if` compares two integer values using `==`, `!=`, `<`, `<=`, `>`, or `>=`.
`else` is optional and each conditional ends with `endif`.

```text
if: age, >=, 18;
    print: "adult\n";
else;
    print: "minor\n";
endif;
```

`loop` creates an infinite loop. Exit it with `break`; close the block with
`endloop`.

```text
int: i, 0;
loop;
    add: i, 1;
    if: i, ==, 3;
        break;
    endif;
endloop;
```

## Instructions

| Instruction | Meaning |
| --- | --- |
| `fn: name, count;` / `endfn;` | Defines a function. |
| `name_parameter: name, index;` | Names a function parameter. |
| `int: name[, value];` | Declares an integer. |
| `string: name, value;` | Declares a global string. |
| `set: variable, value;` | Assigns an integer value. |
| `add`, `sub`, `mul`, `div`, `mod` | Modifies an integer variable. |
| `print: value[, ...];` | Prints integers and strings. |
| `input: variable;` | Reads an integer. |
| `if: left, operator, right;` / `else;` / `endif;` | Conditional block. |
| `loop;` / `break;` / `endloop;` | Loop control. |
| `return[: value];` | Returns from a function; no value returns `0`. |
| `function: argument[, ...];` | Calls a user-defined function. |
| `-get: variable;` | Copies the preceding call's result into a variable. |

## Current limitations

- Only integer input is supported.
- Division or modulo by zero terminates the generated program.
- `return_value` is register-backed; use it immediately after a function call,
  or copy it with `-get` before `print` or `input`.
- String escaping is not implemented.
