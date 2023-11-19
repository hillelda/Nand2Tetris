"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        self.class_symbol_table = {}
        self.subroutine_symbol_table = {}
        self.c_field_idx = 0
        self.c_static_idx = 0

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        self.subroutine_symbol_table = {}
        self.sub_arg_idx = 0
        self.sub_local_idx = 0

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        if kind == "STATIC":
            self.class_symbol_table[name] = (type, kind, self.c_static_idx)
            self.c_static_idx += 1

        elif kind == "FIELD":
            self.class_symbol_table[name] = (type, kind, self.c_field_idx)
            self.c_field_idx += 1

        elif kind == "ARG":
            self.subroutine_symbol_table[name] = (type, kind, self.sub_arg_idx)
            self.sub_arg_idx += 1

        elif kind == "VAR":
            self.subroutine_symbol_table[name] = (type, kind, self.sub_local_idx)
            self.sub_local_idx += 1

        else:
            print("\nType error in define :(\n")

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        if kind == "STATIC":
            return self.c_static_idx

        elif kind == "FIELD":
            return self.c_field_idx

        elif kind == "ARG":
            return self.sub_arg_idx

        elif kind == "VAR":
            return self.sub_local_idx

        else:
            print("\nType error in var_count :(\n")

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        if name in self.subroutine_symbol_table:
            return self.subroutine_symbol_table.get(name)[1]

        elif name in self.class_symbol_table:
            return self.class_symbol_table.get(name)[1]

        else:
            print("\nname not found error in kind_of :(\n")

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        if name in self.subroutine_symbol_table:
            return self.subroutine_symbol_table.get(name)[0]

        elif name in self.class_symbol_table:
            return self.class_symbol_table.get(name)[0]

        else:
            print("\nname not found error in type_of :(\n")

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        if name in self.subroutine_symbol_table:
            return self.subroutine_symbol_table.get(name)[2]

        elif name in self.class_symbol_table:
            return self.class_symbol_table.get(name)[2]

        else:
            print("\nname not found error in index_of :(\n")
