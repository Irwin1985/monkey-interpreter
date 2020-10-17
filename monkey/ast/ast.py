from abc import ABC


class Node:
    def token_literal(self):
        raise NotImplementedError()

    def __str__(self):
        return ""


class Statement(Node, ABC):
    pass


class Expression(Node, ABC):
    pass


class Program(Node):
    def __init__(self):
        self.statements = []

    def token_literal(self):
        return self.statements[0].token_literal() if self.statements else ""

    def __str__(self):
        fmt = ""
        for s in self.statements:
            fmt += str(s)
        return fmt


class Identifier(Expression):
    def __init__(self, token, identifier):
        self.token = token
        self.value = identifier

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return self.value


class LetStatement(Statement):
    def __init__(self, token):
        self.token = token
        self.name = None
        self.value = None

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        s = f"{self.token_literal()} {str(self.name)} = "
        s += str(self.value) if self.value is not None else ""
        s += ";"
        return s


class ReturnStatement(Statement):
    def __init__(self, token):
        self.token = token
        self.return_value = None

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        s = f"{self.token_literal()} "
        s += str(self.return_value) if self.return_value is not None else ""
        s += ";"
        return s


class ExpressionStatement(Statement):
    def __init__(self, token):
        self.token = token
        self.expression = None

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return str(self.expression) if self.expression is not None else ""


class IntegerLiteral(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return self.token.literal


class BooleanLiteral(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return self.token.literal


class PrefixExpression(Expression):
    def __init__(self, token, operator):
        self.token = token
        self.operator = operator
        self.right = None

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return f"({self.operator}{self.right})"


class InfixExpression(Expression):
    def __init__(self, token, left, operator):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = None

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"


class BlockStatement(Statement):
    def __init__(self, token):
        self.token = token
        self.statements = []

    def __str__(self):
        return "".join([str(statement) for statement in self.statements])

    def token_literal(self):
        return self.token.literal


class FunctionLiteral(Expression):
    def __init__(self, token):
        self.token = token
        self.params = []
        self.body = None

    def __str__(self):
        p = ", ".join([str(x) for x in self.params])
        return f"{self.token_literal()}({p}){str(self.body)}"

    def token_literal(self):
        return self.token.literal


class IfExpression(Expression):
    def __init__(self, token):
        self.token = token
        self.condition = None
        self.consequence = None
        self.alternative = None

    def __str__(self):
        s = f"if {self.condition} {{ {self.consequence} }}"
        if self.alternative is not None:
            s += f" else {{ {self.alternative} }}"
        return s

    def token_literal(self):
        return self.token.literal


class WhileExpression(Expression):
    def __init__(self, token):
        self.token = token
        self.condition = None
        self.consequence = None

    def __str__(self):
        return f"while {self.condition} {{ {self.consequence} }}"

    def token_literal(self):
        return self.token.literal


class CallExpression(Expression):
    def __init__(self, token, function):
        self.token = token
        self.function = function
        self.args = []

    def __str__(self):
        args = ", ".join(str(arg) for arg in self.args)
        return f"{self.function}({args})"

    def token_literal(self):
        return self.token.literal


class StringLiteral(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return self.token.literal


class ArrayLiteral(Expression):
    def __init__(self, token):
        self.token = token
        self.elements = []

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        elems = [str(elem) for elem in self.elements]
        return f"[{', '.join(elems)}]"


class IndexExpression(Expression):
    def __init__(self, token, left):
        self.token = token
        self.left = left
        self.index = None

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return f"({str(self.left)}[{str(self.index)}])"


class HashLiteral(Expression):
    def __init__(self, token):
        self.token = token
        self.pairs = {}

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        pairs = [f"{str(k)}: {str(v)}" for k, v in self.pairs.items()]
        return "{" + ", ".join(pairs) + "}"
