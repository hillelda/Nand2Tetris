"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs 
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | dsds
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        file = input_stream.read()
        self.input_lines = []
        inString = False
        i = 0
        new_file = ""

        while i < len(file):
            char = file[i]
            if char == "\"":
                if not inString:
                    inString = True
                else:
                    inString = False

            if char == "/" and not inString:#checks if we are at comment and not in string
                i += 1
                char = file[i]
                if char == "/":#double slash comment is until end of line
                    while (char != "\n"):
                        i += 1
                        char = file[i]

                elif char == "*":#/* or /** comment
                    i += 1

                    while (not (file[i] == "*" and file[i + 1] == "/")):#find */ to mark end of comment
                        i += 1
                    i += 2
                else:
                    new_file += "/"#operator of division
            else:
                new_file += char
                i += 1

        raw_input_lines = new_file.splitlines()

        for line in raw_input_lines:
            line = line.strip()
            if (line != ""):
                self.input_lines.append(line)

        self.current_command_idx = 0
        self.curr_token = ''

        self.parsing_dict = {
            "class": "KEYWORD", "constructor": "KEYWORD", "function": "KEYWORD", "method": "KEYWORD",
            "field": "KEYWORD",
            "static": "KEYWORD", "var": "KEYWORD", "int": "KEYWORD", "char": "KEYWORD", "boolean": "KEYWORD",
            "void": "KEYWORD", "true": "KEYWORD", "false": "KEYWORD", "null": "KEYWORD", "this": "KEYWORD",
            "let": "KEYWORD", "do": "KEYWORD", "if": "KEYWORD", "else": "KEYWORD", "while": "KEYWORD",
            "return": "KEYWORD",
            '{': "SYMBOL", '}': "SYMBOL", '(': "SYMBOL", ')': "SYMBOL",
            '[': "SYMBOL", ']': "SYMBOL", '.': "SYMBOL",
            ',': "SYMBOL", ';': "SYMBOL", '+': "SYMBOL",
            '-': "SYMBOL", '*': "SYMBOL", '/': "SYMBOL", '&': "SYMBOL", '|': "SYMBOL",
            '<': "SYMBOL", '>': "SYMBOL", '=': "SYMBOL",
            '~': "SYMBOL", '^': "SYMBOL", '#': "SYMBOL"
        }

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        # Your code goes here!
        return not (self.current_command_idx == len(self.input_lines) - 1 and \
                    self.input_lines[self.current_command_idx - 1] == "")

    def check_command_idx(self):
        if self.input_lines[self.current_command_idx] == "":
            self.current_command_idx += 1

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        # Your code goes here!
        my_token = ""
        if not self.has_more_tokens():
            print("bad call to advance")
            return
        self.input_lines[self.current_command_idx] = self.input_lines[self.current_command_idx].strip()

        if self.input_lines[self.current_command_idx][0].isdigit():
            while self.input_lines[self.current_command_idx][0].isdigit():
                my_token += self.input_lines[self.current_command_idx][0]
                self.input_lines[self.current_command_idx] = self.input_lines[self.current_command_idx][1:]
            self.curr_token = my_token
            self.check_command_idx()
            return

        if self.input_lines[self.current_command_idx][0] == "\"":
            my_token += self.input_lines[self.current_command_idx][0]
            self.input_lines[self.current_command_idx] = self.input_lines[self.current_command_idx][1:]

            while self.input_lines[self.current_command_idx][0] != "\"":
                my_token += self.input_lines[self.current_command_idx][0]
                self.input_lines[self.current_command_idx] = self.input_lines[self.current_command_idx][1:]

            self.input_lines[self.current_command_idx] = self.input_lines[self.current_command_idx][1:]
            self.curr_token = my_token + "\""
            self.check_command_idx()
            return

        if self.parsing_dict.get(self.input_lines[self.current_command_idx][0]) == "SYMBOL":
            self.curr_token = self.input_lines[self.current_command_idx][0]
            self.input_lines[self.current_command_idx] = self.input_lines[self.current_command_idx][1:]
            self.check_command_idx()
            return

        if self.input_lines[self.current_command_idx][0].isalpha() or \
                self.input_lines[self.current_command_idx][0] == "_":  # todo: bad tokenizer for "main()".
            while self.input_lines[self.current_command_idx] and \
                    (self.input_lines[self.current_command_idx][0].isalpha() or
                     self.input_lines[self.current_command_idx][0] == "_"
                     or self.input_lines[self.current_command_idx][0].isdigit()):
                my_token += self.input_lines[self.current_command_idx][0]
                self.input_lines[self.current_command_idx] = self.input_lines[self.current_command_idx][1:]
            self.curr_token = my_token
            self.check_command_idx()
            return

        self.curr_token = "ERROR!!! BAD ADVANCE :(\n"

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        c_type = self.parsing_dict.get(self.curr_token)
        if c_type is not None:
            return c_type
        elif self.curr_token[0].isnumeric():
            return "INT_CONST"
        elif self.curr_token[0] == "\"":
            return "STRING_CONST"
        elif self.curr_token[0] == "_" or self.curr_token[0].isalpha():
            return "IDENTIFIER"
        else:
            return "\nERROR!!! bad token type :(\n"

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        # Your code goes here!
        return self.curr_token.upper()

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
        """
        # Your code goes here!
        return self.curr_token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
        """
        # Your code goes here!
        return self.curr_token

    def int_val(self) -> str:  # we fixed from int
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
        """
        # Your code goes here!
        return self.curr_token

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
        """
        # Your code goes here!
        return self.curr_token[1:-1]
