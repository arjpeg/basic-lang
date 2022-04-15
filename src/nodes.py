from __future__ import annotations
from src.token import Token


class NumberNode:
    def __init__(self, tok: Token) -> None:
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self) -> str:
        return f"{self.tok}"


class BinOpNode:
    def __init__(
        self,
        left_node: BinOpNode | NumberNode | UnaryOpNode,
        op_tok: Token,
        right_node: BinOpNode | NumberNode | UnaryOpNode,
    ) -> None:
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start  # type: ignore
        self.pos_end = self.right_node.pos_end  # type: ignore

    def __repr__(self) -> str:
        return f"({self.left_node} {self.op_tok} {self.right_node})"


class UnaryOpNode:
    def __init__(self, op_tok: Token, node: UnaryOpNode | NumberNode) -> None:
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end  # type: ignore

    def __repr__(self) -> str:
        return f"({self.op_tok}{self.node})"


class VarAccessNode:
    def __init__(self, var_name_tok: Token) -> None:
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def __repr__(self) -> str:
        return f"{self.var_name_tok}"


class VarAssignNode:
    def __init__(self, var_name_tok: Token, value_node) -> None:
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end
