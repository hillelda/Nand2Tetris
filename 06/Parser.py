"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        raw_input_lines = input_file.read().splitlines()
        self.input_lines = []

        for line in raw_input_lines:
            line = line.strip()
            if line == '' or line[0] == "/" or line[0] == "":
                continue
            else:
                line = line.replace(" ", "")
                line = line.split("//")[0]
                self.input_lines.append(line)

        self.current_command_idx = 0

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return self.current_command_idx < len(self.input_lines)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        # Your code goes here!
        self.current_command_idx += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        first_char = self.input_lines[self.current_command_idx][0]
        if first_char == '@':
            return "A_COMMAND"
        elif first_char == "(":
            return "L_COMMAND"
        return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        first_char = self.input_lines[self.current_command_idx][0]
        if first_char == '@':
            return self.input_lines[self.current_command_idx][1:]
        else:
            return self.input_lines[self.current_command_idx][1:-1]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        this_dest = self.input_lines[self.current_command_idx].split(";")[0]
        if '=' in this_dest:
            return this_dest.split('=')[0]

        else:
            return "null"

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """

        condition = self.input_lines[self.current_command_idx].split(";")[0]
        if "=" in condition:
            return condition.split("=")[1]
        return condition.split("=")[0]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """

        if ";" in self.input_lines[self.current_command_idx]:
            return self.input_lines[self.current_command_idx].split(";")[1]
        return "null"
