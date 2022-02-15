"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads and assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        self.input_lines = input_file.read().splitlines()
        self.line_num = 0
        self.curr_instruction = None

    def initialize_line_num(self):
        self.line_num = 0
        self.curr_instruction = None


    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.line_num < len(self.input_lines)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        # print(self.curr_instruction)
        self.curr_instruction = self.input_lines[self.line_num].split("//")[0]
        while (self.curr_instruction == "" or
               self.curr_instruction.strip().startswith("//"))\
                and self.has_more_commands():
            self.line_num += 1
            self.curr_instruction = self.input_lines[self.line_num]
        self.line_num += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        starts_with = self.curr_instruction.strip()[0]
        if starts_with == "@":
            return "A_COMMAND"
        elif starts_with == "(":
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        starts_with = self.curr_instruction.strip()[0]
        if starts_with == "@":
            return self.curr_instruction.strip()[1:]
        elif starts_with == "(":
            return self.curr_instruction.strip()[1:-1]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        equal_idx = self.curr_instruction.find("=")
        if equal_idx != -1:
            return self.curr_instruction[:equal_idx].strip()
        else:
            return ""

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        equal_idx = self.curr_instruction.find("=")
        comma_idx = self.curr_instruction.find(";")
        if comma_idx == -1:
            comma_idx = len(self.curr_instruction)
        return self.curr_instruction[equal_idx + 1:comma_idx].strip()

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        comma_idx = self.curr_instruction.find(";")
        if comma_idx != -1:
            return self.curr_instruction[comma_idx + 1:].strip()
        else:
            return ""