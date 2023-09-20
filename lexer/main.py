from lexer import Lexer
lexer = Lexer().build()
address = 'test3.txt'
file = open('TestCases/'+address)
result = open('resultOF'+address,'w')
text_input = file.read()
file.close()
lexer.input(text_input)
while True:
    tok = lexer.token()
    if not tok: break
    print(tok)
    result.write(str(tok)+'\n')
#print(Lexer.st)
