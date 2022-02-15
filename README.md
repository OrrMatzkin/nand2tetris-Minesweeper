# nand2tetris-Minesweeper

As part of The Hebrew University of Jerusalem course *"Nand to Tetris"* I built a general-purpose computer system and a modern software hierarchy from the ground up. After the copmuter was ready I designed and develpoed a mini version of the known Minesweeper game to run on the computer system.

Minesweeper is a single-player puzzle video game. The objective of the game is to clear a rectangular board containing hidden "mines" without detonating any of them, with help from clues about the number of neighbouring mines in each field. The game originates from the 1960s, and it has been written for many computing platforms in use today.
For more information about the game see https://en.wikipedia.org/wiki/Minesweeper_(video_game)

For the full game instructions run the game locally.


![build](https://img.shields.io/badge/build-passing-brightgreen)

![platform](https://camo.githubusercontent.com/fb4912e741e566f3089bd8ca3561a536cc352ecfae75127d2fab3e1852e2234d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f706c6174666f726d2d6c696e75782532302537432532306d61636f7325323025374325323077696e646f77732d6c6967687467726579) 

## Table of context
- [About the Course](#about-the-course)
- [Requirements](#requirements)
- [Run Locally](#run-locally)
- [Screenshots](#screenshots)    
- [Copyright](#copyright)    

## About the Course
Nand to Tetris a hands-on journey that starts with the most elementary logic gate, called Nand, and ends up, twelve projects later, with a general-purpose computer system capable of running Tetris, as well as any other program like Minesweeper. 

Today, Nand to Tetris courses are taught in numerous universities, high schools, coding boot camps, online platforms, and hacker clubs around the world. The book and the online course became highly popular, and thousands of learners — ranging from high school students to Google engineers, routinely post reviews describing Nand to Tetris as their best educational experience ever. 

The Course follows the book: The Elements of Computing Systems, Second Edition: Building a Modern Computer from First Principles, By Noam Nisan and Shimon Schocken, MIT Press, 2021.

https://www.nand2tetris.org
https://mitpress.mit.edu/books/elements-computing-systems


## Requirements
Minesweeper requires the followin to run:

- Java Runtime Environment
- Nand2Tetris software tools
    

## Run Locally

Clone the project

```bash
    git clone https://github.com/OrrMatzkin/   nand2tetris-Minesweeper.git
```

Go to the project directory

```bash
  cd nand2tetris-Minesweeper
```
Open the VMEmulator

```bash
  cd tools
  sh VMEmulator.sh
```
(on Windows just click VMEmulator.bat)

Load the program, in the file menu click "load program". Navigate to MinesweeperGame directory and load the entire folder named "VMfiles".

Set Animate to "No Animation" in the view menu.

Finaly You can hit the "Run" button in the Run menu.

![Loading Program](https://github.com/OrrMatzkin/nand2tetris-Minesweeper/blob/master/readme%20assets/Loading%20Minesweeper.gif?raw=true)

## Screenshots 

![open](https://github.com/OrrMatzkin/nand2tetris-Minesweeper/blob/master/readme%20assets/start.png?raw=true)

![playing](https://github.com/OrrMatzkin/nand2tetris-Minesweeper/blob/master/readme%20assets/playing.png?raw=true)

![game over](https://github.com/OrrMatzkin/nand2tetris-Minesweeper/blob/master/readme%20assets/game%20over.png?raw=true)

## Copyright
All files, software and tools are part of nand2tetris, as taught in The Hebrew University, according to the specifications given in https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017) and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/)
