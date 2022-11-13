from Lexer import *
from Parser import *
from AST_classes import *
from Interpreter import *
sys.setrecursionlimit(200000)


def main():
    #f = open("basic", "r")
    f = open("basic2", "r")
    #f = open("basic3", "r")
    s = f.read()
    s = '\n' + s[0:]
    lexed = lexer(s, [])
    p1 = Parser(lexed)
    file = p1.parseProgram()
    interp = Interpreter(file)
    interp.initial()

if __name__ == "__main__":
    main()
