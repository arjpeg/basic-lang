from src.interpreter import Context, Interpreter, SymbolTable
from src.parser import Parser
from src.lexer import Lexer

global_symbol_table = SymbolTable()
global_symbol_table.set("null", 0)


def run(text: str, fn: str):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    if error:
        return [], error

    parser = Parser(tokens)
    ast = parser.parse()

    if ast.error:
        return [], ast.error

    interpreter = Interpreter()

    context = Context("<module>")
    context.symbol_table = global_symbol_table

    res = interpreter.visit(ast.node, context)

    return res.value, res.error
