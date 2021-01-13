## Language Support

The languages currently have some level of support in the `solver` script. Most contain an executor that is compatible with performance timing, but some do not. To add support for a new language, see the [adding laguage support documentation](../lib/lang/README.md).

### C

C source code is compiled with `gcc`.

#### Timing Support

Use the [aoc_executor.c package](https://github.com/tcollier/aoc_executor.c) for timing support

### Golang

**IMPORTANT**: To compile golang code, set your `GOPATH` to the `ext/go` directory of this repository

#### Timing Support

Use the [aoc_executor.go package](https://github.com/tcollier/aoc_executor.go) for timing support

### Haskell

Basic support for compiling and running Haskell solutions is availabe, but no timing support

### Java

#### Timing Support

Use the [aoc_executor.java package](https://github.com/tcollier/aoc_executor.java) for timing support

### Kotlin

#### Timing Support

Use the [aoc_executor.kt package](https://github.com/tcollier/aoc_executor.kt) for timing support

### Lisp

`solver` will run a solution in `main.lisp` using `sbcl` ([download from sbcl.org](http://www.sbcl.org/) or install with HomeBrew).

#### Timing Support

Use the [aoc_executor.lisp package](https://github.com/tcollier/aoc_executor.lisp) for timing support

### Python

#### Timing Support

Use the [aoc_executor.py package](https://github.com/tcollier/aoc_executor.py) for timing support

### Ruby

#### Timing Support

Use the [aoc_executor.rb get](https://github.com/tcollier/aoc_executor.rb) for timing support

### Rust

#### Timing Support

Use the [aoc_executor.rs get](https://github.com/tcollier/aoc_executor.rs) for timing support

### Scala

#### Timing Support

Use the [aoc_executor.scala package](https://github.com/tcollier/aoc_executor.scala) for timing support

### Typescript

#### Requirements

The `solver` script uses `node` to compile typescript files and run the compiled javascript. Ensure `node` and `npm` are installed.

#### Timing Support

Use the [aoc_executor.kt package](https://github.com/tcollier/aoc_executor.js) for timing support
