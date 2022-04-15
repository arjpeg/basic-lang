from src.position import Position


class Error:
    def __init__(
        self, error_name: str, details: str, pos_start: Position, pos_end: Position
    ):
        self.error_name = error_name
        self.details = details

        self.pos_start = pos_start
        self.pos_end = pos_end

    @staticmethod
    def generate_string_with_arrows(text: str, pos_start: Position, pos_end: Position):
        result = ""
        # Calculate indices
        idx_start = max(text.rfind("\n", 0, pos_start.idx), 0)
        idx_end = text.find("\n", idx_start + 1)
        if idx_end < 0:
            idx_end = len(text)

        # Generate each line
        line_count = pos_end.ln - pos_start.ln + 1

        for i in range(line_count):
            # Calculate line columns
            line = text[idx_start:idx_end]
            col_start = pos_start.col if i == 0 else 0
            col_end = pos_end.col if i == line_count - 1 else len(line) - 1

            # Append to result
            result += line + "\n"
            result += " " * col_start + "^" * (col_end - col_start)

            # Re-calculate indices
            idx_start = idx_end
            idx_end = text.find("\n", idx_start + 1)
            if idx_end < 0:
                idx_end = len(text)

        return result.replace("\t", "")

    def as_string(self):
        res = f'\nFile "{self.pos_start.file_name}", line {self.pos_start.ln+1}'
        res = f"{self.error_name}: {self.details}"
        res += f"\n{self.generate_string_with_arrows(self.pos_start.file_text, self.pos_start, self.pos_end)}"

        return res


class IllegalCharError(Error):
    def __init__(self, details, pos_start: Position, pos_end: Position):
        super().__init__("Illegal Character", details, pos_start, pos_end)


class InvalidSyntaxError(Error):
    def __init__(self, details, pos_start: Position, pos_end: Position):
        super().__init__(
            "Illegal Syntax", details=details, pos_start=pos_start, pos_end=pos_end
        )


class RTError(Error):
    def __init__(self, details, pos_start: Position, pos_end: Position, context):
        super().__init__(
            "Runtime Error", details=details, pos_start=pos_start, pos_end=pos_end
        )
        self.context = context

    def as_string(self):
        res = self.generate_traceback()
        res += f"{self.error_name}: {self.details}\n"
        res += f"\n{self.generate_string_with_arrows(self.pos_start.file_text, self.pos_start, self.pos_end)}"

        return res

    def generate_traceback(self):
        res = ""

        pos = self.pos_start
        ctx = self.context

        while ctx:
            res = (
                f'\tFile "{pos.file_name}", line {pos.ln+1} in {ctx.display_name}\n'
                + res
            )

            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return "Traceback (most recent call last):\n" + res


class NoOverloadError(Error):
    def __init__(self, details, pos_start: Position, pos_end: Position):
        super().__init__(
            "No overload provided",
            details=details,
            pos_start=pos_start,
            pos_end=pos_end,
        )
