from typing import List, Tuple, Union, Dict
import sys
sys.setrecursionlimit(200000)


class Token:
    # __repr__ :: Token -> String
    def __repr__(self) -> str:
        return "Undefined"

class Add(Token):
    # __repr__ :: Add -> String
    def __repr__(self) -> str:
        return "Add"

class Min(Token):
    # __repr__ :: Min -> String
    def __repr__(self) -> str:
        return "Min"

class Multiply(Token):
    # __repr__ :: Multiply -> String
    def __repr__(self) -> str:
        return "Multiply"

class Divide(Token):
    # __repr__ :: Divide -> String
    def __repr__(self) -> str:
        return "Divide"

class GT(Token):  # Greater than
    # __repr__ :: GT -> String
    def __repr__(self) -> str:
        return "GT"

class LT(Token):  # Lesser than
    # __repr__ :: LT -> String
    def __repr__(self) -> str:
        return "LT"

class EQ(Token):  # Equal
    # __repr__ :: EQ -> String
    def __repr__(self) -> str:
        return "EQ"

class NEQ(Token):  # Not Equal
    # __repr__ :: NEQ -> String
    def __repr__(self) -> str:
        return "NEQ"

class GTE(Token):  # Greater than or equal
    # __repr__ :: GTE -> String
    def __repr__(self) -> str:
        return "GTE"

class LTE(Token):  # Lesser than or equal
    # __repr__ :: LTE -> String
    def __repr__(self) -> str:
        return "LTE"

class PRINT(Token):
    # __init__ :: String -> String
    def __init__(self, value: str) -> str:
        self.value = value

    # __repr__ :: PRINT -> String
    def __repr__(self) -> str:
        return "PRINT '" + str(self.value) + "'"

class INPUT(Token):
    # __repr__ :: INPUT -> String
    def __repr__(self) -> str:
        return "INPUT "

class IF_state(Token):
    # __repr__ :: IF_state -> String
    def __repr__(self) -> str:
        return "IF_state "

class Newline(Token):
    # __init__ :: Integer -> Integer
    def __init__(self, value: int) -> int:
        self.value = value

    # __repr__ :: Newline -> String
    def __repr__(self) -> str:
        return "Newline " + str(self.value)

class Variable(Token):
    # __init__ :: String -> String
    def __init__(self, value: str) -> str:
        self.value = value

    # __repr__ :: Variable -> String
    def __repr__(self) -> str:
        return "Variable " + str(self.value)

class Comma(Token):
    # __repr__ :: Comma -> String
    def __repr__(self) -> str:
        return "Comma "

class Integer(Token):
    # __init__ :: Integer -> int
    def __init__(self, value: int) -> int:
        self.value = value

    # __repr__ :: Integer -> String
    def __repr__(self) -> str:
        return "Integer " + str(self.value)

class GOTO(Token):
    # __init__ :: Newline -> int
    def __init__(self, line_value: Newline) -> int:
        self.line_value = line_value

    # __repr__ :: GOTO -> String
    def __repr__(self) -> str:
        return "GOTO " + str(self.line_value)


# small_tokens :: [Char]
small_tokens = ['+', '*', '/', '>', '<', '=', ',']

# digits :: [Char]
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# Variables :: [Char]
variables = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z']


# tokendict :: Dict((String,Token))
tokendict = dict()
tokendict['+'] = ("Add", lambda: Add())
tokendict['-'] = ("Min", lambda: Min())
tokendict['*'] = ("Multiply", lambda: Multiply())
tokendict['/'] = ("Divide", lambda: Divide())
tokendict[','] = ("Comma", lambda: Comma())
tokendict['>'] = ("GT", lambda: GT())
tokendict['<'] = ("LT", lambda: LT())
tokendict['='] = ("EQ", lambda: EQ())
tokendict['<>'] = ("NEQ", lambda: NEQ())
tokendict['>='] = ("GTE", lambda: GTE())
tokendict['<='] = ("LTE", lambda: LTE())
tokendict['GOTO'] = ("GOTO", lambda line_value: GOTO(line_value))
tokendict['PRINT'] = ("PRINT", lambda value:  PRINT(value))
tokendict['INPUT'] = ("INPUT", lambda: INPUT())
tokendict['IF_state'] = ("IF_state", lambda: IF_state())
tokendict['Newline'] = ("Newline", lambda value: Newline(value))
tokendict['Variable'] = ("Variable", lambda value: Variable(value))
tokendict['Integer'] = ("Integer", lambda value: Integer(value))

