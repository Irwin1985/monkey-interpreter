from tok.tok import Token, lookup_identifier

WHITE_SPACE = (" ", "\n", "\t", "\r")
EOF = "\0"


class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.read_position = 0
        self.ch = ""

        self.read_char()

    def read_char(self):
        if self.read_position >= len(self.code):
            self.ch = EOF
        else:
            self.ch = self.code[self.read_position]

        self.position = self.read_position
        self.read_position += 1

    def next_token(self):
        self.skip_whitespace()

        if self.ch == "=":
            if self.peek_char() == "=":
                ch = self.ch
                self.read_char()
                tok = Token(Token.EQ, ch + self.ch)
            else:
                tok = Token(Token.ASSIGN, self.ch)
        elif self.ch == "+":
            tok = Token(Token.PLUS, self.ch)
        elif self.ch == "-":
            tok = Token(Token.MINUS, self.ch)
        elif self.ch == "!":
            if self.peek_char() == "=":
                ch = self.ch
                self.read_char()
                tok = Token(Token.NOT_EQ, ch + self.ch)
            else:
                tok = Token(Token.BANG, self.ch)
        elif self.ch == '"':
            tok = Token(Token.STRING, self.read_string())
        elif self.ch == "/":
            tok = Token(Token.SLASH, self.ch)
        elif self.ch == "*":
            tok = Token(Token.ASTERISK, self.ch)
        elif self.ch == "<":
            tok = Token(Token.LT, self.ch)
        elif self.ch == ">":
            tok = Token(Token.GT, self.ch)
        elif self.ch == ";":
            tok = Token(Token.SEMICOLON, self.ch)
        elif self.ch == ":":
            tok = Token(Token.COLON, self.ch)
        elif self.ch == ",":
            tok = Token(Token.COMMA, self.ch)
        elif self.ch == "(":
            tok = Token(Token.LPAREN, self.ch)
        elif self.ch == ")":
            tok = Token(Token.RPAREN, self.ch)
        elif self.ch == "{":
            tok = Token(Token.LBRACE, self.ch)
        elif self.ch == "}":
            tok = Token(Token.RBRACE, self.ch)
        elif self.ch == "[":
            tok = Token(Token.LBRACKET, self.ch)
        elif self.ch == "]":
            tok = Token(Token.RBRACKET, self.ch)
        elif self.ch == EOF:
            tok = Token(Token.EOF, "")
        else:
            if self.ch.isalpha() or self.ch == "_":
                ident = self.read_identifier()
                tok = Token(lookup_identifier(ident), ident)
                return tok
            elif self.ch.isdigit():
                tok = Token(Token.INT, self.read_number())
                return tok
            else:
                tok = Token(Token.ILLEGAL, self.ch)

        self.read_char()
        return tok

    def read_number(self):
        pos = self.position
        while self.ch.isdigit():
            self.read_char()

            if self.ch == EOF:
                break

        return self.code[pos : self.position]

    def read_string(self):
        position = self.position + 1
        while True:
            self.read_char()
            if self.ch == '"' or self.ch == EOF:
                break

        return self.code[position : self.position]

    def read_identifier(self):
        pos = self.position
        while self.ch.isalpha() or self.ch == "_":
            self.read_char()

            if self.ch == EOF:
                break

        return self.code[pos : self.position]

    def peek_char(self):
        if self.position >= len(self.code):
            return EOF
        else:
            return self.code[self.position + 1]

    def skip_whitespace(self):
        if self.ch == EOF:
            return

        while self.ch.isspace():
            self.read_char()
