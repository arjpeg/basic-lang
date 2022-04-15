class Position:
    def __init__(
        self, idx: int, ln: int, col: int, file_name: str, file_text: str
    ) -> None:
        self.idx = idx
        self.ln = ln
        self.col = col

        self.file_name = file_name
        self.file_text = file_text

    def advance(self, current_char: str = None):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.file_name, self.file_text)