# list_till_seperator :: List[str] -> chr -> List[str]
def list_till_seperator(lijst: List[str], seperator: chr) -> List[str]:
    '''Creates a list till given seperator, this can be a char or a list of chars'''
    if len(lijst) == 0:
        return []
    else:
        head, *tail = lijst
        if head in seperator:
            return [head][:-1]
        return [head] + list_till_seperator(tail, seperator)


# lexer :: String -> List[Token] -> List[Token]
def lexer(prog: str, lexed: List[Token]) -> List[Token]:
    '''Goes over each char in the string
    Detects tokens and stores them by given token class in lexed list'''
    if not prog:
        return lexed
    c, *progrest = prog
    if c in small_tokens:
        if c == '<' and prog[1] == '>':  ### NEQ token <>
            lexed.append(tokendict['<>'][1]())
            progrest.remove(progrest[0])
            return lexer(progrest, lexed)

        if c == '>' and prog[1] == '=':  ### GTE token >=
            lexed.append(tokendict['>='][1]())
            progrest.remove(progrest[0])
            return lexer(progrest, lexed)

        if c == '<' and prog[1] == '=':  ### LTE token <=
            lexed.append(tokendict['<='][1]())
            progrest.remove(progrest[0])
            return lexer(progrest, lexed)
        lexed.append(tokendict[c][1]())

    if c == 'G' and prog[1:5] == ['O', 'T', 'O', ' ']:  ### GOTO token
        del progrest[0:4]
        number_list = list_till_seperator(progrest, [' ', "\n"])
        number = ''.join(number_list)
        del progrest[0:len(number_list)]
        lexed.append(tokendict['GOTO'][1](number))

    if c == 'P' and prog[1:6] == ['R', 'I', 'N', 'T', ' ']:  ### PRINT token
        del progrest[0:5]
        if progrest[0] == "'":
            text = list_till_seperator(progrest[1:], "'")
            print_text = ''.join(text)
            del progrest[0:len(text) + 2] # + the "'" at the end
            lexed.append(tokendict['PRINT'][1](print_text))
        else:
            raise SyntaxError(f"No valid print value")

    if c == 'I' and prog[1:3] == ['F', ' ']:  ### IF_state token
        lexed.append(tokendict['IF_state'][1]())
        del progrest[0:2]

    if c in variables:  ### Variable token
        if len(prog) == 1:
            lexed.append(tokendict['Variable'][1](c))
        elif (prog[1] in small_tokens or prog[1] == ' ' or prog[1] == '\n'):
            lexed.append(tokendict['Variable'][1](c))

    if c == '\n' and prog[1] in digits:  ### Newline + subroutine number
        line = list_till_seperator(prog[1:], [' ','\n'])
        line_number = ''.join(line)
        del progrest[0:len(line)]
        lexed.append(tokendict['Newline'][1](line_number))

    if c == '-': ### Minus numbers - Integer token
        if prog[1] in digits:
            numbers = list_till_seperator(progrest, (small_tokens, variables, ' ', '\n', ','))
            numbers.insert(0, c)
            del progrest[0:len(numbers) - 1]
            number = ''.join(numbers)
            lexed.append(tokendict['Integer'][1](number))
        else:
            lexed.append(tokendict[c][1]())

    if c in digits:  ### Integer token
        numbers = list_till_seperator(progrest, (small_tokens, variables, ' ', '\n', ','))
        numbers.insert(0, c)
        del progrest[0:len(numbers) - 1]
        number = ''.join(numbers)
        lexed.append(tokendict['Integer'][1](number))
    return lexer(progrest, lexed)
