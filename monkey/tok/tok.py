from enum import Enum


class Token:
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    IDENT = "IDENT"
    INT = "INT"
    STRING = "STRING"

    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"

    LT = "<"
    GT = ">"

    COMMA = ","
    SEMICOLON = ";"
    COLON = ":"

    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"

    FUNCTION = "FUNCTION"
    LET = "LET"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    RETURN = "RETURN"
    EQ = "=="
    NOT_EQ = "!="

    KEYWORDS = {
        "fn": FUNCTION,
        "let": LET,
        "true": TRUE,
        "false": FALSE,
        "if": IF,
        "else": ELSE,
        "return": RETURN,
    }

    def __init__(self, token_type, literal):
        self.token_type = token_type
        self.literal = literal


def lookup_identifier(ident):
    keyword = Token.KEYWORDS.get(ident)
    return Token.IDENT if keyword is None else keyword


class Precedence(Enum):
    LOWEST = 0
    EQUALS = 1
    LESSGREATER = 2
    SUM = 3
    PRODUCT = 4
    PREFIX = 5
    CALL = 6
    INDEX = 7


PRECEDENCES = {
    Token.EQ: Precedence.EQUALS,
    Token.NOT_EQ: Precedence.EQUALS,
    Token.LT: Precedence.LESSGREATER,
    Token.GT: Precedence.LESSGREATER,
    Token.PLUS: Precedence.SUM,
    Token.MINUS: Precedence.SUM,
    Token.SLASH: Precedence.PRODUCT,
    Token.ASTERISK: Precedence.PRODUCT,
    Token.LPAREN: Precedence.CALL,
    Token.LBRACKET: Precedence.INDEX,
}
