from d1.lexer import Lexer
from d1.parser1 import Parser1
lexer = Lexer().build()
file = open('./test.txt')
text_input = file.read()
file.close()
lexer.input(text_input)
# while True:
#     tok = lexer.token()
#     if not tok: break
#     print(tok)
parser = Parser1()
parser.build().parse(text_input, lexer, False)
