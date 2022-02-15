# Assembler
Before an assembly program can be executed on a computer, it must be translated into the computer’s binary machine language (our Hack language). The translation task is done by a program called the assembler. The assembler takes as input a stream of assembly commands and generates as output a stream of equivalent binary instructions. The resulting code can be loaded as is into the computer’s memory and executed by the hardware.

The assembler is essentially a text-processing program, designed to provide translation services. For each symbolic command, the assembler carries out the following tasks (not necessarily in that order):

- Parse the symbolic command into its underlying fields.
- For each field, generate the corresponding bits in the machine language.
- Replace all symbolic references (if any) with numeric addresses of memory locations.
- Assemble the binary codes into a complete Hack machine instruction.

## Binary Code (.hack) Files
A binary code file is composed of text lines. Each line is a sequence of 16 ‘‘0’’ and ‘‘1’’ ASCII characters, coding a single 16-bit machine language instruction. Taken together, all the lines in the file represent a machine language program. When a machine language program is loaded into the computer’s instruction memory, the binary code represented by the file’s nth line is stored in address n of the instruction memory.

## Assembly Language (.asm) File
An assembly language file is composed of text lines, each representing either an instruction or a symbol declaration:

- Instruction: an A-instruction or a C-instruction.
- (Symbol): This pseudo-command binds the Symbol to the memory location into which the next command in the program will be stored. It is called ‘‘pseudo-command’’ since it generates no machine code.

## Example

Assembly and binary representations of the same program.

![assembly_to_binary](https://github.com/OrrMatzkin/nand2tetris-Minesweeper/blob/master/readme%20assets/assembly_to_binary_example.png?raw=true)
