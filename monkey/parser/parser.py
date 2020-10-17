from ast.ast import (
    Program,
    LetStatement,
    Identifier,
    ReturnStatement,
    ExpressionStatement,
    IntegerLiteral,
    BooleanLiteral,
    PrefixExpression,
    InfixExpression,
    CallExpression,
    FunctionLiteral,
    BlockStatement,
    IfExpression,
    StringLiteral,
    ArrayLiteral,
    IndexExpression,
    HashLiteral,
)
from tok.tok import Token, PRECEDENCES, Precedence


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.curr_token = lexer.next_token()
        self.peek_token = lexer.next_token()

        self.errors = []

        self.prefix_parse_fns = {}
        self.infix_parse_fns = {}

        self.register_prefix(Token.IDENT, self.parse_identifier)
        self.register_prefix(Token.INT, self.parse_numeric_literal)
        self.register_prefix(Token.BANG, self.parse_prefix_expression)
        self.register_prefix(Token.MINUS, self.parse_prefix_expression)
        self.register_prefix(Token.TRUE, self.parse_boolean_literal)
        self.register_prefix(Token.FALSE, self.parse_boolean_literal)
        self.register_prefix(Token.LPAREN, self.parse_grouped_expression)
        self.register_prefix(Token.IF, self.parse_if_expression)
        self.register_prefix(Token.FUNCTION, self.parse_function_literal)
        self.register_prefix(Token.STRING, self.parse_string_literal)
        self.register_prefix(Token.LBRACKET, self.parse_array_literal)
        self.register_prefix(Token.LBRACE, self.parse_hash_literal)

        self.register_infix(Token.PLUS, self.parse_infix_expression)
        self.register_infix(Token.MINUS, self.parse_infix_expression)
        self.register_infix(Token.SLASH, self.parse_infix_expression)
        self.register_infix(Token.ASTERISK, self.parse_infix_expression)
        self.register_infix(Token.EQ, self.parse_infix_expression)
        self.register_infix(Token.NOT_EQ, self.parse_infix_expression)
        self.register_infix(Token.LT, self.parse_infix_expression)
        self.register_infix(Token.GT, self.parse_infix_expression)
        self.register_infix(Token.LPAREN, self.parse_call_expression)
        self.register_infix(Token.LBRACKET, self.parse_index_expression)

    def parse_program(self):
        program = Program()

        while not self.is_current(Token.EOF):
            stmt = self.parse_statement()
            if stmt is not None:
                program.statements.append(stmt)
            self.next_token()

        return program

    def parse_statement(self):
        if self.is_current(Token.LET):
            return self.parse_let_statement()
        elif self.is_current(Token.RETURN):
            return self.parse_return_statement()
        else:
            return self.parse_expression_statement()

    def parse_let_statement(self):
        stmt = LetStatement(self.curr_token)

        if not self.expect_peek(Token.IDENT):
            return None

        stmt.name = Identifier(self.curr_token, self.curr_token.literal)

        if not self.expect_peek(Token.ASSIGN):
            return None

        self.next_token()

        stmt.value = self.parse_expression(Precedence.LOWEST)

        if self.is_peek(Token.SEMICOLON):
            self.next_token()

        return stmt

    def parse_return_statement(self):
        stmt = ReturnStatement(self.curr_token)

        self.next_token()

        stmt.return_value = self.parse_expression(Precedence.LOWEST)

        if self.is_peek(Token.SEMICOLON):
            self.next_token()

        return stmt

    def parse_expression_statement(self):
        stmt = ExpressionStatement(self.curr_token)

        exp = self.parse_expression(Precedence.LOWEST)
        if exp is None:
            return None

        stmt.expression = exp

        if self.is_peek(Token.SEMICOLON):
            self.next_token()

        return stmt

    def parse_expression(self, precedence):
        prefix = self.prefix_parse_fns.get(self.curr_token.token_type)

        if prefix is None:
            self.no_prefix_parse_fn_error(self.curr_token.token_type)
            return None

        left_exp = prefix()

        while (
            not self.is_peek(Token.SEMICOLON)
            and precedence.value < self.peek_precedence().value
        ):

            infix = self.infix_parse_fns.get(self.peek_token.token_type)
            if infix is None:
                return left_exp

            self.next_token()

            if left_exp is None:
                return None

            left_exp = infix(left_exp)

        return left_exp

    def parse_numeric_literal(self):
        try:
            val = int(self.curr_token.literal)
            return IntegerLiteral(self.curr_token, val)
        except ValueError:
            self.errors.append(
                f"Could not parse '{self.curr_token.literal}' as int"
            )
            return None

    def parse_prefix_expression(self):
        exp = PrefixExpression(self.curr_token, self.curr_token.literal)
        self.next_token()
        exp.right = self.parse_expression(Precedence.PREFIX)
        return exp

    def parse_infix_expression(self, left):
        exp = InfixExpression(self.curr_token, left, self.curr_token.literal)
        precedence = self.curr_precedence()
        self.next_token()
        exp.right = self.parse_expression(precedence)
        return exp

    def parse_call_expression(self, function):
        exp = CallExpression(self.curr_token, function)
        exp.args = self.parse_expression_list(Token.RPAREN)
        return exp

    def parse_string_literal(self):
        return StringLiteral(self.curr_token, self.curr_token.literal)

    def parse_function_literal(self):
        fn = FunctionLiteral(self.curr_token)

        if not self.expect_peek(Token.LPAREN):
            return None

        fn.params = self.parse_function_parameters()

        if not self.expect_peek(Token.LBRACE):
            return None

        fn.body = self.parse_block_statement()
        return fn

    def parse_function_parameters(self):
        identifiers = []

        if self.peek_token.token_type == Token.RPAREN:
            self.next_token()
            return identifiers

        self.next_token()

        ident = Identifier(self.curr_token, self.curr_token.literal)
        identifiers.append(ident)

        while self.peek_token.token_type == Token.COMMA:
            self.next_token()
            self.next_token()

            ident = Identifier(self.curr_token, self.curr_token.literal)
            identifiers.append(ident)

        if not self.expect_peek(Token.RPAREN):
            return None

        return identifiers

    def parse_block_statement(self):
        block = BlockStatement(self.curr_token)

        self.next_token()

        while not self.is_current(Token.RBRACE) and not self.is_current(
            Token.EOF
        ):
            stmt = self.parse_statement()
            if stmt is not None:
                block.statements.append(stmt)

            self.next_token()

        return block

    def parse_grouped_expression(self):
        self.next_token()
        exp = self.parse_expression(Precedence.LOWEST)
        return exp if self.expect_peek(Token.RPAREN) else None

    def parse_if_expression(self):
        exp = IfExpression(self.curr_token)

        if not self.expect_peek(Token.LPAREN):
            return None

        self.next_token()

        exp.condition = self.parse_expression(Precedence.LOWEST)

        if not self.expect_peek(Token.RPAREN):
            return None

        if not self.expect_peek(Token.LBRACE):
            return None

        exp.consequence = self.parse_block_statement()

        if self.is_peek(Token.ELSE):
            self.next_token()

            if not self.expect_peek(Token.LBRACE):
                return None

            exp.alternative = self.parse_block_statement()

        return exp

    def parse_array_literal(self):
        array = ArrayLiteral(self.curr_token)
        elems = self.parse_expression_list(Token.RBRACKET)
        array.elements = elems
        return array

    def parse_expression_list(self, end):
        lst = []

        if self.is_peek(end):
            self.next_token()
            return lst

        self.next_token()
        lst.append(self.parse_expression(Precedence.LOWEST))

        while self.is_peek(Token.COMMA):
            self.next_token()
            self.next_token()
            lst.append(self.parse_expression(Precedence.LOWEST))

        return lst if self.expect_peek(end) else None

    def parse_index_expression(self, left):
        exp = IndexExpression(self.curr_token, left)
        self.next_token()
        exp.index = self.parse_expression(Precedence.LOWEST)
        return exp if self.expect_peek(Token.RBRACKET) else None

    def parse_hash_literal(self):
        hsh = HashLiteral(self.curr_token)

        while not self.is_peek(Token.RBRACE):
            self.next_token()
            key = self.parse_expression(Precedence.LOWEST)

            if not self.expect_peek(Token.COLON):
                return None

            self.next_token()

            value = self.parse_expression(Precedence.LOWEST)
            hsh.pairs[key] = value

            if not self.is_peek(Token.RBRACE) and not self.expect_peek(
                Token.COMMA
            ):
                return None

        return hsh if self.expect_peek(Token.RBRACE) else None

    def expect_peek(self, token_type):
        if self.is_peek(token_type):
            self.next_token()
            return True
        else:
            self.peek_error(token_type)
            return False

    def parse_identifier(self):
        return Identifier(self.curr_token, self.curr_token.literal)

    def parse_boolean_literal(self):
        return BooleanLiteral(
            self.curr_token, Token.TRUE == self.curr_token.token_type
        )

    def is_current(self, token_type):
        return self.curr_token.token_type == token_type

    def is_peek(self, token_type):
        return self.peek_token.token_type == token_type

    def peek_error(self, token_type):
        self.errors.append(
            f"Expected '{token_type}', got '{self.peek_token.token_type}'"
        )

    def peek_precedence(self):
        return PRECEDENCES.get(self.peek_token.token_type, Precedence.LOWEST)

    def curr_precedence(self):
        precedence = PRECEDENCES.get(self.curr_token.token_type)
        return precedence if precedence is not None else Precedence.LOWEST

    def no_prefix_parse_fn_error(self, token_type):
        msg = f"No prefix parse function for '{token_type}' found"
        self.errors.append(msg)

    def next_token(self):
        self.curr_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def register_prefix(self, token_type, fn):
        self.prefix_parse_fns[token_type] = fn

    def register_infix(self, token_type, fn):
        self.infix_parse_fns[token_type] = fn

    def print_errors(self):
        for err in self.errors:
            print(f"\t{err}")
