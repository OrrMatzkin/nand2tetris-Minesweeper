"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter


def translate_file(input_file: typing.TextIO) -> None:
    """
    Translates a single file.
    Args:
        input_file (typing.TextIO): the file to translate.
    """
    code_writer.set_file_name(os.path.splitext(os.path.basename(input_file.name))[0])
    while parser.has_more_commands():
        parser.advance()
        if parser.curr_instruction == "EOF":
            break
        if parser.command_type() == "C_ARITHMETIC":
            code_writer.write_arithmetic(parser.curr_instruction)
            continue
        elif parser.command_type() in {"C_POP", "C_PUSH"}:
            split = parser.curr_instruction.split()
            segment, index = split[1].upper(), split[2]
            code_writer.write_push_pop(parser.command_type(), segment, int(index))
            continue
        elif parser.command_type() == "C_LABEL":
            code_writer.write_label(code_writer.function_name + "." + parser.curr_instruction.split()[1])
            continue
        elif parser.command_type() == "C_GOTO":
            code_writer.write_goto(code_writer.function_name + "." + parser.curr_instruction.split()[1])
            continue
        elif parser.command_type() == "C_IF":
            code_writer.write_if(code_writer.function_name + "." + parser.curr_instruction.split()[1])
            continue
        elif parser.command_type() == "C_RETURN":
            code_writer.write_return()
            continue
        split = parser.curr_instruction.split()
        function_name, num_args = split[1], split[2]
        if parser.command_type() == "C_CALL":
            if function_name in code_writer.function_calls_num:
                code_writer.function_calls_num[function_name] += 1
            else:
                code_writer.function_calls_num[function_name] = 0
            code_writer.write_call(function_name, num_args)
        elif parser.command_type() == "C_FUNCTION":
            code_writer.write_function(function_name, num_args)


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"

    with open(output_path, 'w') as output_file:
        code_writer = CodeWriter(output_file)
        code_writer.write_bootstrap()
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                parser = Parser(input_file)
                translate_file(input_file)
        code_writer.close()

