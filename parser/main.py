from lexer import Lexer
from yacc import Parser

lexer = Lexer().build()
file = open('D:/documents/Py.exercises/comp2/test.txt')
text_input = file.read()
file.close()
lexer.input(text_input)
# while True:
#     tok = lexer.token()
#     if not tok: break
#     print(tok)
parser = Parser()
parser.build().parse(text_input, lexer, False)
