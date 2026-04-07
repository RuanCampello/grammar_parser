"""
Grammar:
    E  -> (E Op E)
    E  -> a
    Op -> + | - | / | *
"""

from typing import Optional
from dataclasses import dataclass
import nltk
nltk.download('punkt')        # Required for tokenization
nltk.download('treebank')     # Contains sample parse tree
from nltk import Tree as NLTKTree


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
        self.cursor = 0 

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
    
    def to_nltk_tree(self, node: TreeNode) -> NLTKTree:
        """Função para fazer a árvore sintática mantendo os parênteses estritos da gramática"""
        if isinstance(node, Leaf):
            return NLTKTree('E', [node.value])
            
        elif isinstance(node, Expression):
            left_tree = self.to_nltk_tree(node.left)
            op_tree = NLTKTree('Op', [node.operator])
            right_tree = self.to_nltk_tree(node.right)
            
            # Os parênteses voltam como filhos diretos de E
            return NLTKTree('E', ['(', left_tree, op_tree, right_tree, ')'])

cases = [
    "a",
    "(a+a)",
    "(a*(a+a))",
    "((a+a)/(a*a))",
    "(a+)",  # missing second operand
    "a+a",  # missing parentheses
    "(a+a",  # missing closing paren
    "a(+a)",  #  misplaced a
    "((a*a)+(a/a))",
    "(a + (a * (a - a)))",
    "(((a + a) * a) - a)",
    "(a + (a * a))",
    "(a - (a / a))",
    "((a + a) * a)",
    "((a - a) / a)",
    "(-a)", # missing first operand
    "((a a))", #missing operator
    "()", #completely empty
]


for expr in cases:
    print("-=" * 20)
    print(f"Input: {expr}\n")

    parser = Parser(expr)
    ast = parser.try_parse()
    
    if ast:
        tree = parser.to_nltk_tree(ast)
        print("Abrindo a árvore na interface gráfica...")
        
        # fazendo com que se abra a vizualização das árvores
        tree.draw() 
        
    else:
        print("Falha ao gerar árvore devido a erro de sintaxe.")
