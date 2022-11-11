from typing import List, Tuple, Union, Dict
import sys
from Lexer import *
from Parser import *
from AST_classes import *
from Interpreter import *
sys.setrecursionlimit(200000)


def main():
    prog3 = "\n40 G = 8, Z = 9 \n52 IF G = 8 PRINT 'Its 7' \n60 G = G + 1, N = 8 \n70 IF G=N GOTO 52 \n80 IF G>N PRINT 'LOWER'\n90 IF G<N PRINT 'HIGHER'\n100 A = 2\n110 PRINT 'YOU GUESSED IT', A = 1"
    prog5 = "\n40 IF 10 = 11 PRINT 'knap hoor', P = 12, Y = 7\n60 Z = 11, P = 33\n80 PRINT 'janee'"
    prog6 = "\n40 G = 10, A = 10\n60 G = G + 1\n70 GOTO 60\n110 PRINT 'done', A = 1"
    prog7 = "\n40 G = 12, Z = 10 \n41 G = G + Z \n50 IF G = 100 GOTO 80 \n60 G = G + 1\n70 GOTO 50\n80 PRINT 'ITS 100 NOW!'"
    lexed = lexer(prog7, [])
    p1 = Parser(lexed)
    file = p1.parseProgram()
    interp = Interpreter(file)
    interp.initial()

if __name__ == "__main__":
    main()