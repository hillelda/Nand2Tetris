"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_stream = output_stream
        self.file_name = ""
        self.counter = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.file_name = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        if command == "add":
            assembly_command = "// add\n" \
                               "@SP\n" \
                               "M = M - 1\n" \
                               "A = M\n" \
                               "D = M\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "D = D + M\n" \
                               "M = D\n"
        elif command == "sub":
            assembly_command = "// sub\n" \
                               "@SP\n" \
                               "M = M - 1\n" \
                               "A = M\n" \
                               "D = M\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "D = M - D\n" \
                               "M = D\n"
        elif command == "neg":
            assembly_command = "// neg\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "M = - M\n"
        elif command == "and":
            assembly_command = "// and\n" \
                               "@SP\n" \
                               "M = M - 1\n" \
                               "A = M\n" \
                               "D = M\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "D = D&M\n" \
                               "M = D\n"
        elif command == "or":
            assembly_command = "// or\n" \
                               "@SP\n" \
                               "M = M - 1\n" \
                               "A = M\n" \
                               "D = M\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "D = D|M\n" \
                               "M = D\n"

        elif command == "not":
            assembly_command = "// neg\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "M = !M\n"

        elif command == "shiftleft":
            assembly_command = "// shiftleft\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "M = M<<\n"

        elif command == "shiftright":
            assembly_command = "// shiftright\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "M = M>>\n"

        elif command == "eq":
            self.counter += 1
            assembly_command = "// eq\n" \
                               "@SP\n" \
                               "AM = M - 1\n" \
                               "D = M\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "D = D - M\n" \
                               "@TRUE_JEQ" + str(self.counter) + "\n"\
                               "D;JEQ" "\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "M = 0\n" \
                               "@CONTINUE" + str(self.counter) + "\n" \
                               "0;JMP\n" \
                               "(TRUE_JEQ" + str(self.counter) + ")\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "M = -1\n" \
                               "(CONTINUE" + str(self.counter) + ")\n"

        elif command == "gt":
            self.counter += 1
            str_cntr = str(self.counter)
            assembly_command = "// gt\n" \
                               "@SP\n" \
                               "M = M - 1\n" \
                               "A = M\n" \
                               "D = M\n"\
                               "@R13\n"\
                               "M = D\n" \
                               "@SP\n" \
                               "A = M - 1\n"\
                               "D = M\n"\
                               "@R14\n" \
                               "M = D\n"\
                               "@TOP_VALUE_POSITIVE" + str_cntr + "\n"\
                               "D;JGE\n" \
                               "@R13\n" \
                                "D = M\n" \
                                "@REGULAR" + str_cntr + "\n"\
                               "D;JLE\n" \
                                "@FALSE_JT" + str_cntr + "\n" \
                                "0;JMP\n"\
            \
                                "(TOP_VALUE_POSITIVE" + str_cntr + ")\n" \
                                "@R13\n" \
                                "D = M\n" \
                               "@TRUE_JT" + str_cntr + "\n" \
                                "D;JLT\n" \
 \
                                "(REGULAR" + str_cntr + ")\n" \
                                "@R14\n"\
                               "D = M - D\n" \
                               "@TRUE_JT" + str_cntr + "\n" \
                               "D;JGT" "\n" \
                                \
                               "(FALSE_JT" + str_cntr + ")\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "M = 0\n" \
                               "@CONTINUE" + str_cntr + "\n" \
                               "0;JMP\n" \
            \
                               "(TRUE_JT" + str_cntr + ")\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "M = -1\n" \
                               "(CONTINUE" + str_cntr + ")\n"

        elif command == "lt":
            self.counter += 1
            str_cntr = str(self.counter)
            assembly_command = "// lt\n" \
                               "@SP\n" \
                               "M = M - 1\n" \
                               "A = M\n" \
                               "D = M\n"\
                               "@R13\n"\
                               "M = D\n" \
                               "@SP\n" \
                               "A = M - 1\n"\
                               "D = M\n"\
                               "@R14\n" \
                               "M = D\n"\
            \
                               "@TOP_VALUE_POSITIVE" + str_cntr + "\n"\
                               "D;JGE\n" \
                               "@R13\n" \
                                "D = M\n" \
                                "@REGULAR" + str_cntr + "\n"\
                               "D;JLE\n" \
                                "@TRUE_JL" + str_cntr + "\n" \
                                "0;JMP\n"\
            \
                                "(TOP_VALUE_POSITIVE" + str_cntr + ")\n" \
                                "@R13\n" \
                                "D = M\n" \
                               "@FALSE_JL" + str_cntr + "\n" \
                                "D;JLT\n" \
 \
                                "(REGULAR" + str_cntr + ")\n" \
                                "@R14\n"\
                               "D = M - D\n" \
                               "@TRUE_JL" + str_cntr + "\n" \
                               "D;JLT\n" \
                                \
                               "(FALSE_JL" + str_cntr + ")\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "M = 0\n" \
                               "@CONTINUE" + str_cntr + "\n" \
                               "0;JMP\n" \
            \
                               "(TRUE_JL" + str_cntr + ")\n" \
                               "@SP\n" \
                               "A = M - 1\n" \
                               "M = -1\n" \
                               "(CONTINUE" + str_cntr + ")\n"
        else:
            assembly_command = "ERROR!!!!!!!! \n"

        self.output_stream.write(assembly_command)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        if command == "C_PUSH":
            if segment == "constant":
                assembly_command = "// Push constant" + str(index) + "\n"\
                                   "@" + str(index) + "\n" \
                                   "D = A\n" \
                                   "@SP\n" \
                                   "M = M + 1\n"\
                                   "A = M - 1\n" \
                                   "M = D\n"
            elif segment == "static":
                assembly_command = "// Push static" + str(index) + "\n" \
                                    "@" + self.file_name + "." + str(index) + "\n" \
                                    "D = M\n" \
                                    "@SP\n" \
                                    "M = M + 1\n" \
                                    "A = M - 1\n" \
                                    "M = D\n"

            elif segment == "local":
                assembly_command = "// Push local" + str(index) + "\n" \
                                    "@" + str(index) + "\n" \
                                    "D = A\n"\
                                    "@LCL\n" \
                                    "A = M + D\n" \
                                    "D = M\n" \
                                    "@SP\n" \
                                    "M = M + 1\n" \
                                    "A = M - 1\n" \
                                    "M = D\n"

            elif segment == "argument":
                assembly_command = "// Push argument" + str(index) + "\n" \
                                    "@" + str(index) + "\n" \
                                    "D = A\n"\
                                    "@ARG\n" \
                                    "A = M + D\n" \
                                    "D = M\n" \
                                    "@SP\n" \
                                    "M = M + 1\n" \
                                    "A = M - 1\n" \
                                    "M = D\n"

            elif segment == "this":
                assembly_command = "// Push this" + str(index) + "\n" \
                                    "@" + str(index) + "\n" \
                                    "D = A\n"\
                                    "@THIS\n" \
                                    "A = M + D\n" \
                                    "D = M\n" \
                                    "@SP\n" \
                                    "M = M + 1\n" \
                                    "A = M - 1\n" \
                                    "M = D\n"

            elif segment == "that":
                assembly_command = "// Push that" + str(index) + "\n" \
                                    "@" + str(index) + "\n" \
                                    "D = A\n"\
                                    "@THAT\n" \
                                    "A = M + D\n" \
                                    "D = M\n" \
                                    "@SP\n" \
                                    "M = M + 1\n" \
                                    "A = M - 1\n" \
                                    "M = D\n"

            elif segment == "pointer":
                assembly_command = "// Push pointer" + str(index) + "\n" \
                                    "@" + str(index) + "\n" \
                                    "D = A\n"\
                                    "@THIS\n" \
                                    "A = A + D\n" \
                                    "D = M\n"\
                                    "@SP\n" \
                                    "M = M + 1\n" \
                                    "A = M - 1\n" \
                                    "M = D\n"

            elif segment == "temp":
                assembly_command = "// Push temp" + str(index) + "\n" \
                                    "@" + str(index) + "\n" \
                                    "D = A\n"\
                                    "@5 // temp is in 5th index\n" \
                                    "A = A + D\n" \
                                    "D = M\n" \
                                    "@SP\n" \
                                    "M = M + 1\n" \
                                    "A = M - 1\n" \
                                    "M = D\n"

        else:
            if segment == "static":
                assembly_command = "// Pop static" + str(index) + "\n" \
                                  "@SP\n" \
                                  "M = M - 1\n" \
                                  "A = M\n"\
                                  "D = M\n" \
                                  "@" + self.file_name + "." + str(index) + "\n" \
                                  "M = D\n" \


            elif segment == "local":
                # we used the SP (garbage) memory as an extra register, to avoid using R14 R15 that we didn't know if
                # we can use or that they are used in other processes.
                assembly_command = "// Pop local" + str(index) + "\n" \
                                     "@" + str(index) + "\n" \
                                     "D = A\n" \
                                     "@LCL\n" \
                                     "D = M + D \n"\
                                     "@SP\n" \
                                     "M = M - 1\n" \
                                     "A = M + 1\n"\
                                     "M = D\n"\
                                     "@SP\n"\
                                     "A = M\n"\
                                     "D = M\n"\
                                     "A = A + 1\n"\
                                     "A = M\n"\
                                     "M = D\n"

            elif segment == "argument":
                # we used the SP (garbage) memory as an extra register, to avoid using R14 R15 that we didn't know if
                # we can use or that they are used in other processes.
                assembly_command = "// Pop argument" + str(index) + "\n" \
                                     "@" + str(index) + "\n" \
                                     "D = A\n" \
                                     "@ARG\n" \
                                     "D = M + D \n"\
                                     "@SP\n" \
                                     "M = M - 1\n" \
                                     "A = M + 1\n"\
                                     "M = D\n" \
                                     "@SP\n"\
                                     "A = M\n" \
                                     "D = M\n"\
                                     "A = A + 1\n"\
                                     "A = M\n"\
                                     "M = D\n"

            elif segment == "this":
                # we used the SP (garbage) memory as an extra register, to avoid using R14 R15 that we didn't know if
                # we can use or that they are used in other processes.
                assembly_command = "// Pop this" + str(index) + "\n" \
                                     "@" + str(index) + "\n" \
                                     "D = A\n" \
                                     "@THIS\n" \
                                     "D = M + D \n"\
                                     "@SP\n" \
                                     "M = M - 1\n" \
                                     "A = M + 1\n"\
                                     "M = D\n"\
                                     "@SP\n"\
                                     "A = M\n" \
                                     "D = M\n"\
                                     "A = A + 1\n"\
                                     "A = M\n"\
                                     "M = D\n"

            elif segment == "that":
                # we used the SP (garbage) memory as an extra register, to avoid using R14 R15 that we didn't know if
                # we can use or that they are used in other processes.
                assembly_command = "// Pop that" + str(index) + "\n" \
                                     "@" + str(index) + "\n" \
                                     "D = A\n" \
                                     "@THAT\n" \
                                     "D = M + D \n"\
                                     "@SP\n" \
                                     "M = M - 1\n" \
                                     "A = M + 1\n"\
                                     "M = D\n" \
                                     "@SP\n"\
                                     "A = M\n" \
                                     "D = M\n"\
                                     "A = A + 1\n"\
                                     "A = M\n"\
                                     "M = D\n"

            elif segment == "pointer":
                assembly_command = "// Pop pointer" + str(index) + "\n" \
                                     "@" + str(index) + "\n" \
                                     "D = A\n" \
                                     "@THIS\n" \
                                     "D = A + D \n"\
                                     "@SP\n" \
                                     "M = M - 1\n" \
                                     "A = M + 1\n"\
                                     "M = D\n"\
                                     "@SP\n"\
                                     "A = M\n" \
                                     "D = M\n"\
                                     "A = A + 1\n"\
                                     "A = M\n"\
                                     "M = D\n"

            elif segment == "temp":
                # we used the SP (garbage) memory as an extra register, to avoid using R14 R15 that we didn't know if
                # we can use or that they are used in other processes.
                assembly_command = "// Pop temp" + str(index) + "\n" \
                                     "@" + str(index) + "\n" \
                                     "D = A\n" \
                                     "@5\n" \
                                     "D = A + D \n"\
                                     "@SP\n" \
                                     "M = M - 1\n" \
                                     "A = M + 1\n"\
                                     "M = D\n" \
                                     "@SP\n"\
                                     "A = M\n" \
                                     "D = M\n"\
                                     "A = A + 1\n"\
                                     "A = M\n"\
                                     "M = D\n"

        self.output_stream.write(assembly_command)

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "foo" be a function within the file Xxx.vm.
        The handling of each "call" command within foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass
