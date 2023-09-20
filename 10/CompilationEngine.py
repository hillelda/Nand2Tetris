"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

from JackTokenizer import JackTokenizer


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.tokenizer = input_stream
        self.output = output_stream
        self.num_of_tabs = 0

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.output.write("<class>\n")
        self.tokenizer.advance()
        self.num_of_tabs += 1
        self.write_keyword()
        self.write_identifier()
        self.write_symbol()

        while self.tokenizer.keyword().lower() == "field" or self.tokenizer.keyword().lower() == "static":
            self.compile_class_var_dec()

        while self.tokenizer.keyword().lower() == "constructor" or self.tokenizer.keyword().lower() == "function" or \
                self.tokenizer.keyword().lower() == "method":
            self.compile_subroutine()

        self.write_symbol()
        self.num_of_tabs -= 1
        self.output.write("</class>\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.output.write("\t" * self.num_of_tabs + "<classVarDec>\n")
        self.num_of_tabs += 1
        self.write_keyword()  # static / field
        self.write_type()

        self.write_identifier()  # var name
        while self.tokenizer.symbol() == ",":
            self.write_symbol()
            self.write_identifier()

        self.write_symbol()
        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</classVarDec>\n")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.output.write("\t" * self.num_of_tabs + "<subroutineDec>\n")
        self.num_of_tabs += 1
        self.write_keyword()
        self.write_type()
        self.write_identifier()  # subroutine name
        self.write_symbol()  # (
        self.compile_parameter_list()
        self.write_symbol()  # )
        self.output.write("\t" * self.num_of_tabs + "<subroutineBody>\n")
        self.num_of_tabs += 1
        self.write_symbol()

        if self.tokenizer.token_type() == "KEYWORD":  # VarDec
            while self.tokenizer.keyword() == "VAR":
                self.compile_var_dec()
        if self.tokenizer.token_type() == "KEYWORD":  # statements
            self.compile_statements()
        self.write_symbol()

        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</subroutineBody>\n")
        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</subroutineDec>\n")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        self.output.write("\t" * self.num_of_tabs + "<parameterList>\n")
        self.num_of_tabs += 1
        while self.tokenizer.token_type() != "SYMBOL":

            self.write_type()
            if self.tokenizer.symbol() == ",":  # while loop will start again
                self.write_symbol()

        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</parameterList>\n")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.output.write("\t" * self.num_of_tabs + "<varDec>\n")
        self.num_of_tabs += 1

        self.write_keyword()  # var
        self.write_type()
        while self.tokenizer.token_type() != "SYMBOL":
            self.write_identifier()
            if self.tokenizer.symbol() == ",":  # while loop will start again
                self.write_symbol()

        self.write_symbol()  # ;
        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self.output.write("\t" * self.num_of_tabs + "<statements>\n")
        self.num_of_tabs += 1
        while self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() == "LET":
                self.compile_let()
            elif self.tokenizer.keyword() == "DO":
                self.compile_do()
            elif self.tokenizer.keyword() == "IF":
                self.compile_if()
            elif self.tokenizer.keyword() == "WHILE":
                self.compile_while()
            elif self.tokenizer.keyword() == "RETURN":
                self.compile_return()
            else:
                print("BAD STATEMENT :(\n")

        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</statements>\n")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.output.write("\t" * self.num_of_tabs + "<doStatement>\n")
        self.num_of_tabs += 1
        self.write_keyword()
        self.write_identifier()  # subroutine call's name
        self.compile_subroutine_call()
        self.write_symbol()  # ;
        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</doStatement>\n")

    def compile_subroutine_call(self) -> None:
        """without the identifier at the beginning"""
        if self.tokenizer.symbol() == ".":
            self.write_symbol()
            self.write_identifier()
        self.write_symbol()
        self.compile_expression_list()
        self.write_symbol()

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.output.write("\t" * self.num_of_tabs + "<letStatement>\n")
        self.num_of_tabs += 1
        self.write_keyword()  # let
        self.write_identifier()

        if self.tokenizer.symbol() == "[":
            self.write_symbol()  # [
            self.compile_expression()
            self.write_symbol()  # ]

        self.write_symbol()  # '='
        self.compile_expression()
        self.write_symbol()  # ;

        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</letStatement>\n")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.output.write("\t" * self.num_of_tabs + "<whileStatement>\n")
        self.num_of_tabs += 1
        self.write_keyword()  # while

        self.write_symbol()
        self.compile_expression()
        self.write_symbol()
        self.write_symbol()
        self.compile_statements()
        self.write_symbol()

        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.output.write("\t" * self.num_of_tabs + "<returnStatement>\n")
        self.num_of_tabs += 1
        self.write_keyword()

        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ";":
            self.compile_expression()

        self.write_symbol()

        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.output.write("\t" * self.num_of_tabs + "<ifStatement>\n")
        self.num_of_tabs += 1
        self.write_keyword()  # if

        self.write_symbol()
        self.compile_expression()
        self.write_symbol()  # )
        self.write_symbol()  # {
        self.compile_statements()
        self.write_symbol()

        if self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "ELSE":
            self.write_keyword()  # else
            self.write_symbol()  # {
            self.compile_statements()
            self.write_symbol()

        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</ifStatement>\n")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        arr = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
        self.output.write("\t" * self.num_of_tabs + "<expression>\n")
        self.num_of_tabs += 1

        self.compile_term()
        while self.tokenizer.symbol() in arr:
            self.write_symbol()
            self.compile_term()

        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</expression>\n")

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        self.output.write("\t" * self.num_of_tabs + "<term>\n")
        self.num_of_tabs += 1

        if self.tokenizer.token_type() == "INT_CONST":
            self.write_int_constant()
        elif self.tokenizer.token_type() == "STRING_CONST":
            self.write_str_const()
        elif self.tokenizer.token_type() == "KEYWORD":
            self.write_keyword()
        elif self.tokenizer.token_type() == "IDENTIFIER":
            self.write_identifier()
            if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() != ";":
                if self.tokenizer.symbol() == "(" or self.tokenizer.symbol() == ".":
                    self.compile_subroutine_call()
                elif self.tokenizer.symbol() == "[":
                    self.write_symbol()
                    self.compile_expression()
                    self.write_symbol()
        elif self.tokenizer.token_type() == "SYMBOL":

            token = self.tokenizer.symbol()
            if token == "~" or token == "-" or token == '^' or token == '#':
                self.write_symbol()
                self.compile_term()
            else:
                self.write_symbol()   # (expression)
                self.compile_expression()
                self.write_symbol()

        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</term>\n")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.output.write("\t" * self.num_of_tabs + "<expressionList>\n")
        self.num_of_tabs += 1

        if not (self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ")"):
            self.compile_expression()
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self.write_symbol()
            self.compile_expression()

        self.num_of_tabs -= 1
        self.output.write("\t" * self.num_of_tabs + "</expressionList>\n")

    def write_keyword(self) -> None:
        self.output.write("\t" * self.num_of_tabs + "<keyword> " + self.tokenizer.keyword().lower() + " </keyword>\n")
        self.tokenizer.advance()

    def write_symbol(self) -> None:
        special_symbols = {'>': "&gt;", '<': "&lt;", "&": "&amp;"}
        token = self.tokenizer.symbol()
        if token in special_symbols:
            token = special_symbols.get(token)
        self.output.write("\t" * self.num_of_tabs + "<symbol> " + token + " </symbol>\n")
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def write_identifier(self) -> None:
        self.output.write("\t" * self.num_of_tabs + "<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
        self.tokenizer.advance()

    def write_int_constant(self) -> None:
        self.output.write("\t" * self.num_of_tabs + "<integerConstant> " + self.tokenizer.int_val() +
                          " </integerConstant>\n")
        self.tokenizer.advance()

    def write_str_const(self) -> None:
        self.output.write("\t" * self.num_of_tabs + "<stringConstant> " + self.tokenizer.string_val() +
                          " </stringConstant>\n")
        self.tokenizer.advance()

    def write_type(self):
        if self.tokenizer.token_type().lower() == "keyword":
            self.write_keyword()  # type
        else:
            self.write_identifier()  # type if a class
