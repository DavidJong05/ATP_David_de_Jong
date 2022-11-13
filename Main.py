from Lexer import *
from Parser import *
from AST_classes import *
from Interpreter import *
sys.setrecursionlimit(200000)


def main():
    #f = open("basic", "r")
    f = open("basic2", "r")
    #f = open("basic3", "r")
    file_string = f.read()
    file_string = '\n' + file_string[0:]
    lexed = lexer(s, [])
    parsed = Parser(lexed)
    file = parsed.parseProgram()
    interp = Interpreter(file)
    interp.initial()

if __name__ == "__main__":
    main()
