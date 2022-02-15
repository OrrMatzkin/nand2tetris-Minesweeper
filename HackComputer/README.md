# The Hack Computer

The Hack Computer is a theoretical computer design created by Noam Nisan and Shimon Schocken and described in their book, The Elements of Computing Systems: Building a Modern Computer from First Principles. In using the term "modern", the authors refer to a digital, binary machine that is patterned according to the von Neumann architecture model.

## Table of context
- [Hack Computer diagram](#hack-computer-diagram)
- [Central Processing Unit](#central-processing-unit)
    - [Arithmetic Logic Unit](#arithmetic-logic-unit)
    - [Registers](#registers)
        - [Data register](#data-registers)
        - [Address Register](#address-register)
        - [Program counter](#program-counter-(pc))
    - [Control Unit](#control-unit)    
- [Memory](#memory)
    - [Data Memory (RAM)](#data-memory-(ram))
    - [Instruction Memory (ROM)](#instruction-memory-(rom))
- [Logic Gates](#logic-gates)       


## Hack Computer Diagram
The Computer chip can be realized using three chip-parts: a CPU, a data Memory named RAM, and an instruction memory named ROM32K.

![hack coomputer diagram](https://github.com/OrrMatzkin/nand2tetris-Minesweeper/blob/master/readme%20assets/Hack_Computer_Block_Diagram_2.png?raw=true?=100x20)

This task of implementing the computer is done using a design tool called Hardware Description Language. HDL is a formalism used to define and test chips: objects whose interfaces consist of input and output pins that carry Boolean signals, and whose bodies are composed of inter-connected collections of other, lower level, chips.

## Central Processing Unit (CPU)
The centerpiece of the computer’s architecture—is in charge of executing the instructions of the currently loaded program. These instructions tell the CPU which calculation it has to perform, which registers is has to read from or write to, and which instruction it has to fetch and execute next. The CPU executes these tasks using three main hardware elements: an Arithmetic-Logic Unit (ALU), a set of registers, and a control unit.

![cpu diagram](https://github.com/OrrMatzkin/nand2tetris-Minesweeper/blob/master/readme%20assets/CPU_Diagram.png?raw=true)

## Arithmetic Logic Unit (ALU)
The ALU chip is built to perform all the low-level arithmetic and logical operations featured by the computer. For example, a typical ALU can add two numbers, compute a bitwise And function on two numbers, compare two numbers, and so on. How much functionality an ALU should have is a matter of need, budget, energy, and similar cost- effectiveness considerations. Any function not supported by the ALU as a primitive hardware operation can be later realized by the computer’s system software.

## Registers
Since the CPU is the computer’s centerpiece, it must perform as efficiently as possible. In order to boost performance, it is desirable to store the intermediate results that computer programs generate locally, close to the ALU, rather than ship them in and out of the CPU chip and store them in some remote and separate RAM chip. Thus, a CPU is typically equipped with a small set of 2 up to 32 resident high-speed registers, each capable of holding a single word.

### Data Register 
This register give the CPU short-term memory services. For example, if a program wants to calculate (a − b) ⋅ c, we must first compute and remember the value of (a − b). In principle, this temporary result can be stored in some memory register. Clearly, a much more sensible solution is to store it locally inside the CPU, using a data register. Typically, CPU’s
use at least one and up to 32 data registers, we only used one.

### Address Register
Many machine language instructions involve memory access: reading data, writing data, and fetching instructions. In any one of these operations, we must specify which memory register we wish to operate on. This is done by supplying an address. In some cases, the address is coded as part of the instruction, while in other cases the address is specified, or computed, by some previous instruction. In the latter case, the address must be stored somewhere. This is done using a CPU-resident chip called address register.

### Program counter (PC)
When executing a program, the CPU must always keep track of the address of the instruction that must be fetched and executed next. This address is kept in a special register called program counter or PC.

## Control Unit
A computer instruction is represented as a binary code 16 bits wide. Before such an instruction can be executed, it must be decoded, and the information embedded in it must be used to signal various hardware devices (ALU, registers, memory) how to execute the instruction. The instruction decoding is done by some control unit, which is also responsible for figuring out which instruction to fetch and execute next.

## Memory 
Physically, the memory is a linear sequence of addressable registers, each having a unique address and a value, which is a fixed-size word of information. Logically, the memory is divided into two areas. One area is dedicated for storing data, e.g. the arrays and objects of programs that are presently executing, while the other area is dedicated for storing the programs’ instructions. Although all these “data words” and “instruction words” look exactly the same physically, they serve very different purposes.

### Data Memory (RAM)
High-level programs manipulate abstract artifacts like variables, arrays, and objects. After the programs are translated into machine language, these data abstractions become binary codes, stored in the computer’s memory. Once an individual register has been selected from the memory by specifying its address, its contents can be either read or written to. In the former case, we retrieve the value of the selected register. In the latter case, we store a new value in the selected register, overriding the previous value. Such memories are sometimes referred to as “read/write” memories.

The overall address space known as the Hack data memory is realized by a chip called Memory. This chip is essentially a package of three 16-bit storage devices: a RAM (16K registers, for regular data storage), a Screen (8K registers, acting as the screen memory map), and a Keyboard (1 register, acting as the keyboard memory map)

### Instruction Memory (ROM)
Before high-level programs can be executed on the computer, they must be translated into machine language. Following this translation, each high-level statement becomes a series of one or more machine language instructions. These instructions are stored in the computer’s instruction memory as binary codes. In each step of a program’s execution, the CPU fetches (i.e., reads) a binary machine instruction from a selected register in the instruction memory, decodes it, executes the specified instruction, and figures out which instruction to fetch and execute next.

## Logic Gates
A logic gate is an idealized model of computation or physical electronic device implementing a Boolean function, a logical operation performed on one or more binary inputs that produces a single binary output.

All the basic logic gates are designed from scratch from the universal NAND gate. 

| No. | Name | Description | In | Out |
| --- | --- | --- | --- | --- |
| 1 | And | a single bit bitwise And | a, b | out
| 2  | And16 | a 16-bit bitwise And |  a, b | out
| 3 | Or | a single bit bitwise Or | a, b | out
| 4 | Or16 | a 16-bit bitwise Or | a, b | out
| 5 | Not | a single bit bitwise Not | in | out
| 6 | Not16 | a 16-bit bitwise Not | in | out
| 7 | Xor | a single bit bitwise Exclusive Or | a, b | out
| 8 | Or8Way | 8-way Or gate | in | out
| 9 | Or16Way | 16-way Or gate | in | out
| 10 | Dmux | 2-way single bit Demultiplexor | in, sel | a, b
| 11 | Dmux4Way | 4-way single bit Demultiplexor | in, sel | a, b, c, d
| 12 | Dmux8Way | 8-way single bit Demultiplexor | in, sel | a, b, c, d, e, f, g, h
| 13 | Mux | 2-way single bit Multiplexor | in, sel | a, b
| 14 | Mux16 | 2-way 16 bit Multiplexor | in, sel | a, b
| 15 | Mux4Way16 | 4-way 16 bit Multiplexor | in, sel | a, b
| 16 | Mux8Way16 | 8-way 16 bit Multiplexor | in, sel | a, b

There also some more advanced gates such: Add16 (added two 16 bit length numbers), ShiftRight, ShiftLeft etc.