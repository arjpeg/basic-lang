from __future__ import annotations

from src.nodes import BinOpNode, NumberNode, UnaryOpNode, VarAccessNode, VarAssignNode
from src.error import RTError
from src.token import TokenType
from src.values import Number


class SymbolTable:
    def __init__(self, parent: SymbolTable = None):
        self.symbols = {}  # type: ignore
        self.parent = parent

    def get(self, name: str):
        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)

        return value

    def set(self, name: str, value):
        self.symbols[name] = value

    def remove(self, name: str):
        del self.symbols[name]


class RunTimeResult:
    def __init__(self) -> None:
        self.value: Number | None = None
        self.error: RTError | None = None

    def register(self, res: RunTimeResult | Number):
        if isinstance(res, RunTimeResult):
            if res.error:
                self.error = res.error
            return res.value

        return res

    def success(self, value: Number | None):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self


class Interpreter:
    def visit(self, node: UnaryOpNode | BinOpNode | NumberNode, context: Context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context: Context):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node: NumberNode, context: Context):
        return RunTimeResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)  # type: ignore
        )

    def visit_BinOpNode(self, node: BinOpNode, context: Context):
        res = RunTimeResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node, context))
        print(node.right_node)
        if res.error:
            return res

        if node.op_tok.type == TokenType.PLUS:
            result, error = left.add(right)
        if node.op_tok.type == TokenType.MINUS:
            result, error = left.sub(right)
        if node.op_tok.type == TokenType.MUL:
            result, error = left.mul(right)
        if node.op_tok.type == TokenType.DIV:
            result, error = left.div(right)
        if node.op_tok.type == TokenType.POW:
            result, error = left.pow(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node: UnaryOpNode, context: Context):
        res = RunTimeResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        if node.op_tok.type == TokenType.MINUS:
            number, error = number.mul(Number(-1))

        if res.error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_VarAccessNode(self, node: VarAccessNode, context: Context):
        res = RunTimeResult()
        var_name = str(node.var_name_tok.value)

        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(
                RTError(
                    f"{var_name} is not defined", node.pos_start, node.pos_end, context
                )
            )

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node: VarAssignNode, context: Context):
        res = RunTimeResult()
        var_name = str(node.var_name_tok.value)
        value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)


class Context:
    def __init__(
        self, display_name: str, parent: Context = None, parent_entry_pos=None
    ) -> None:
        self.parent_entry_pos = parent_entry_pos
        self.display_name = display_name
        self.parent = parent

        self.symbol_table: SymbolTable = None  # type: ignore
