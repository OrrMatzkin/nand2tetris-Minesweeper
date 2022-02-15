# Jack Operation System

The OS is designed to close gaps between the computer’s hardware and software, making the computer system more accessible to programmers, compilers, and users. For example, to display the text Hello World on the screen, several hundred pixels must be drawn at specific screen locations. This can be done by consulting the hardware specification and writing code that turns bits on and off in selected RAM locations. Clearly, high-level programmers expect a better interface. They want to write ```print("Hello World")``` and let someone else worry about the details. That’s where the operating system enters the picture.

## Modules
- [Math](#math)
- [String](#string) 
- [Array](#array)
- [Output](#output) 
- [Screen](#screen) 
- [Keyboard](#keyboard) 
- [Memory](#memory) 
- [Sys](#sys) 
- [Errors](#errors) 

## Math
| Type | Name | Return Value | Arguments | Description |
| --- | --- | --- | --- | --- |
| function | init | void | - | for internal use only. |
| function | abs | int | int x | returns the absolute value of x. |
| function | multiply | int | int x, y | returns the prodcut of of x and y. |
| function | divide | int | int x, y | returns the integer part of x/y. |
| function | min | int | int x, y | returns the minimum of x and y. |
| function | max | int | int x, y | returns the maximum of x and y. |
| function | sqrt | int | int x | returns the integer part of the square root of x. |

## String
| Type | Name | Return Value | Arguments | Description |
| --- | --- | --- | --- | --- |
| constractor | new | String | int MaxLength | constracts a new empty string. |
| method | dispose | void | - | disposes this string. |
| method | length | int | - | returns the length of this string. |
| method | charAt | char | int j | returns the character at location j of this string. |
| method | setCharAt | void | int j, char c | sets the j-th element of this string to c |
| method | appendChar | String | char c | appends c to this string and returns this strin |
| method | eraseLastChar | void | - | erases the last character from this string. |
| method | intValue | int | - | returns the integer value of this string. |
| method | setInt | void | - | sets this string to hold a representation of j. |
| function | backSpace | char | - | returns the backspace character. |
| function | doubleQuote | char | - | returns the double quote (") character. 
| function | newLine | char | - | returns the newline character. |

## Array
| Type | Name | Return Value | Arguments | Description |
| --- | --- | --- | --- | --- |
| funnction | new | Array | int size | constracts a new array of the given size. |
| method | dispose | void | - | disposes this array. |

## Output
| Type | Name | Return Value | Arguments | Description |
| --- | --- | --- | --- | --- |
| funnction | init | void | - | for internal use only. |
| funnction | moveCursor | void | int i, j | moves the cursor to the j-th column of the i-th row, and erases the character displayed there. |
| funnction | printChar | void | char c | prints c at the cursor location and advances the cursor one column forward. |
| funnction | printString | void | String s | prints s starting at the cursor location and advances the cursor appropriately. |
| funnction | printInt | void | int i | prints i starting at the cursor location and advances the cursor appropriately. |
| funnction | println | void | - | advances the cursor to the beginning of the next line. |
| funnction | backSpace | void | - | moves the cursor one column back. |


## Screen
Column indices start at 0 and are left-to-right. 
Row indices start at 0 and are top-to-bottom. 
Screen size is 256 rows by 512 columns.

| Type | Name | Return Value | Arguments | Description |
| --- | --- | --- | --- | --- |
| function | init | void | - | for internal use only. |
| function | clearScreen | void | - | erases the entire screen. 
| function | setColor | void | boolean b | sets a color (white=false, black=true) to be used for all further drawXXX commands. |
| function | drawPixel | void | int x, y | draws the (x,y) pixe. |
| function | drawLine | void | int xl, yl, x2, y2 | draws a line from (xl,yl) to (x2,y2). 
| function | drawRectangle | void | int xl, yl, x2, y2  | draws a filled rectangle whose top left corner is (x1,y1) and bottom right corner is (x2,y2). |
| function | drawCircle | void | int x, y, r | draws a filled circle of radius r <=181 around (x,y). |

## Keyboard
| Type | Name | Return Value | Arguments | Description |
| --- | --- | --- | --- | --- |
| function | init | void | - | for internal use only. |
| function | keyPressed | char | - | returns the character of the currently pressed key on the keyboard; if no key is currently pressed, returns 0. |
| function | readChar | char | - | waits until a key is pressed on the keyboard and released, then echoes the key to the screen and returns the character of the pressed ke. |
| function | readLine | String | String message | prints the message on the screen, reads the line (text until a newline character is detected) from the keyboard, echoes the line to the screen, and returns its value. This function also handles user backspaces. |
| function | readInt | int |  String message | prints the message on the screen, reads the line (text until a newline character is detected) from the keyboard, echoes the line to the screen, and returns its integer value (until the first nondigit character in the line is detected). This function also handles user backspaces. |

## Memory
| Type | Name | Return Value | Arguments | Description |
| --- | --- | --- | --- | --- |
| function | init | void | - | for internal use only. |
| function | peek | int | int address | returns the value of the main memory at this address. |
| function | poke | void | int address, value | sets the contents of the main memory at this address to value. |
| function | alloc | Array | int size | finds and allocates from the heap a memory block of the specified size and returns a reference to its base address. |
| function | deAlloc | void | Array o | De-allocates the given object and frees its memory space. |


# Sys
| Type | Name | Return Value | Arguments | Description |
| --- | --- | --- | --- | --- |
| function | init | void | - | calls the init functions of the other OS classes, then calls the Main.main() function and finally Sys.halt(). For internal use only.. |
| function | halt | void | - | halts the program execution. |
| function | error | void | int errorCode | prints the error code on the screen and halts. |
| function | wait | void | int duration | waits approximately duration milliseconds and returns. |

# Errors
| No. | Code Name | Description |
| --- | --- | --- |
| 1 | Sys.halt | Duration must be positive. |
| 2 | Array.new | Array size must be positive. |
| 3 | Math.divide | Division by zero. |
| 4 | Math.sqrt |Cannot compute square root of a negative number. |
| 5 | Memory.alloc | Allocated memory size must be positive. |
| 6 | Memory.alloc | Heap overflow. |
| 7 | Screen.drawPixel | Illegal pixel coordinates. |
| 8 | Screen.drawLine | Illegal line coordinates. |
| 9 | Screen.drawRectangle | Illegal rectangle coordinates. |
| 10 | Screen.drawCircle | Illegal center coordinates. |
| 11 | Screen.drawCircle | Illegal radius. |
| 12 | String.new | Maximum length must be non-negative. |
| 13 | String.charAt | String index out of bounds. |
| 14 | String.setCharAt | String index out of bounds. |
| 15 | String.appendChar | String is full. |
| 16 | String.eraseLastChar | String is empty. |
| 17 | String.setInt  | Insufficient string capacity. |
| 18 | Output.moveCursor | Illegal cursor location. |
