"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """
        Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_stream = output_stream
        self.filename = None
        self.label_counter = 0
        self.date_segments_to_asm = {"LOCAL": "LCL", "ARGUMENT": "ARG",
                                     "THIS": "THIS", "THAT": "THAT"}
        self.generic_push = ["@SP",
                             "A=M",
                             "M=D",
                             "@SP",
                             "M=M+1"]
        self.generic_pop = ["@SP",
                            "M=M-1",
                            "A=M",
                            "D=M",
                            "@R13",
                            "A=M",
                            "M=D"]
        self.function_calls_num = dict()
        self.function_name = ""

    def set_file_name(self, filename: str) -> None:
        """
        Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        self.filename = filename

    def write_arithmetic(self, command: str) -> None:
        """
        Writes the assembly code that is the translation of the given
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        jack_to_asm = {"add": ["// ADD",
                               "@SP",
                               "A=M-1",
                               "D=M",
                               "A=A-1",
                               "M=M+D",
                               "@SP",
                               "M=M-1"],
                       "sub": ["// SUB",
                               "@SP",
                               "A=M-1",
                               "D=M",
                               "A=A-1",
                               "M=M-D",
                               "@SP",
                               "M=M-1"],
                       "neg": ["// NEG",
                               "@SP",
                               "A=M-1",
                               "D=M",
                               "M=-D"],
                       "eq": ["// EQUAL",
                              "@SP",
                              "A=M-1",
                              "D=M",
                              "A=A-1",
                              "M=M-D",
                              "D=M",
                              "@TRUE" + str(self.label_counter),
                              "D;JEQ",
                              " ",
                              "@SP",
                              "A=M-1",
                              "D=M",
                              "A=A-1",
                              "M=0",
                              "@END" + str(self.label_counter),
                              "0;JMP",
                              " ",
                              "(TRUE" + str(self.label_counter) + ")",
                              "@SP",
                              "A=M-1",
                              "D=M",
                              "A=A-1",
                              "M=-1",
                              " ",
                              "(END" + str(self.label_counter) + ")",
                              "@SP",
                              "M=M-1"],
                       "gt": ["// GT",
                              "@SP",
                              "A=M-1",
                              "A=A-1",
                              "D=M",
                              "@X_NEG" + str(self.label_counter),
                              "D;JLT",

                              "@SP",
                              "A=M-1",
                              "D=M",
                              "@SAME_SIGN" + str(self.label_counter),
                              "D;JGT",

                              "@TRUE" + str(self.label_counter),
                              "0;JMP",

                              "(X_NEG" + str(self.label_counter) + ")",
                              "@SP",
                              "A=M-1",
                              "D=M",
                              "@FALSE" + str(self.label_counter),
                              "D;JGT",

                              "(SAME_SIGN" + str(self.label_counter) + ")",
                              "@SP",
                              "A=M-1",
                              "D=M",
                              "A=A-1",
                              "M=M-D",
                              "D=M",
                              "@TRUE" + str(self.label_counter),
                              "D;JGT",

                              "(FALSE" + str(self.label_counter) + ")",
                              "@SP",
                              "A=M-1",
                              "D=M",
                              "A=A-1",
                              "M=0",
                              "@END" + str(self.label_counter),
                              "0;JMP",

                              "(TRUE" + str(self.label_counter) + ")",
                              "@SP",
                              "A=M-1",
                              "D=M",
                              "A=A-1",
                              "M=-1",

                              "(END" + str(self.label_counter) + ")",
                              "@SP",
                              "M=M-1"],
                       "lt": ["// LT",
                              "@SP",
                              "A=M-1",
                              "A=A-1",
                              "D=M",
                              "@X_NEG" + str(self.label_counter),
                              "D;JLT",

                              "@SP",
                              "A=M-1",
                              "D=M",
                              "@SAME_SIGN" + str(self.label_counter),
                              "D;JGT",

                              "@FALSE" + str(self.label_counter),
                              "0;JMP",

                              "(X_NEG" + str(self.label_counter) + ")",
                              "@SP",
                              "A=M-1",
                              "D=M",
                              "@TRUE" + str(self.label_counter),
                              "D;JGT",

                              "(SAME_SIGN" + str(self.label_counter) + ")",
                              "@SP",
                              "A=M-1",
                              "D=M",
                              "A=A-1",
                              "M=M-D",
                              "D=M",
                              "@TRUE" + str(self.label_counter),
                              "D;JLT",

                              "(FALSE" + str(self.label_counter) + ")",
                              "@SP",
                              "A=M-1",
                              "D=M",
                              "A=A-1",
                              "M=0",
                              "@END" + str(self.label_counter),
                              "0;JMP",

                              "(TRUE" + str(self.label_counter) + ")",
                              "@SP",
                              "A=M-1",
                              "D=M",
                              "A=A-1",
                              "M=-1",

                              "(END" + str(self.label_counter) + ")",
                              "@SP",
                              "M=M-1"],
                       "and": ["// AND",
                               "@SP",
                               "A=M-1",
                               "D=M",
                               "A=A-1",
                               "M=M&D",
                               "@SP",
                               "M=M-1"],
                       "or": ["// OR",
                              "@SP",
                              "A=M-1",
                              "D=M",
                              "A=A-1",
                              "M=M|D",
                              "@SP",
                              "M=M-1"],
                       "not": ["// NOT",
                               "@SP",
                               "A=M-1",
                               "M=!M",
                               ],
                       "shiftleft": ["// SHIFT LEFT",
                                     "@SP",
                                     "A=M-1",
                                     "M=M<<"],
                       "shiftright": ["// SHIFT RIGHT",
                                      "@SP",
                                      "A=M-1",
                                      "M=M>>"]
                       }
        asm_command = jack_to_asm[command]
        for line in asm_command:
            self.output_stream.write(line + '\n')
        self.output_stream.write('\n')
        self.label_counter += 1

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """
        Writes the assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        if command == "C_PUSH":
            asm_command = self.get_push_command(segment, index)
        else:
            asm_command = self.get_pop_command(segment, index)
        for line in asm_command:
            self.output_stream.write(line + '\n')
        self.output_stream.write('\n')

    def get_push_command(self, segment: str, index: int) -> list:
        """
        This method contracts the appropriate .asm push command.

        Args:
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.

        Return:
            the .asm command.
        """
        if segment == "CONSTANT":
            segment_lst = ["// push constant " + str(index),
                           "@" + str(index),
                           "D=A"]
        elif segment == "STATIC":
            segment_lst = ["// push static " + str(index),
                           "@" + self.filename + "." + str(index),
                           "D=M"]
        elif segment == "TEMP":
            segment_lst = ["// pop temp " + str(index),
                           "@" + str(index),
                           "D=A",
                           "@5",
                           "A=A+D",
                           "D=M"]
        elif segment == "POINTER":
            if index == 0:
                segment_lst = ["// push pointer this",
                               "@THIS",
                               "D=M"]
            else:
                segment_lst = ["// push pointer that",
                               "@THAT",
                               "D=M"]
        elif segment in self.date_segments_to_asm:
            segment_lst = [
                "// push " + segment.lower() + " " + str(index),
                "@" + str(index),
                "D=A",
                "@" + self.date_segments_to_asm[segment],
                "A=M+D",
                "D=M"]

        return segment_lst + self.generic_push

    def get_pop_command(self, segment: str, index: int):
        """
        This method contracts the appropriate .asm pop command.

        Args:
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.

        Return:
             the .asm command.
        """
        if segment == "STATIC":
            segment_lst = ["// pop static " + str(index),
                           "@" + self.filename + "." + str(index),
                           "D=A",
                           "@R13",
                           "M=D"]
        elif segment == "TEMP":
            segment_lst = ["// pop temp " + str(index),
                           "@" + str(5 + index),
                           "D=A",
                           "@R13",
                           "M=D"]
        elif segment == "POINTER":
            if index == 0:
                segment_lst = ["// pop pointer this",
                               "@SP",
                               "M=M-1",
                               "A=M",
                               "D=M",
                               "@THIS",
                               "M=D"]
            else:
                segment_lst = ["// pop pointer that",
                               "@SP",
                               "M=M-1",
                               "A=M",
                               "D=M",
                               "@THAT",
                               "M=D"]
            return segment_lst
        elif segment in self.date_segments_to_asm:
            segment_lst = [
                "// pop " + segment.lower() + " " + str(index),
                "@" + str(index),
                "D=A",
                "@" + self.date_segments_to_asm[segment],
                "A=M+D",
                "D=A",
                "@R13",
                "M=D"]

        return segment_lst + self.generic_pop

    def write_lines(self, lines: list) -> None:
        """
        Write the given lines to the output .asm file.

        Args:
            lines: the line to write.
        """
        for line in lines:
            self.output_stream.write(line + '\n')
        self.output_stream.write('\n')

    def write_label(self, label: str) -> None:
        """
        Writes a the given label to the output asm file.

        Args:
            label (str): the name of the label.
        """
        write_label_lines = ["// Writing Label " + label,
                             "(" + label + ")"]
        self.write_lines(write_label_lines)

    def write_goto(self, label: str) -> None:
        """
        Write the goto part to the output asm file.

        Args:
            label (str): the label to go to.
        """
        write_goto_lines = ["// Writing goto " + label,
                            "@" + label,
                            "0;JMP"]
        self.write_lines(write_goto_lines)

    def write_if(self, label: str) -> None:
        """
        Write the if-goto part to the output asm file.

        Args:
            label (str): the label to go to.
        """
        write_if_lines = ["// Writing if " + label,
                        "@SP",
                        "M=M-1",
                        "A=M",
                        "D=M",
                        "@" + label,
                        "D;JNE"]
        self.write_lines(write_if_lines)

    def write_call(self, function_name: str, num_args: int) -> None:
        """
        Write the call function part to the output asm file.

        Args:
            function_name (str): the function name to go to.
            num_args (int): the number of arguments to call the function with.
        """
        write_call_lines = ["// Writing call " + function_name + str(num_args),
                            "@" + function_name + "$ret." + str(self.function_calls_num[function_name]),
                            "D=A"]
        write_call_lines += self.generic_push

        for memory in ["LCL", "ARG", "THIS", "THAT"]:
            write_call_lines += ["\n// push " + memory,
                                 "@" + memory,
                                 "D=M"]
            write_call_lines += self.generic_push

        write_call_lines += ["\n// Repositions ARG",
                             "@SP",
                             "D=M",
                             "@5",
                             "D=D-A",
                             "@" + str(num_args),
                             "D=D-A",
                             "@ARG",
                             "M=D",
                             "\n// Repositions LCL",
                             "@SP",
                             "D=M",
                             "@LCL",
                             "M=D"]

        self.write_lines(write_call_lines)
        self.write_goto(function_name)
        self.output_stream.write("(" + function_name + "$ret." +
                                 str(self.function_calls_num[function_name]) + ')\n\n')

    def write_function(self, function_name: str, num_args: int) -> None:
        """
        Write the function declaration part to the output asm file.

        Args:
            function_name (str): the function name to go to.
            num_args (int): the number of arguments to call the function with.
        """
        write_function_lines = ["// writing function " + function_name + " " + str(num_args)]
        self.function_name = function_name
        self.write_lines(write_function_lines)
        self.write_label(function_name)
        write_function_lines = ["@" + str(num_args),
                                "D=A",
                                "@R13",
                                "M=D",
                                "(LOOP_" + function_name + ")",
                                "@END_LOOP_" + function_name,
                                "D;JEQ"]
        self.write_lines(write_function_lines)
        self.write_push_pop("C_PUSH", "CONSTANT", 0)
        write_function_lines = ["@R13",
                                "M=M-1",
                                "D=M"]
        self.write_lines(write_function_lines)
        write_function_lines = ["@LOOP_" + function_name,
                                "0;JMP",
                                "(END_LOOP_" + function_name + ")"]
        self.write_lines(write_function_lines)

    def write_return(self) -> None:
        """
        Write the return function part to the output asm file.
        """
        write_function_lines = ["// writing return",
                                "// endFrame = LCL",
                                "@LCL",
                                "D=M",
                                "@R14",
                                "M=D",
                                "",
                                "// retAddr = *(endFrame - 5)",
                                "@R14",
                                "D=M",
                                "@5",
                                "A=D-A",
                                "D=M",
                                "@R15",
                                "M=D",
                                "",
                                "// *ARG = pop()",
                                "@SP",
                                "M=M-1",
                                "A=M",
                                "D=M",
                                "@ARG",
                                "A=M",
                                "M=D",
                                "",
                                "// SP = ARG + 1",
                                "@ARG",
                                "D=M+1",
                                "@SP",
                                "M=D",
                                ""]
        for memory in ["THAT", "THIS", "ARG", "LCL"]:
            write_function_lines += ["\n@R14",
                                     "M=M-1",
                                     "A=M",
                                     "D=M",
                                     "@" + memory,
                                     "M=D"]

        write_function_lines += ["\n// goto retAddr",
                                 "@R15",
                                 "A=M",
                                 "0;JMP"]
        self.write_lines(write_function_lines)
        # self.function_name = ""

    def write_bootstrap(self) -> None:
        """
        Writes the bootstrap part to the output asm file.
        Bootstrap includes:
            1. set up SP to 256
            2. call Sys.main (with zero args)
        """
        self.function_calls_num["Sys.init"] = 0
        bootstrap_lines = ["// Writing bootstrap",
                           "@256",
                           "D=A",
                           "@SP",
                           "M=D"]
        self.write_lines(bootstrap_lines)
        self.write_call("Sys.init", 0)

    def close(self) -> None:
        """Closes the output file."""
        self.output_stream.close()
