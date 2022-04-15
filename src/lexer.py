from src.error import IllegalCharError
from src.position import Position
from src.token import KEYWORDS, Token, TokenType
from src.consts import DIGITS, LETTERS, LETTERS_DIGITS


class Lexer:
    def __init__(self, fn: str, text: str) -> None:
        self.text = text
        self.fn = fn

        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        )

    def make_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in " \t":
                self.advance()

            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())

            elif self.current_char == "+":
                tokens.append(Token(TokenType.PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TokenType.MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TokenType.MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TokenType.DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == "^":
                tokens.append(Token(TokenType.POW, pos_start=self.pos))
                self.advance()

            elif self.current_char == "(":
                tokens.append(Token(TokenType.LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TokenType.RPAREN, pos_start=self.pos))
                self.advance()

            elif self.current_char == "=":
                tokens.append(Token(TokenType.EQUAL, pos_start=self.pos))
                self.advance()

            else:
                pos_start = self.pos.copy()

                char = self.current_char
                self.advance()

                return [], IllegalCharError(
                    f'"{char}" is not a valid character', pos_start, self.pos
                )
        tokens.append(Token(TokenType.EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                dot_count += 1

                if dot_count > 1:
                    break

            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TokenType.INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TokenType.FLOAT, float(num_str), pos_start, self.pos)

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + "_":
            id_str += self.current_char
            self.advance()

        tok_type = TokenType.KEYWORD if id_str in KEYWORDS else TokenType.IDENTIFIER

        return Token(tok_type, id_str, pos_start, self.pos)
