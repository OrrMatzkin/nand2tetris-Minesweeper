"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import ssl
import typing

from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    op_list = ('+', '-', '*', '/', '&', '|', '<', '>', "=", "^", "#")

    def __init__(self, input_stream: typing.TextIO,
                output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.tokenizer = JackTokenizer(input_stream)
        self.symbol_table = SymbolTable()
        self.current_class_name = None
        self.current_subroutine_name = None
        self.label_counter = 0
        self.output = output_stream
        self.vm_writer = VMWriter(output_stream)
        self.compile_class()
        # print(self.current_class_name)
        # print(self.symbol_table)

    def advance(self, n=1) -> None:
        """
        Advances the tokenizer according to a given number of times
        :param n: Number of times to advance
        """
        for _ in range(n):
            self.tokenizer.advance()

    def compile_class(self) -> None:
        """
        Compiles a complete class.
        """
        self.advance()
        self.current_class_name = self.tokenizer.get_token()
        self.advance(2)
        while self.tokenizer.get_token() in ("field", "static"):
            self.compile_class_var_dec()
        while self.tokenizer.get_token() in ("method", "function", "constructor"):
            self.compile_subroutine()
        self.advance()

    def compile_class_var_dec(self) -> None:
        """
        Compiles a static declaration or a field declaration.
        """
        token = self.tokenizer.get_token()
        self.advance()
        _type = self.tokenizer.get_token()
        while self.tokenizer.get_token() != ';':
            self.advance()
            self.symbol_table.define(self.tokenizer.get_token(), _type, token.upper())
            self.advance()
        self.advance()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        """
        self.symbol_table.start_subroutine()
        if self.tokenizer.get_token() == "constructor":
            self.advance(2)
            self.current_subroutine_name = self.tokenizer.get_token()
            self.advance()
        elif self.tokenizer.get_token() == "method":
            self.symbol_table.define("this", self.current_class_name, "ARG")
            self.advance(2)
            self.current_subroutine_name = self.tokenizer.get_token()
            self.advance()
        else:
            self.advance(2)
            self.current_subroutine_name = self.tokenizer.get_token()
            self.tokenizer.advance()
        self.advance()
        self.compile_parameter_list()
        self.advance()
        self.compile_subroutine_body()

    def compile_subroutine_body(self) -> None:
        """
        Compiles a (possibly empty) varDec and statement list, not including the
        enclosing "()".
        """
        self.advance()
        while self.tokenizer.get_token() == "var":
            self.compile_var_dec()
        self.vm_writer.write_function(self.current_class_name + '.' +
                                  self.current_subroutine_name, self.symbol_table.counter_map["VAR"])
        if self.current_subroutine_name == "new":
            self.vm_writer.write_push("CONST",
                                      self.symbol_table.counter_map["FIELD"])
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("POINTER", 0)
        elif self.symbol_table.type_of("this"):
            self.vm_writer.write_push("ARG", 0)
            self.vm_writer.write_pop("POINTER", 0)
        self.compile_statements()
        self.advance()

    def compile_parameter_list(self) -> int:
        """
        Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        n_args = 0
        while self.tokenizer.get_token() != ")":
            if self.tokenizer.get_token() == ",":
                self.advance()
            else:
                _type = self.tokenizer.get_token()
                if self.tokenizer.token_type() == "KEYWORD":
                    self.advance()
                else:
                    self.advance()
                n_args += 1
                self.symbol_table.define(self.tokenizer.get_token(), _type, "ARG")
                self.advance()
        return n_args

    def compile_var_dec(self) -> None:
        """
        Compiles a var declaration.
        """
        self.advance()
        _type = self.tokenizer.get_token()
        self.advance()
        self.symbol_table.define(self.tokenizer.get_token(), _type, "VAR")
        self.advance()
        while self.tokenizer.get_token() == ',':
            self.advance()
            self.symbol_table.define(self.tokenizer.get_token(), _type, "VAR")
            self.advance()
        self.advance()

    def compile_statements(self) -> None:
        """
        Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        while self.tokenizer.get_token() in ("let", "if", "while", "do", "return"):
            if self.tokenizer.get_token() == "let":
                self.compile_let()
            if self.tokenizer.get_token() == "if":
                self.compile_if()
            if self.tokenizer.get_token() == "while":
                self.compile_while()
            if self.tokenizer.get_token() == "do":
                self.compile_do()
                self.vm_writer.write_pop("TEMP", 0)
            if self.tokenizer.get_token() == "return":
                self.compile_return()
            self.advance()

    def compile_do(self) -> None:
        """
        Compiles a do statement.
        """
        self.advance()
        if self.tokenizer.get_token() != ";":
            self.compile_subroutine_call()
        self.advance()

    def compile_let(self) -> None:
        """
        Compiles a let statement.
        """
        is_array = False
        while self.tokenizer.get_token() != '=':
            if self.tokenizer.token_type() == "IDENTIFIER" or\
                    (self.tokenizer.token_type() == "KEYWORD"
                     and self.tokenizer.get_token() in ["this", "that"]):
                name = self.tokenizer.get_token()
                if self.tokenizer.get_next_token() == '[':
                    is_array = True
                    self.vm_writer.write_push(self.symbol_table.kind_of(name),
                                              self.symbol_table.index_of(name))
                    self.advance(2)
                    self.compile_expression()
                    self.vm_writer.write_arithmetic("+")
                    break
            self.tokenizer.advance()
        if is_array:
            self.advance(2)
        else:
            self.advance()
        self.compile_expression()
        if not is_array:
            self.vm_writer.write_pop(self.symbol_table.kind_of(name),
                                     self.symbol_table.index_of(name))
        else:
            self.vm_writer.write_pop("TEMP", 0)
            self.vm_writer.write_pop("POINTER", 1)
            self.vm_writer.write_push("TEMP", 0)
            self.vm_writer.write_pop("THAT", 0)

    def compile_while(self) -> None:
        """
        Compiles a while statement.
        """
        self.advance(2)
        label1 = self.current_subroutine_name + "." + "while-cond-true." + str(self.label_counter)
        label2 = self.current_subroutine_name + "." + "while-cond-false." + str(self.label_counter)
        self.label_counter += 1
        self.vm_writer.write_label(label1)
        self.compile_expression()
        self.vm_writer.write_arithmetic("~")
        self.vm_writer.write_if(label2)
        self.advance(2)
        self.compile_statements()
        self.vm_writer.write_goto(label1)
        self.vm_writer.write_label(label2)

    def compile_return(self) -> None:
        """
        Compiles a return statement.
        """
        self.advance()
        if self.tokenizer.get_token() != ";":
            self.compile_expression()
        else:
            self.vm_writer.write_push("CONST", 0)
        self.vm_writer.write_return()

    def compile_if(self) -> None:
        """
        Compiles a if statement, possibly with a trailing else clause.
        """
        self.advance(2)
        self.compile_expression()
        self.advance(2)
        self.vm_writer.write_arithmetic("~")
        label1 = self.current_subroutine_name + "." + "if-cond-false." + str(self.label_counter)
        label2 = self.current_subroutine_name + "." + "if-cond-true." + str(self.label_counter)
        self.label_counter += 1
        self.vm_writer.write_if(label1)
        self.compile_statements()
        self.vm_writer.write_goto(label2)
        self.vm_writer.write_label(label1)

        # if the condition has an else
        if self.tokenizer.get_next_token() == "else":
            self.advance(3)
            self.compile_statements()

        self.vm_writer.write_label(label2)

    def compile_expression(self) -> None:
        """
        Compiles an expression.
        """
        self.compile_term()
        self.advance()
        ops = []
        while self.tokenizer.get_token() in CompilationEngine.op_list:
            ops.append(self.tokenizer.get_token())
            self.advance()
            self.compile_term()
            self.advance()
        for op in ops[::-1]:
            self.vm_writer.write_arithmetic(op)

    def compile_term(self) -> None:
        """
        Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        if self.tokenizer.token_type() == "STRING_CONST":
            n_args = len(self.tokenizer.get_token())
            self.vm_writer.write_push("CONST", n_args)
            self.vm_writer.write_call("String.new", 1)
            for letter in self.tokenizer.get_token():
                self.vm_writer.write_push("CONST", ord(letter))
                self.vm_writer.write_call("String.appendChar", 2)
        elif self.tokenizer.get_token() in ('null', 'false'):
            self.vm_writer.write_push("CONST", 0)
        elif self.tokenizer.get_token() == 'true':
            self.vm_writer.write_push("CONST", 1)
            self.vm_writer.write_arithmetic("--")
        elif self.tokenizer.get_token() == 'this':
            self.vm_writer.write_push("POINTER", 0)

        # if exp is number
        elif self.tokenizer.token_type() == "INT_CONST":
            self.vm_writer.write_push("CONST", self.tokenizer.get_token())

        # unaryOP term
        elif self.tokenizer.get_token() in ('-', '~', '^', '#'):
            op_term = self.tokenizer.get_token()
            if op_term == '-':
                op_term = "--"
            self.advance()
            self.compile_term()
            self.vm_writer.write_arithmetic(op_term)

        # '(' expression ')'
        elif self.tokenizer.get_token() in ["(", "["]:
            self.advance()
            self.compile_expression()

        elif self.tokenizer.get_next_token() in ['.', '(']:
            self.compile_subroutine_call()

        # array
        elif self.tokenizer.get_next_token() == '[':
            self.vm_writer.write_push(self.symbol_table.kind_of(self.tokenizer.get_token()),
                                      self.symbol_table.index_of(self.tokenizer.get_token()))
            self.advance(2)
            self.compile_expression()
            self.vm_writer.write_arithmetic("+")
            self.vm_writer.write_pop("POINTER", 1)
            self.vm_writer.write_push("THAT", 0)
        else:
            # if exp is variable
            self.vm_writer.write_push(self.symbol_table.kind_of(self.tokenizer.get_token()), self.symbol_table.index_of(self.tokenizer.get_token()))

    def compile_subroutine_call(self) -> None:
        """
        Compiles a subroutine call.
        """
        # method
        if self.tokenizer.get_next_token() == '(':
            method_name = self.tokenizer.get_token()
            self.advance(2)
            self.vm_writer.write_push("POINTER", 0)
            n_args = self.compile_expression_list()
            self.vm_writer.write_call(self.current_class_name + "." + method_name, n_args+1)

        # function
        if self.tokenizer.get_next_token() == '.':
            object_name = self.tokenizer.get_token()
            if self.symbol_table.type_of(object_name):
                self.vm_writer.write_push(self.symbol_table.kind_of(object_name),
                                          self.symbol_table.index_of(object_name))
            self.advance(2)

            method_name = self.tokenizer.get_token()
            self.advance(2)
            n_args = self.compile_expression_list()

            if self.symbol_table.type_of(object_name):
                self.vm_writer.write_call(self.symbol_table.type_of(object_name) + "." + method_name, n_args+1)
            else:
                self.vm_writer.write_call(object_name + "." + method_name,
                                          n_args)


    def compile_expression_list(self) -> int:
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        """
        n_args = 0
        while self.tokenizer.get_token() != ')':
            self.compile_expression()
            n_args += 1
            if self.tokenizer.get_token() == ',':
                self.advance()
        return n_args