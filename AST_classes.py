from typing import List, Tuple, Union, Dict
import sys
from Lexer import *
from Parser import *
sys.setrecursionlimit(200000)


class AST(object):
    pass

class TokenLineNode(AST):
    '''
    TokenLineNode
    Is the node in the AST that stores the classes per line
    The line number is connected to the children within that line
    Example: ( 40 [ AssignOP, AssignOp, BinOp, Goto ] )
    '''
    # __init__ :: Newline -> List -> None
    def __init__(self, line_number: Newline, children: List) -> None:
        self.line_number = line_number
        self.children = children

    def __str__(self) -> str:
        return f"TokenLineNode: Number: ({self.line_number.value} {[str(i) for i in self.children]})"

class Goto(AST):
    '''
    GOTO node
    Stores the GOTO token. Within the token is the value of the line to jump to
    '''
    # __init__ :: Token -> None
    def __init__(self, token: GOTO) -> None:
        self.token = token
        self.value = token.line_value

    # __str__ :: str
    def __str__(self) ->str:
        return f"GOTO: value:{self.value})"

class Print(AST):
    '''
    PRINT node
    Stores the PRINT token. Within the token is the value to print
    '''
    # __init__ :: Token -> None
    def __init__(self, token: PRINT) -> None:
        self.token = token
        self.value = token.value

    # __str__ :: str
    def __str__(self) -> str:
        return f"Print: value:{self.value})"

class BinOp(AST):
    '''
    Binary operator
    A binary operator requires two operands and an operator
    Example 5 + 4 where 5 and 4 are the operands and + is the operator
    '''
    # __init__ :: Token -> Token -> Token -> None
    def __init__(self, left: Token, op: Token, right: Token) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right

    # __str__ :: str
    def __str__(self) -> str:
        return f"BinOp: LHS: ({self.left}), OP: ({self.token}), RHS: ({self.right})"

class AssignOp(AST):
    '''
    Assign operator
    Takes any variable and assigns an integer to it
    '''
    # __init__ :: Token -> Token -> Token -> None
    def __init__(self, left: Token, op: Token, right: Token) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right

    # __str__ :: str
    def __str__(self) -> str:
        return f"AssignOP: LHS: ({self.left}) Assign: ({self.token}) RHS: ({self.right})"

class Condition(AST):
    '''
    Condition

    The condition evaluates the lhs and rhs token with the conditional operator
    The conditional operators are: >, <, <=, >=, <> or =
    '''
    # __init__ :: Token -> Token -> Token -> None
    def __init__(self, left: Token, conditional: Token, right: Token) -> None:
        self.left = left
        self.conditional = conditional
        self.right = right

    # __str__ :: str
    def __str__(self) -> str:
        return f"Condition: LHS: ({self.left}), Condition: ({self.conditional}), RHS: ({self.right})"

class IfNode(AST):
    '''
    IfNode
    Is the actual if statement with its token combined with the condition
    IF(token) G = 8(condition)
    '''
    # __init__ :: Token -> Condition -> None
    def __init__(self, token: Token, body: Condition) -> None:
        self.token = token
        self.body = body

    # __str__ :: str
    def __str__(self) -> str:
        return f"IF_state: IF: ({self.token}) Body: ({self.body})"

class FileNode(AST):
    '''
    FileNode
    This is the root of the AST, it stores the AST in the designated file by filename
    Within the body are the TokenLineNodes classes per line
    '''
    # __init__ :: str -> None
    def __init__(self, filename: str) -> None:
        self.name = filename
        self.body = []

    # __str__ :: str
    def __str__(self) -> str:
        return f"FILE: {self.name}\n{[str(line) for line in self.body]}"


# list_till_token :: List[Token] -> Token -> List[Token]
def list_till_token(lijst: List[Token], seperator: Token) -> List[Token]:
    '''Returns a list till given seperator/token'''
    if len(lijst) == 0:
        return []
    else:
        head, *tail = lijst
        if isinstance(head, seperator):
            return [head][:-1]
        return [head] + list_till_token(tail, seperator)
