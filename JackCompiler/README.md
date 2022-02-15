# Jack Compiler
Jack is a general-purpose language that can be implemented over different hardware platforms. In Nand to Tetris we develop a Jack compiler over the Hack platform.

## Jack Language 
Jack is an object-based language, meaning that it supports objects and classes but not inheritance. In this respect it is positioned somewhere between procedural languages like Pascal or C and object-oriented languages like Java or C++. Jack is certainly more simple-minded than any of these industrial strength programming languages. However, its basic syntax and semantics are similar to those of modern languages. Some features of the Jack language leave much to be desired. For example, its primitive type system is, well, rather primitive. Moreover, it is a weakly typed language, meaning that type conformity in assignments and operations is not strictly enforced. Also, you may wonder why the Jack syntax includes clunky keywords like do and let , why every subroutine must end with a return statement, why the language does not enforce operator priority, and so on you may add your favorite complaint to the list.

## Compilation
Compilation consists of two main stages: syntax analysis and code generation. The syntax analysis stage is usually divided further into two substages: tokenizing,the grouping of input characters into language atoms called tokens, and parsing, the grouping of tokens into structured statements that have a meaning.

![roadmap](https://github.com/OrrMatzkin/nand2tetris-Minesweeper/blob/master/readme%20assets/jack_compiler_roadmap.png?raw=true)

## From High Level to Low Level

![jack_to_hack](https://github.com/OrrMatzkin/nand2tetris-Minesweeper/blob/master/readme%20assets/jack_to_hack.png?raw=true)
