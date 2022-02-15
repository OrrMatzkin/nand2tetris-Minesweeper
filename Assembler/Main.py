"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    parser = Parser(input_file)
    symbol_table = SymbolTable()
    first_pass(parser, symbol_table)
    second_pass(parser, symbol_table, output_file)


def second_pass(parser: Parser, symbol_table: SymbolTable, output_file: typing.TextIO) -> None:
    """
    This function passes threw the .asm code lines and converts it into hack
    language code.
    :param parser: The input's Parser.
    :param symbol_table: The input's Symbol_Table.
    :param output_file: An empty .hack file.
    """
    parser.initialize_line_num()
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == "A_COMMAND":
            if parser.symbol().isnumeric():
                output_file.write(Code.create_A_instruction(int(parser.symbol())))
                output_file.write("\n")
            else:
                if not symbol_table.contains(parser.symbol()):
                    symbol_table.add_entry(parser.symbol(), symbol_table.next_empty_memory)
                    symbol_table.update_next_empty_memory()
                output_file.write(Code.create_A_instruction(int(symbol_table.get_address(parser.symbol()))))
                output_file.write("\n")
        elif parser.command_type() == "C_COMMAND":
            output_file.write(Code.create_C_instruction(parser.dest(), parser.comp(), parser.jump()))
            output_file.write("\n")


def first_pass(parser: Parser, symbol_table: SymbolTable) -> None:
    """
    This function passes threw the .asm code lines and updates the symbol_table
    accordingly.
    :param parser: The input's Parser.
    :param symbol_table: The input's Symbol_Table.
    """
    counter = 0
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == "L_COMMAND":
            symbol_table.add_entry(parser.symbol(), counter)
        else:
            counter += 1


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
