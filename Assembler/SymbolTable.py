"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class SymbolTable:
    """
    A symbol table that keeps a correspondence between symbolic labels and 
    numeric addresses.
    """

    def __init__(self) -> None:
        """Creates a new symbol table initialized with all the predefined symbols
        and their pre-allocated RAM addresses, according to section 6.2.3 of the
        book.
        """
        self.symbol_table = {"R0": 0, "R1": 1 ,"R2": 2, "R3": 3, "R4": 4,
                             "R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9,
                             "R10": 10, "R11": 11, "R12": 12, "R13": 13,
                             "R14": 14, "R15": 15, "SCREEN": 16384,
                             "KBD": 24576, "SP": 0, "LCL": 1, "ARG": 2,
                             "THIS": 3, "THAT": 4}
        self.next_empty_memory = 16

    def add_entry(self, symbol: str, address: int) -> None:
        """Adds the pair (symbol, address) to the table.

        Args:
            symbol (str): the symbol to add.
            address (int): the address corresponding to the symbol.
        """
        self.symbol_table[symbol] = address

    def update_next_empty_memory(self):
        """
        This method increments the next empty memory counter in 1.
        :return:
        """
        self.next_empty_memory += 1

    def contains(self, symbol: str) -> bool:
        """Does the symbol table contain the given symbol?

        Args:
            symbol (str): a symbol.

        Returns:
            bool: True if the symbol is contained, False otherwise.
        """
        return symbol in self.symbol_table

    def get_address(self, symbol: str) -> int:
        """Returns the address associated with the symbol.

        Args:
            symbol (str): a symbol.

        Returns:
            int: the address associated with the symbol.
        """
        return self.symbol_table[symbol]
