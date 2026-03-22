"""
Grammar:
    E  -> (E Op E)
    E  -> a
    Op -> + | - | / | *
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class TreeNode:
    pass


@dataclass
class Leaf(TreeNode):
    """Represents a terminal symbol: (a | + | - | * | /)"""

    value: str


@dataclass
class Expression(TreeNode):
    """Represents a binary operation node: (E Op E)"""

    left: TreeNode
    operator: str
    right: TreeNode


class Parser:
    input: str
    cursor: int = 0
    derivations: list[str] = []

    def __init__(self, input: str):
        self.input = input.replace(" ", "")

    def current(self) -> Optional[str]:
        if not self.is_end_of_input():
            return self.input[self.cursor]
        return None

    def advance(self):
        self.cursor += 1

    def consume_if(self, expected: str) -> bool:
        if self.current() == expected:
            self.advance()
            return True
        return False

    def is_end_of_input(self) -> bool:
        return self.cursor >= len(self.input)

    def try_parse(self) -> Optional[TreeNode]:
        try:
            result = self.parse_expression()
            if not self.is_end_of_input():
                raise SyntaxError(
                    f"Unexpected character {self.current()} at {self.cursor}"
                )
            return result

        except SyntaxError as err:
            print(f"Syntax Error: {err}")
            return None

    def parse_expression(self) -> TreeNode:
        """
        Parse expression:
            E -> a
            E -> (E Op E)
        """

        self.derivations.append("E")
        current = self.current()

        if current == "(":
            self.derivations.append("   -> (E Op E)")
            self.advance()

            left = self.parse_expression()
            operator = self.parse_operator()
            right = self.parse_expression()

            if not self.consume_if(")"):
                raise SyntaxError(
                    f"Expected ')' at position {self.cursor} but found {current}"
                )

            return Expression(left=left, operator=operator, right=right)

        elif current == "a":
            self.derivations.append("   -> a")
            self.advance()
            return Leaf("a")

        else:
            raise SyntaxError(
                f"Expected '(' or 'a' at position {self.cursor} but found {current}"
            )

    def parse_operator(self) -> str:
        self.derivations.append("Op")
        current = self.current()

        if current in ["+", "-", "*", "/"]:
            self.derivations.append(f"  -> {current}")
            self.advance()
            return current
        else:
            raise SyntaxError(
                f"Expected operator at position {self.cursor} but found {current}"
            )


cases = [
    "a",
    "(a+a)",
    "(a*(a+a))",
    "((a+a)/(a*a))",
    "(a+)",  # missing second operand
    "a+a",  # missing parentheses
    "(a+a",  # missing closing paren
    "a(+a)",  #  misplaced a
]

for expr in cases:
    print("-=" * 15)
    print(f"Input: {expr}")

    parser = Parser(expr)
    ast = parser.try_parse()

    print(ast)
