"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter


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
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(output_stream)
        self.current_class_name = "DEFAULT_CLASS_NAME"
        self.label_index = 0

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.tokenizer.advance()
        self.num_of_tabs += 1
        self.give_keyword()
        self.current_class_name = self.give_identifier()
        self.give_symbol()

        while self.tokenizer.keyword().lower() == "field" or self.tokenizer.keyword().lower() == "static":
            self.compile_class_var_dec()

        while self.tokenizer.keyword().lower() == "constructor" or self.tokenizer.keyword().lower() == "function" or \
                self.tokenizer.keyword().lower() == "method":
            self.compile_subroutine()

        self.give_symbol()

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.output.write("//\t" * self.num_of_tabs + "<classVarDec>\n")
        cur_kind = self.give_keyword()  # static / field
        cur_type = self.give_type()  # int bool CLASS_NAME etc.
        cur_name = self.give_identifier()  # var name
        self.symbol_table.define(cur_name, cur_type, cur_kind)

        while self.tokenizer.symbol() == ",":
            self.give_symbol()
            cur_name = self.give_identifier()
            self.symbol_table.define(cur_name, cur_type, cur_kind)

        self.give_symbol()
        self.output.write("//\t" * self.num_of_tabs + "</classVarDec>\n")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.symbol_table.start_subroutine()  # clean sub_table
        self.output.write("//" + "\t" * self.num_of_tabs + "<subroutineDec>\n")
        cur_function_type = self.give_keyword()  # type of subroutine
        if cur_function_type == "METHOD":
            self.symbol_table.define("this", self.current_class_name, "ARG")
        cur_return_type = self.give_type()
        cur_function_name = self.give_identifier()  # subroutine name
        self.give_symbol()  # (
        self.compile_parameter_list()
        self.give_symbol()  # )
        self.num_of_tabs += 1
        self.give_symbol()

        if self.tokenizer.token_type() == "KEYWORD":  # VarDec
            while self.tokenizer.keyword() == "VAR":
                self.compile_var_dec()
        self.vm_writer.write_function(self.current_class_name + "." + cur_function_name,
                                      self.symbol_table.var_count("VAR"))

        if cur_function_type == "METHOD":
            self.vm_writer.write_push("ARG", 0)
            self.vm_writer.write_pop("POINTER", 0)

        elif cur_function_type == "CONSTRUCTOR":
            num_of_class_vars = self.symbol_table.var_count("FIELD")
            self.vm_writer.write_push("CONST", num_of_class_vars)
            self.vm_writer.write_call("Memory.alloc ", 1)
            self.vm_writer.write_pop("POINTER", 0)

        if self.tokenizer.token_type() == "KEYWORD":  # statements
            self.compile_statements()
        self.give_symbol()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.output.write("//" + "\t" * self.num_of_tabs + "<parameterList>\n")
        while self.tokenizer.token_type() != "SYMBOL":
            cur_type = self.give_type()
            cur_name = self.give_identifier()
            self.symbol_table.define(cur_name, cur_type, "ARG")
            if self.tokenizer.symbol() == ",":  # while loop will start again
                self.give_symbol()

        self.output.write("//"+"\t" * self.num_of_tabs + "<subroutineBody>\n")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.output.write("//"+"\t" * self.num_of_tabs + "<varDec>\n")
        self.give_keyword()  # var
        cur_type = self.give_type()
        while self.tokenizer.token_type() != "SYMBOL":
            cur_name = self.give_identifier()
            self.symbol_table.define(cur_name, cur_type, "VAR")
            if self.tokenizer.symbol() == ",":  # while loop will start again
                self.give_symbol()

        self.give_symbol()  # ;
        self.output.write("//" + "\t" * self.num_of_tabs + "</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
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

    def compile_do(self) -> None:
        """Compiles a do statement."""

        self.give_keyword()
        cur_name = self.give_identifier()  # subroutine call's name
        self.compile_subroutine_call(cur_name)
        self.give_symbol()  # ;
        self.vm_writer.write_pop("TEMP", 0)  # do is using a void func

    def compile_subroutine_call(self, cur_name: str) -> None:
        """without the identifier at the beginning"""
        num_of_expressions = 0
        cur_class_name = self.current_class_name
        is_object = False

        if cur_name in self.symbol_table.subroutine_symbol_table or cur_name in self.symbol_table.class_symbol_table:
            num_of_expressions += 1
            is_object = True
            cur_class_name = self.symbol_table.type_of(cur_name)
            self.vm_writer.write_push(self.symbol_table.kind_of(cur_name), self.symbol_table.index_of(cur_name))

        if self.tokenizer.symbol() != ".":
            num_of_expressions += 1
            self.vm_writer.write_push("POINTER", 0)

        elif self.tokenizer.symbol() == ".":
            self.give_symbol()
            if not is_object:
                cur_class_name = cur_name
            cur_name = self.give_identifier()

        else:
            print("\nBAD COMPILE SUB_ROUTINE :(\n")

        self.give_symbol()
        num_of_expressions += self.compile_expression_list()
        self.give_symbol()
        self.vm_writer.write_call(cur_class_name + "." + cur_name, num_of_expressions)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.give_keyword()  # let
        var_name = self.give_identifier()
        var_idx = self.symbol_table.index_of(var_name)
        var_seg = self.symbol_table.kind_of(var_name)
        if var_seg == "VAR":
            var_seg = "LOCAL"

        if self.tokenizer.symbol() == "[":
            self.give_symbol()  # [
            self.vm_writer.write_push(var_seg, var_idx)
            self.compile_expression()
            self.vm_writer.write_arithmetic("ADD")
            self.give_symbol()  # ]

            self.give_symbol()  # '='
            self.compile_expression()
            self.vm_writer.write_pop("TEMP", 0)
            self.vm_writer.write_pop("POINTER", 1)
            self.vm_writer.write_push("TEMP", 0)
            self.vm_writer.write_pop("THAT", 0)
            self.give_symbol()  # ;

        else:
            self.give_symbol()  # '='
            self.compile_expression()
            self.give_symbol()  # ;

            self.vm_writer.write_pop(var_seg, var_idx)  # save info to var

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.give_keyword()  # while
        self.give_symbol()
        cur_label_index = self.label_index
        self.vm_writer.write_label(self.current_class_name + ".WHILE" + str(cur_label_index))
        self.compile_expression()
        self.vm_writer.write_arithmetic("NOT")
        self.vm_writer.write_if(self.current_class_name + ".END_WHILE" + str(cur_label_index))

        self.give_symbol()
        self.give_symbol()

        self.label_index += 1

        self.compile_statements()
        self.give_symbol()

        self.vm_writer.write_goto(self.current_class_name + ".WHILE" + str(cur_label_index))
        self.vm_writer.write_label(self.current_class_name + ".END_WHILE" + str(cur_label_index))

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.give_keyword()

        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ";":
            self.compile_expression()
        else:
            self.vm_writer.write_push("CONST", 0)

        self.vm_writer.write_return()
        self.give_symbol()

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        cur_label_index = self.label_index
        self.give_keyword()  # if
        self.give_symbol()

        self.compile_expression()
        self.vm_writer.write_arithmetic("NOT")
        self.vm_writer.write_if(self.current_class_name + ".ELSE" + str(cur_label_index))
        self.give_symbol()  # )
        self.give_symbol()  # {

        self.label_index += 1
        self.compile_statements()
        self.give_symbol()

        self.vm_writer.write_goto(self.current_class_name + ".END_IF" + str(cur_label_index))

        self.vm_writer.write_label(self.current_class_name + ".ELSE" + str(cur_label_index))

        if self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "ELSE":
            self.give_keyword()  # else
            self.give_symbol()  # {
            self.label_index += 1
            self.compile_statements()
            self.give_symbol()

        self.vm_writer.write_label(self.current_class_name + ".END_IF" + str(cur_label_index))

    def compile_expression(self) -> None:
        """Compiles an expression."""
        op_map = {'+': "ADD", '-': "SUB", '*': "Math.multiply", '/': "Math.divide", '&': "AND", '|': "OR",
                  '<': "LT", '>': "GT", '=': "EQ", "&gt;": "GT", "&lt;": "LT", "&amp;": "AND"}
        self.num_of_tabs += 1

        self.compile_term()

        while self.tokenizer.symbol() in op_map:
            symbol = self.give_symbol()
            self.compile_term()
            if symbol == "*":
                self.vm_writer.write_call(op_map.get(symbol), 2)
            elif symbol == "/":
                self.vm_writer.write_call(op_map.get(symbol), 2)
            else:
                self.vm_writer.write_arithmetic(op_map.get(symbol))

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

        unary_map = {
            "-": "NEG", "~": "NOT", '^': "SHIFTLEFT", '#': "SHIFTRIGHT"}

        if self.tokenizer.token_type() == "INT_CONST":
            cur_int = self.give_int_constant()
            self.vm_writer.write_push("CONST", int(cur_int))
        elif self.tokenizer.token_type() == "STRING_CONST":
            current_str = self.give_str_const()
            self.vm_writer.write_push("CONST", len(current_str))
            self.vm_writer.write_call("String.new", 1)
            self.vm_writer.write_pop("TEMP", 0)
            for i in current_str:
                self.vm_writer.write_push("TEMP", 0)
                self.vm_writer.write_push("CONST", ord(i))
                self.vm_writer.write_call("String.appendChar", 2)
                self.vm_writer.write_pop("TEMP", 0)

            self.vm_writer.write_push("TEMP", 0)

        elif self.tokenizer.token_type() == "KEYWORD":
            current_keyword = self.give_keyword()
            if current_keyword == "TRUE":
                self.vm_writer.write_push("CONST", 1)
                self.vm_writer.write_arithmetic("NEG")
            elif current_keyword == "FALSE" or current_keyword == "NULL":
                self.vm_writer.write_push("CONST", 0)
            elif current_keyword == "THIS":
                self.vm_writer.write_push("POINTER", 0)

        elif self.tokenizer.token_type() == "IDENTIFIER":
            cur_name = self.give_identifier()
            if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() != ";":
                if self.tokenizer.symbol() == "(" or self.tokenizer.symbol() == ".":
                    self.compile_subroutine_call(cur_name)
                elif self.tokenizer.symbol() == "[":
                    self.give_symbol()
                    self.vm_writer.write_push(self.symbol_table.kind_of(cur_name), self.symbol_table.index_of(cur_name))
                    self.compile_expression()
                    self.vm_writer.write_arithmetic("ADD")
                    self.vm_writer.write_pop("POINTER", 1)
                    self.vm_writer.write_push("THAT", 0)
                    self.give_symbol()  # ]
                else:
                    cur_idx = self.symbol_table.index_of(cur_name)
                    cur_seg = self.symbol_table.kind_of(cur_name)
                    self.vm_writer.write_push(cur_seg, cur_idx)
            else:
                cur_idx = self.symbol_table.index_of(cur_name)
                cur_seg = self.symbol_table.kind_of(cur_name)
                self.vm_writer.write_push(cur_seg, cur_idx)  # x = 67, so write 67.
        elif self.tokenizer.token_type() == "SYMBOL":
            token = self.tokenizer.symbol()
            if token == "~" or token == "-" or token == '^' or token == '#':
                symbol = self.give_symbol()
                self.compile_term()
                self.vm_writer.write_arithmetic(unary_map.get(symbol))
            else:
                self.give_symbol()  # (expression)
                self.compile_expression()
                self.give_symbol()

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.num_of_tabs += 1
        counter = 0
        if not (self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ")"):
            self.compile_expression()
            counter += 1
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self.give_symbol()
            self.compile_expression()
            counter += 1

        self.num_of_tabs -= 1
        return counter

    def give_keyword(self) -> str:
        ret = self.tokenizer.keyword()
        self.tokenizer.advance()
        return ret

    def give_symbol(self) -> str:
        special_symbols = {'>': "&gt;", '<': "&lt;", "&": "&amp;"}
        token = self.tokenizer.symbol()
        if token in special_symbols:
            token = special_symbols.get(token)
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
        return token

    def give_identifier(self) -> str:
        ret = self.tokenizer.identifier()
        self.tokenizer.advance()
        return ret

    def give_int_constant(self) -> str:
        ret = self.tokenizer.int_val()
        self.tokenizer.advance()
        return ret

    def give_str_const(self) -> str:
        ret = self.tokenizer.string_val()
        self.tokenizer.advance()
        return ret

    def give_type(self) -> str:
        if self.tokenizer.token_type().lower() == "keyword":
            return self.give_keyword()  # type
        else:
            return self.give_identifier()  # type if a class
