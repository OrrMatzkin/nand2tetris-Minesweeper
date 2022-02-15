"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re


class JackTokenizer:
    """
    Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    """
    keywords = ('class', 'constructor', 'function', 'method', 'field', 'static',
                'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
                'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return')
    symbols = ('{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
               '&', '|', '<', '>', '=', '~', '^', '#')
    xml_translator = {"INT_CONST": "integerConstant",
                      "STRING_CONST": "stringConstant"}
    special_symbols = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}

    def __init__(self, input_stream: typing.TextIO) -> None:
        """
        Opens the input stream and gets ready to tokenize it.
        Args:
            input_stream (typing.TextIO): input stream.
        """
        self.all_tokens = []
        self.parse_tokens(input_stream)
        self.curr_token_idx = 0

    def get_full_token(self) -> str:
        """
        Returns a full .xml line containing the current token.
        """
        if self.token_type() in JackTokenizer.xml_translator:
            token_type = JackTokenizer.xml_translator[self.token_type()]
        else:
            token_type = self.token_type().lower()
        token = self.get_token()
        if token in JackTokenizer.special_symbols:
            token = JackTokenizer.special_symbols[token]
        return "<" + token_type + "> " + token + \
               " </" + token_type + ">\n"

    def get_token(self) -> str:
        """
        Returns the current token.
        """
        if self.curr_token_idx < len(self.all_tokens):
            token = self.all_tokens[self.curr_token_idx]
            if self.token_type() == "STRING_CONST":
                token = token[1:-1]
            return token

    def get_next_token(self) -> str:
        """
        Returns the next token.
        """
        if self.curr_token_idx + 1 < len(self.all_tokens):
            return self.all_tokens[self.curr_token_idx + 1]

    def parse_tokens(self, input_stream: typing.TextIO) -> None:
        """
        This function separates the input stream into Jack's valid tokens (using
        Regex).
        :param input_stream: The stream which holds the given input.
        """
        line = input_stream.readline()
        c_regex = "^\s*(\w+)"
        s_regex = "^\s*({|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|\/|\&|\||<|>|=|~|\^|#)"
        q_regex = "^\s*(\"[^\"]*\")"
        comment_flag = False
        while line:
            start = 0
            while_flag = True
            while while_flag or symbol or chars or quote or \
                    comment or open_doco or close_doco:
                while_flag = False
                comment = re.search("^\s*\/\/", line[start:])
                open_doco = re.search("^\s*\/\*", line[start:])
                close_doco = re.search("^\s*\*\/", line[start:])
                chars = re.search(c_regex, line[start:])
                symbol = re.search(s_regex, line[start:])
                quote = re.search(q_regex, line[start:])
                if comment:
                    break
                elif open_doco:
                    comment_flag = True
                    start += open_doco.end()
                elif close_doco:
                    comment_flag = False
                    start += close_doco.end()
                elif symbol:
                    if not comment_flag:
                        self.all_tokens.append(symbol.group(1))
                    start += symbol.end()
                elif chars:
                    if not comment_flag:
                        self.all_tokens.append(chars.group(1))
                    start += chars.end()
                elif quote:
                    if not comment_flag:
                        self.all_tokens.append(quote.group(1))
                    start += quote.end()
                else:
                    if comment_flag and line.find("*/") >= 0:
                        start = line.find("*/")
                        while_flag = True
            line = input_stream.readline()

    def has_more_tokens(self) -> bool:
        """
        Do we have more tokens in the input?
        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        return self.curr_token_idx < len(self.all_tokens)

    def advance(self) -> None:
        """
        Gets the next token from the input and makes it the current token.
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        curr_token = self.all_tokens[self.curr_token_idx]
        if self.token_type() == "STRING_CONST":
            curr_token = curr_token[1:-1]
        self.curr_token_idx += 1
        return curr_token

    def token_type(self) -> str:
        """
        Returns:
        str: the type of the current token, can be
        "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        curr_token = self.all_tokens[self.curr_token_idx]
        if curr_token in JackTokenizer.keywords:
            return "KEYWORD"
        if curr_token in JackTokenizer.symbols:
            return "SYMBOL"
        if curr_token.startswith('"'):
            return "STRING_CONST"
        if curr_token.isdigit():
            return "INT_CONST"
        return "IDENTIFIER"

    def keyword(self) -> str:
        """
        Returns:
        str: the keyword which is the current token.
        Should be called only when token_type() is "KEYWORD".
        Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT",
        "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO",
        "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        return self.all_tokens[self.curr_token_idx].uppercase()

    def symbol(self) -> str:
        """
        Returns:
        str: the character which is the current token.
        Should be called only when token_type() is "SYMBOL".
        """
        return self.all_tokens[self.curr_token_idx]

    def identifier(self) -> str:
        """
        Returns:
        str: the identifier which is the current token.
        Should be called only when token_type() is "IDENTIFIER".
        """
        return self.all_tokens[self.curr_token_idx]

    def int_val(self) -> int:
        """
        Returns:
        int: the integer value of the current token.
        Should be called only when token_type() is "INT_CONST".
        """
        return int(self.all_tokens[self.curr_token_idx])

    def string_val(self) -> str:
        """
        Returns:
        str: the string value of the current token, without the double
        quotes. Should be called only when token_type() is "STRING_CONST".
        """
        return self.all_tokens[self.curr_token_idx]
