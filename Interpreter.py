from typing import List, Tuple, Union, Dict
import sys
from Lexer import *
from Parser import *
from AST_classes import *
sys.setrecursionlimit(200000)

class Interpreter():
    # __init__ :: FileNode -> None
    def __init__(self, AST: FileNode) -> None:
        self.tree = AST
        self.memory = dict()
        self.line_numberList = []
        self.index = 0

    # initial :: None
    def initial(self) -> None:
        '''Initiates the Interpreter by assigning all the line numbers to self.line_numberList'''
        [self.line_numberList.append(lineNode.line_number.value) for lineNode in self.tree.body]
        return self.interpTree()

    # interpTree :: None
    def interpTree(self) -> None:
        '''Interprets the body of the tree
        Within the body are codelines, each line gets interpreted'''
        if len(self.tree.body) == self.index:
            return self.tree
        self.interpLine(self.tree.body[self.index].children)
        self.index += 1
        return self.interpTree()

    # interpLine :: List -> None
    def interpLine(self, line: List, counter = 0) -> None:
        '''Interprets a line of code
        by detecting the operations in the line'''
        if len(line) == counter :
            return counter
        else:
            self.detectInterp(line[counter])
            if isinstance(line[counter], IfNode):
                if not self.interpIF(line[counter]):
                    return counter
            counter += 1
            return self.interpLine(line,counter)

    # detectInterp :: AST -> None
    def detectInterp(self, node: AST) -> None:
        '''Detects the specific class on what way it needs to be interpreted'''
        if isinstance(node, AssignOp):
            return self.interpAssignOp(node)
        elif isinstance(node, BinOp):
            return self.interpBinOp(node)
        elif isinstance(node, IfNode):
            return
        elif isinstance(node, Print):
            return self.interpPrint(node)
        elif isinstance(node, Goto):
            return self.interpGoto(node)
        else:
            raise SyntaxError(f"This is no correct node: {node}")

    # interpBinOp :: BinOp -> None
    def interpBinOp(self, node: BinOp) -> None:
        '''Interprets the binary operator by returning the result of the operation'''
        if node.left.value and node.right.value in self.memory.keys(): # both Variables G + N
            return self.returnResult(int(self.memory[node.left.value]),node.op,int(self.memory[node.right.value]))
        elif node.left.value in self.memory.keys(): # Only left G + 8
            return self.returnResult(int(self.memory[node.left.value]), node.op, int(node.right.value))
        elif node.right.value in self.memory.keys(): # Only right 8 + G
            return self.returnResult(int(node.left.value), node.op, int(self.memory[node.right.value]))
        elif isinstance(int(node.left.value), int) and isinstance(int(node.right.value), int): # Both Integers 8 + 10
            return self.returnResult(int(node.left.value), node.op, int(node.right.value))
        else:
            raise SyntaxError(f"Unknown Variable or Integer {node.left.value} {node.op} {node.right.value}")

    # returnResult :: int -> Token -> int -> Union[int,float]
    def returnResult(self, left: int, op: Token, right: int) -> Union[int,float]:
        '''Returns the result of the given operation'''
        if isinstance(op, Add):
            return left + right
        elif isinstance(op, Min):
            return left - right
        elif isinstance(op, Divide):
            return left / right
        elif isinstance(op, Multiply):
            return left * right
        else:
            raise SyntaxError(f"Unknown operator found: {node.op}")

    # interpAssignOp :: AssignOp -> None
    def interpAssignOp(self, node: AssignOp) -> None:
        '''Interprets the assign operator
        Assign the given value to the given variable
        Puts it in the self.memory'''

        if isinstance(node.right, BinOp):
            result = self.interpBinOp(node.right)
            self.memory[node.left.value] = int(result)
        elif node.right.value in self.memory.keys():
            self.memory[node.left.value] = self.memory[node.right.value]
        else:
            self.memory[node.left.value] = int(node.right.value)
        print(self.memory)
        return self.memory

    # interpCondition :: Condition -> bool
    def interpCondition(self, node: Condition) -> bool:
        '''Interprets the given condition and returns a boolean'''
        if node.left.value and node.right.value in self.memory.keys(): # both Variables G > N
            return self.returnBool(int(self.memory[node.left.value]),node.conditional,int(self.memory[node.right.value]))
        elif node.left.value in self.memory.keys(): # Only left G > 8
            return self.returnBool(int(self.memory[node.left.value]), node.conditional,int(node.right.value))
        elif node.right.value in self.memory.keys(): # Only right 8 > G
            return self.returnBool(int(node.left.value), node.conditional, int(self.memory[node.right.value]))
        elif isinstance(int(node.left.value), int) and isinstance(int(node.right.value), int): # Both Integers 8 > 10
            return self.returnBool(int(node.left.value), node.conditional, int(node.right.value))
        else:
            raise SyntaxError(f"Unknown Variable or Integer {node.left.value} {node.conditional} {node.right.value}")

    # returnBool :: int -> Token -> int -> bool
    def returnBool(self, left: int, condition: Token, right: int) -> bool:
        '''Returns a bool from given condition'''
        if isinstance(condition, EQ):
            return left == right
        elif isinstance(condition, NEQ):
            return left != right
        elif isinstance(condition, LT):
            return left < right
        elif isinstance(condition, GT):
            return left> right
        elif isinstance(condition, LTE):
            return left <= right
        elif isinstance(condition, GTE):
            return left >= right
        else:
            raise SyntaxError(f"Unknown condition found: {node.conditional}")

    # interpIF :: IfNode -> None
    def interpIF(self, node: IfNode) -> None:
        '''Interprets the given if statement'''
        if self.interpCondition(node.body):
            print(node.body.left.value,"",node.body.conditional,"",node.body.right.value," is correct!")#finish the line
            return 1
        else:
            print("if-state is wrong")#go next line
            return 0

    # interpPrint :: Print -> None
    def interpPrint(self, node: Print) -> None:
        '''Returns printed value'''
        return print("Print: ",node.value)

    # interpGoto :: Goto -> None
    def interpGoto(self, node: Goto) -> None:
        '''Interprets the goto statement by changing the index to the designed line'''
        print("Go to line: ", node.value)
        return self.matchNode(node.value)

    # matchNode :: int -> None
    def matchNode(self, jump_number: int) -> None:
        '''Matches the jump number to the actual line in the code and gets the index from that line
        Changes the self.index to start interpreting from the designed line'''
        if jump_number in self.line_numberList:
            ind = next(((n, x) for n, x in enumerate(self.tree.body) if int(x.line_number.value) == int(jump_number)), None)
            self.index = ind[0]
            self.index -=1
            return self.index
        else:
            raise SyntaxError(f"{jump_number} is no valid line to go to")
