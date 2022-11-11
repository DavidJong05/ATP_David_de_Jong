from typing import List, Tuple, Union, Dict
import sys
from Lexer import *
from AST_classes import *

sys.setrecursionlimit(200000)



class Parser:
    # __init__ :: List[Token] -> None
    def __init__(self, lexed_tokens: List[Token]) -> None:
        self.lexed_tokens = lexed_tokens[1:]
        self.current_token = lexed_tokens[0]
        self.next_token = lexed_tokens[1]

    # GoNextToken :: Token
    def goNextToken(self) -> Token:
        '''Goes to the next token in self.lexed_tokens
        Makes the self.next_token the new self.current_token
        narrows down lexed_tokens'''
        if len(self.lexed_tokens) == 1:
            self.current_token = self.lexed_tokens[0]
            self.lexed_tokens = []
            self.next_token = None
            return self.current_token
        elif len(self.lexed_tokens) == 0:
            self.current_token = None
            return self.current_token
        else:
            head, *tail = self.lexed_tokens
            self.lexed_tokens = tail
            self.current_token = head
            self.next_token = tail[0]
            return head

    # tokenLine :: TokenLineNode
    def tokenLine(self) -> TokenLineNode:
        '''Creates a TokenLineNode'''
        if isinstance(self.current_token, Newline):
            return TokenLineNode(self.current_token, list_till_token(self.lexed_tokens, Newline))

    # binaryOp :: BinOp
    def binaryOp(self) -> BinOp:
        '''Creates a binary operator from tokens and stores it in the class BinOp()'''
        if isinstance(self.current_token, Variable) or isinstance(self.current_token, Integer):
            lhs = self.current_token  # Variable or Integer
            if isinstance(self.next_token, Add) or isinstance(self.next_token, Min) or isinstance(self.next_token,Divide) or isinstance(self.next_token, Multiply):
                self.goNextToken()
                v = self.current_token  # Add/Min/Mult/Div Token
                self.goNextToken()
                if isinstance(self.current_token, Variable) or isinstance(self.current_token, Integer):
                    rhs = self.current_token  # Variable or Integer
                    if isinstance(self.next_token, Add) or isinstance(self.next_token, Min) or isinstance(self.next_token,Divide) or isinstance(self.next_token, Multiply):
                        raise SyntaxError(f"Can only make Expression with 2 Variables")
                    return BinOp(lhs, v, rhs)
                else:
                    raise SyntaxError(f"Token: {self.current_token}, is no Variable or Integer")
            else:
                raise SyntaxError(f"Token: {self.next_token} is no binary operator")
        else:
            raise SyntaxError(f"Token: {self.current_token}, is no Variable or Integer")

    # assignOp :: AssingOp
    def assignOp(self) -> AssignOp:
        '''Creates an assign operator from the list of tokens and stores it in class AssignOp()'''
        if isinstance(self.current_token, Variable):
            lhs = self.current_token  # Variable
            if isinstance(self.next_token, EQ):  # Check if next token is equal token
                self.goNextToken()
                assign = self.current_token  # Equal
                self.goNextToken()  # Go to the token after equal
                if isinstance(self.next_token, Add) \
                        or isinstance(self.next_token, Min) \
                        or isinstance(self.next_token, Divide) \
                        or isinstance(self.next_token, Multiply):  # Example line: C = C + 1
                    temp = self.current_token  # store the first token after "="
                    self.goNextToken()
                    if isinstance(self.next_token, Variable) or isinstance(self.next_token, Integer):
                        rhs = BinOp(temp, self.current_token, self.next_token)
                        self.goNextToken()
                        self.goNextToken()  # ugly way to remove entire assign operator from token list
                        return AssignOp(lhs, assign, rhs)
                    else:
                        raise SyntaxError(f"Token: {self.next_token}, is no Variable or Integer")
                elif isinstance(self.current_token, Variable) or isinstance(self.current_token, Integer):
                    rhs = self.current_token
                    self.goNextToken()  # ugly way to remove entire assign operator from token list
                    return AssignOp(lhs, assign, rhs)
                else:
                    raise SyntaxError(f"Token: {self.next_token} is no Binary operator or Variable or Integer")
            else:
                raise SyntaxError(f"Token: {self.next_token} is no Assign token")
        else:
            raise SyntaxError(f"Token: {self.current_token}, is no Variable")

    # parseIf :: IfNode
    def parseIf(self) -> IfNode:
        '''Creates a IfNode with given tokens from self.lexed_tokens and stores it in class IfNode()'''
        if isinstance(self.current_token, IF_state):
            temp = self.current_token  # Save the IF_state Token
            if isinstance(self.next_token, Variable) or isinstance(self.next_token, Integer):
                self.goNextToken()
                if isinstance(self.next_token, EQ) \
                        or isinstance(self.next_token, GT) \
                        or isinstance(self.next_token, GTE) \
                        or isinstance(self.next_token, LT) \
                        or isinstance(self.next_token, LTE) \
                        or isinstance(self.next_token, NEQ):
                    temp2 = self.current_token  # Save int or var
                    self.goNextToken()
                    if isinstance(self.next_token, Variable) or isinstance(self.next_token, Integer):
                        Con = Condition(temp2, self.current_token, self.next_token)
                        self.goNextToken()
                        self.goNextToken()  # ugly way to remove entire if statement from token list
                        return IfNode(temp, Con)
                    else:
                        print("IF statement not complete: Next token is no int or variable")
                else:
                    print("IF statement not complete: Next token is no condition token")
            else:
                print("IF statement not complete: Next token is no int or variable")
        else:
            print("This token is no IF_state")

    # parsePrint :: Print
    def parsePrint(self) -> Print:
        '''Stores print value in class Print()'''
        if isinstance(self.current_token, PRINT):
            p = Print(self.current_token)
            self.goNextToken()
            return p

    # parseGOTO :: Goto
    def parseGOTO(self):
        '''Stores GOTO value in class Goto()'''
        if isinstance(self.current_token, GOTO):
            g = Goto(self.current_token)
            self.goNextToken()
            return g

    # parseLine :: List
    def parseLine(self) -> List:
        '''Parses a line of code
        Stores the made classes in AST_list'''
        self.goNextToken()
        AST_list = []
        if isinstance(self.current_token, IF_state):
            AST_list.append(self.parseIf())

        if isinstance(self.current_token, Variable) and isinstance(self.next_token, EQ):
            AST_list.append(self.assignOp())

        if isinstance(self.current_token, Variable) or isinstance(self.current_token, Integer):
            AST_list.append(self.binaryOp())

        if isinstance(self.current_token, PRINT):
            AST_list.append(self.parsePrint())

        if isinstance(self.current_token, GOTO):
            AST_list.append(self.parseGOTO())

        if isinstance(self.current_token, Comma):
            AST_list.extend(self.parseLine())

        if isinstance(self.current_token, Newline):
            return AST_list

        if len(self.lexed_tokens) == 0:
            return AST_list

    # parseProgram :: FileNode
    def parseProgram(self, file = None) -> FileNode:
        '''Parses the entire code
        stores it in class FileNode()'''
        if file == None:
            file = FileNode("test")

        if len(self.lexed_tokens) == 0:
            print()
            print(file)
            #print("done")
            return file

        if isinstance(self.current_token, Newline):
            TokenLineNode = self.tokenLine()
            TokenLineNode.children = self.parseLine()
            file.body.append(TokenLineNode)

        return self.parseProgram(file)