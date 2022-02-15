"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        self.arithmetic_operands = {'add', 'sub', 'neg', 'eq', 'gt', 'lt',
                                    'and', 'or', 'not', 'shiftleft', 'shiftright'}
        self.non_arithmetic_commands = {"push": "C_PUSH", "pop": "C_POP",
                                        "label": "C_LABEL", "goto": "C_GOTO",
                                        "if-goto": "C_IF",
                                        "function": "C_FUNCTION",
                                        "call": "C_CALL", "return": "C_RETURN"}
        self.input_lines = input_file.read().splitlines()
        self.line_num = 0
        self.curr_instruction = None

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.line_num < len(self.input_lines)

    def advance(self) -> None:
        """
        Reads the next command from the input and makes it the current
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        while self.has_more_commands() and (self.input_lines[self.line_num].isspace()
            or self.input_lines[self.line_num].startswith("//") or self.input_lines[self.line_num] == ""):
            self.line_num += 1
        if self.has_more_commands():
            self.curr_instruction = self.input_lines[self.line_num].split("//")[0].strip()
        else:
            self.curr_instruction = "EOF"
        self.line_num += 1

    def command_type(self) -> str:
        """
        Returns the command type.

        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        command_word = self.curr_instruction.split()[0]
        if command_word in self.arithmetic_operands:
            return "C_ARITHMETIC"
        elif command_word in self.non_arithmetic_commands:
            return self.non_arithmetic_commands[command_word]
        else:
            return "ERROR"

    def arg1(self) -> str:
        """
        Returns the first argument of the command.

        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        return self.curr_instruction.split()[1]

    def arg2(self) -> int:
        """
        Returns the second argument of the command.

        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        return int(self.curr_instruction.split()[2])
