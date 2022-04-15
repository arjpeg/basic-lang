from src.error import NoOverloadError, RTError
from src.position import Position


class Number:
    def __init__(self, value: float | int):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start: Position = None, pos_end: Position = None):
        self.pos_start = pos_start
        self.pos_end = pos_end

        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

        return None, NoOverloadError(
            f"{type(other)} is not a Number", self.pos_start, self.pos_end
        )

    def sub(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

        return None, NoOverloadError(
            f"{type(other)} is not a Number", self.pos_start, self.pos_end
        )

    def mul(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

        return None, NoOverloadError(
            f"{type(other)} is not a Number", self.pos_start, self.pos_end
        )

    def div(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    f"Division by zero", other.pos_start, other.pos_end, self.context
                )

            return Number(self.value / other.value).set_context(self.context), None

        return None, NoOverloadError(
            f"{type(other)} is not a Number", self.pos_start, self.pos_end
        )

    def pow(self, other):
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(self.context), None

        return None, NoOverloadError(
            f"{type(other)} is not a Number", self.pos_start, self.pos_end
        )

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"{self.value}"
