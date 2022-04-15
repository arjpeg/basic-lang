from __future__ import annotations

from typing import Callable

from src.error import InvalidSyntaxError
from src.nodes import BinOpNode, NumberNode, UnaryOpNode, VarAccessNode, VarAssignNode
from src.token import TokenType, Token


class ParseResult:
    def __init__(self) -> None:
        self.error = None
        self.node: NumberNode | None = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res: ParseResult):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node: NumberNode):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok = self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TokenType.INT, TokenType.FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        if tok.type == TokenType.IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TokenType.LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TokenType.RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ')'",
                    )
                )
        return res.failure(
            InvalidSyntaxError(
                "Expected int, float, identifier, '+', '-' or '('",
                tok.pos_start,
                tok.pos_end,
            )
        )

    def factor(self):
        tok = self.current_tok
        res = ParseResult()

        if tok.type in (TokenType.PLUS, TokenType.MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())

            if res.error:
                return res

            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def power(self):
        return self.bin_op((TokenType.POW), self.atom, self.factor)

    def bin_op(self, operators: tuple[str], func_a: Callable, func_b: Callable = None):
        if func_b is None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.current_tok.type in operators:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

    def term(self):
        return self.bin_op((TokenType.MUL, TokenType.DIV), self.factor)

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(
            TokenType.KEYWORD, "var"
        ) or self.current_tok.matches(TokenType.KEYWORD, "let"):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TokenType.IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(
                        "Expected identifier",
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                    )
                )

            var_name = self.current_tok

            res.register_advancement()
            self.advance()

            if self.current_tok.type != TokenType.EQUAL:
                return res.failure(
                    InvalidSyntaxError(
                        "Expected '='",
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                    )
                )

            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res

            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op((TokenType.PLUS, TokenType.MINUS), self.term))
        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    "Expected 'var', 'let', 'int', 'float', '+', '-', or '('",
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                )
            )
        return res.success(node)

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TokenType.EOF:
            return res.failure(
                InvalidSyntaxError(
                    "Expected '+', '-', '*' or '/'",
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                )
            )
        return res
