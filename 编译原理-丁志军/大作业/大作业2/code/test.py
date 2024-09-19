from myLexer import Lexer
from myParser import Parser


parser = Parser()

while True:
    file_path = "./test.c"

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        if line[-1] == "\n":
            line = line[:-1]

    lex = Lexer().getLex(lines)

    parse = parser.getParse(lex[0])

    input()


# print(parser.parse_process_display)
