from dataclasses import dataclass
from src.position import Position

KEYWORDS = ["var", "let"]


@dataclass
class TokenType:
    # Built in types
    INT: str = "int"
    FLOAT: str = "float"
    STR: str = "string"

    # Operators
    PLUS: str = "+"
    MINUS: str = "-"
    MUL: str = "*"
    DIV: str = "/"
    POW: str = "^"

    LPAREN: str = "("
    RPAREN: str = ")"

    EOF: str = "EOF"

    IDENTIFIER: str = "identifier"
    KEYWORD: str = "keyword"
    EQUAL: str = "="


class Token:
    def __init__(
        self,
        type_: TokenType,
        value: str | int | float | None = None,
        pos_start: Position = None,
        pos_end: Position = None,
    ) -> None:
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

    def matches(self, type_: TokenType, value: str | int | float | None = None) -> bool:
        return self.type == type_ and self.value == value

    def __repr__(self) -> str:
        if self.value:
            return f"{self.type}:{self.value}"
        else:
            return f"{self.type}"
