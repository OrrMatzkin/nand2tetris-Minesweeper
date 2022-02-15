# VM Translator

Before a high-level program can run on a target computer, it must be translated into the computer’s machine language. Traditionally, a separate compiler was developed specifically for any given pair of high-level language and low-level machine language. Over the years, the reality of many high-level languages, on the one hand, and many processors and instruction sets, on the other, has led to a proliferation of many different compilers, each depending on every detail of both its source and target languages. One way to decouple this dependency is to break the overall compilation process into two nearly separate stages. In the first stage, the high-level code is parsed and translated into intermediate and abstract processing steps — steps that are neither high nor low. In the second stage, the intermediate steps are translated further into the low-level machine language of the target hardware.
The VM Translator is exactly that second stage.

## VM Model
Our VM model is stack-based: all the VM operations take their operands from, and store their results on, the stack. There is only one data type: a signed 16-bit integer. A VM program is a sequence of VM commands that fall into four categories:

- Push / pop commands transfer data between the stack and memory segments. 
- Arithmetic-logical commands perform arithmetic and logical operations.
- Branching commands facilitate conditional and unconditional branching operations.
-  Function commands facilitate function call-and-return operations.

## Example

Assembly and binary representations of the same program.

![vm_to_assembly](https://github.com/OrrMatzkin/nand2tetris-Minesweeper/blob/master/readme%20assets/vm_to_assembly2.png?raw=true)

