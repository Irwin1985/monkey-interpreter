import unittest

from ast.ast import (
    LetStatement,
    Identifier,
    IntegerLiteral,
    BooleanLiteral,
    InfixExpression,
    StringLiteral,
    ArrayLiteral,
    IndexExpression,
    HashLiteral,
)
from lexer.lexer import Lexer
from parser.parser import Parser


class TestParser(unittest.TestCase):
    def test_let_statements(self):
        tests = [
            ["let x = 5;", "x", 5],
            ["let y = true;", "y", True],
            ["let foobar = y;", "foobar", "y"],
        ]

        for tt in tests:
            lexer = Lexer(tt[0])
            parser = Parser(lexer)
            program = parser.parse_program()

            self.assert_parser_errors(parser)
            self.assertEqual(1, len(program.statements))

            stmt = program.statements[0]

            self.assert_let_statement(tt[1], stmt)
            self.assert_literal_expression(tt[2], stmt.value)

    def test_return_statements(self):
        tests = [
            ["return 5;", 5],
            ["return true;", True],
            ["return foobar;", "foobar"],
        ]

        for tt in tests:
            lexer = Lexer(tt[0])
            parser = Parser(lexer)
            program = parser.parse_program()

            self.assert_parser_errors(parser)
            self.assertEqual(1, len(program.statements))

            stmt = program.statements[0]

            self.assertEqual("return", stmt.token_literal())
            self.assert_literal_expression(tt[1], stmt.return_value)

    def test_identifier_expression(self):
        lexer = Lexer("foobar;")
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)
        self.assertEqual(1, len(program.statements))

        ident = program.statements[0].expression

        self.assertEqual("foobar", ident.value)
        self.assertEqual("foobar", ident.token_literal())

    def test_integer_literal_expression(self):
        lexer = Lexer("5;")
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)
        self.assertEqual(1, len(program.statements))

        literal = program.statements[0].expression

        self.assertEqual(5, literal.value)
        self.assertEqual("5", literal.token_literal())

    def test_parsing_prefix_expressions(self):
        tests = [
            ["!5;", "!", 5],
            ["-15;", "-", 15],
            ["!foobar;", "!", "foobar"],
            ["-foobar;", "-", "foobar"],
            ["!true;", "!", True],
            ["!false;", "!", False],
        ]

        for tt in tests:
            lexer = Lexer(tt[0])
            parser = Parser(lexer)
            program = parser.parse_program()

            self.assert_parser_errors(parser)
            self.assertEqual(1, len(program.statements))

            exp = program.statements[0].expression

            self.assertEqual(tt[1], exp.operator)
            self.assert_literal_expression(tt[2], exp.right)

    def test_parsing_infix_expressions(self):
        tests = [
            ["5 + 5;", 5, "+", 5],
            ["5 - 5;", 5, "-", 5],
            ["5 * 5;", 5, "*", 5],
            ["5 / 5;", 5, "/", 5],
            ["5 > 5;", 5, ">", 5],
            ["5 < 5;", 5, "<", 5],
            ["5 == 5;", 5, "==", 5],
            ["5 != 5;", 5, "!=", 5],
            ["foobar + barfoo;", "foobar", "+", "barfoo"],
            ["foobar - barfoo;", "foobar", "-", "barfoo"],
            ["foobar * barfoo;", "foobar", "*", "barfoo"],
            ["foobar / barfoo;", "foobar", "/", "barfoo"],
            ["foobar > barfoo;", "foobar", ">", "barfoo"],
            ["foobar < barfoo;", "foobar", "<", "barfoo"],
            ["foobar == barfoo;", "foobar", "==", "barfoo"],
            ["foobar != barfoo;", "foobar", "!=", "barfoo"],
            ["true == true", True, "==", True],
            ["true != false", True, "!=", False],
            ["false == false", False, "==", False],
        ]

        for tt in tests:
            lexer = Lexer(tt[0])
            parser = Parser(lexer)
            program = parser.parse_program()

            self.assert_parser_errors(parser)
            self.assertEqual(1, len(program.statements))

            exp = program.statements[0].expression

            self.assert_infix_expression(tt[1], tt[2], tt[3], exp)

    def test_operator_precedence_parsing(self):
        tests = [
            ["-a * b", "((-a) * b)"],
            ["!-a", "(!(-a))"],
            ["a + b + c", "((a + b) + c)"],
            ["a + b - c", "((a + b) - c)"],
            ["a * b * c", "((a * b) * c)"],
            ["a * b / c", "((a * b) / c)"],
            ["a + b / c", "(a + (b / c))"],
            ["a + b * c + d / e - f", "(((a + (b * c)) + (d / e)) - f)"],
            ["3 + 4; -5 * 5", "(3 + 4)((-5) * 5)"],
            ["5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))"],
            ["5 < 4 != 3 > 4", "((5 < 4) != (3 > 4))"],
            [
                "3 + 4 * 5 == 3 * 1 + 4 * 5",
                "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))",
            ],
            ["true", "true"],
            ["false", "false"],
            ["3 > 5 == false", "((3 > 5) == false)"],
            ["3 < 5 == true", "((3 < 5) == true)"],
            ["1 + (2 + 3) + 4", "((1 + (2 + 3)) + 4)"],
            ["(5 + 5) * 2", "((5 + 5) * 2)"],
            ["2 / (5 + 5)", "(2 / (5 + 5))"],
            ["(5 + 5) * 2 * (5 + 5)", "(((5 + 5) * 2) * (5 + 5))"],
            ["-(5 + 5)", "(-(5 + 5))"],
            ["!(true == true)", "(!(true == true))"],
            ["a + add(b * c) + d", "((a + add((b * c))) + d)"],
            [
                "add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))",
                "add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))",
            ],
            [
                "add(a + b + c * d / f + g)",
                "add((((a + b) + ((c * d) / f)) + g))",
            ],
            [
                "a * [1, 2, 3, 4][b * c] * d",
                "((a * ([1, 2, 3, 4][(b * c)])) * d)",
            ],
            [
                "add(a * b[2], b[1], 2 * [1, 2][1])",
                "add((a * (b[2])), (b[1]), (2 * ([1, 2][1])))",
            ],
        ]

        for tt in tests:
            lexer = Lexer(tt[0])
            parser = Parser(lexer)
            program = parser.parse_program()

            self.assert_parser_errors(parser)
            self.assertEqual(tt[1], str(program))

    def test_boolean_expression(self):
        tests = [
            ["true;", True],
            ["false;", False],
        ]

        for tt in tests:
            lexer = Lexer(tt[0])
            parser = Parser(lexer)
            program = parser.parse_program()

            self.assert_parser_errors(parser)
            self.assertEqual(1, len(program.statements))

            exp = program.statements[0].expression
            self.assert_literal_expression(tt[1], exp)

    def test_if_expression(self):
        lexer = Lexer("if (x < y) { x }")
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)
        self.assertEqual(1, len(program.statements))

        exp = program.statements[0].expression
        self.assert_infix_expression("x", "<", "y", exp.condition)
        self.assertEqual(1, len(exp.consequence.statements))

        consequence = exp.consequence.statements[0]
        self.assert_identifier("x", consequence.expression)

        self.assertIsNone(exp.alternative)

    def test_if_else_expression(self):
        lexer = Lexer("if (x < y) { x } else { y }")
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)
        self.assertEqual(1, len(program.statements))

        exp = program.statements[0].expression
        self.assert_infix_expression("x", "<", "y", exp.condition)
        self.assertEqual(1, len(exp.consequence.statements))

        consequence = exp.consequence.statements[0]
        self.assert_identifier("x", consequence.expression)
        self.assertEqual(1, len(exp.alternative.statements))

        alternative = exp.alternative.statements[0]
        self.assert_identifier("y", alternative.expression)

    def test_while_expression(self):
        lexer = Lexer("while (1 < 2) { x }")
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)
        self.assertEqual(1, len(program.statements))

        exp = program.statements[0].expression
        self.assert_infix_expression(1, "<", 2, exp.condition)
        self.assertEqual(1, len(exp.consequence.statements))

        consequence = exp.consequence.statements[0]
        self.assert_identifier("x", consequence.expression)

    def test_function_literal_parsing(self):
        lexer = Lexer("fn(x, y) { x + y; }")
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)
        self.assertEqual(1, len(program.statements))

        exp = program.statements[0].expression
        self.assertEqual(2, len(exp.params))

        self.assert_literal_expression("x", exp.params[0])
        self.assert_literal_expression("y", exp.params[1])

        self.assertEqual(1, len(exp.body.statements))

        body_stmt = exp.body.statements[0]
        self.assert_infix_expression("x", "+", "y", body_stmt.expression)

    def test_function_parameter_parsing(self):
        tests = [
            ["fn() {};", []],
            ["fn(x) {};", ["x"]],
            ["fn(x, y, z) {};", ["x", "y", "z"]],
        ]

        for tt in tests:
            lexer = Lexer(tt[0])
            parser = Parser(lexer)
            program = parser.parse_program()

            function = program.statements[0].expression

            self.assert_parser_errors(parser)
            self.assertEqual(len(tt[1]), len(function.params))

            for i, ident in enumerate(tt[1]):
                self.assert_literal_expression(ident, function.params[i])

    def test_call_expression(self):
        lexer = Lexer("add(1, 2 * 3, 4 + 5)")
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)
        self.assertEqual(1, len(program.statements))

        exp = program.statements[0].expression
        self.assert_identifier("add", exp.function)
        self.assertEqual(3, len(exp.args))

        self.assert_literal_expression(1, exp.args[0])
        self.assert_infix_expression(2, "*", 3, exp.args[1])
        self.assert_infix_expression(4, "+", 5, exp.args[2])

    def test_string_literal_expression(self):
        lexer = Lexer('"hello world"')
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)
        self.assertEqual(1, len(program.statements))

        literal = program.statements[0].expression

        self.assertIsInstance(literal, StringLiteral)

        self.assertEqual("hello world", literal.value)

    def test_parsing_array_literal(self):
        lexer = Lexer("[1, 2 * 2, 3 + 3]")
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)

        array = program.statements[0].expression

        self.assertIsInstance(array, ArrayLiteral)

        self.assertEqual(3, len(array.elements))

        self.assert_int_literal(1, array.elements[0])
        self.assert_infix_expression(2, "*", 2, array.elements[1])
        self.assert_infix_expression(3, "+", 3, array.elements[2])

    def test_parsing_index_expressions(self):
        lexer = Lexer("myArray[1 + 1]")
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)

        index_exp = program.statements[0].expression

        self.assertIsInstance(index_exp, IndexExpression)

        self.assert_identifier("myArray", index_exp.left)
        self.assert_infix_expression(1, "+", 1, index_exp.index)

    def test_parsing_empty_hash_literal(self):
        lexer = Lexer("{}")
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)

        hash_literal = program.statements[0].expression

        self.assertIsInstance(hash_literal, HashLiteral)

        self.assertEqual(0, len(hash_literal.pairs))

    def test_parsing_hash_literals_string_keys(self):
        lexer = Lexer('{"one": 1, "two": 2, "three": 3}')
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)

        hash_literal = program.statements[0].expression

        self.assertIsInstance(hash_literal, HashLiteral)

        self.assertEqual(3, len(hash_literal.pairs))

        expected_dct = {"one": 1, "two": 2, "three": 3}

        self.assertEqual(len(expected_dct), len(hash_literal.pairs))

        for actual_key, actual_value in hash_literal.pairs.items():
            self.assertIsInstance(actual_key, StringLiteral)
            expected_value = expected_dct.get(str(actual_key))
            self.assert_int_literal(expected_value, actual_value)

    def test_parsing_hash_literals_boolean_keys(self):
        lexer = Lexer("{true: 1, false: 2}")
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)

        hash_literal = program.statements[0].expression

        self.assertIsInstance(hash_literal, HashLiteral)

        expected_dct = {"true": 1, "false": 2}

        self.assertEqual(len(expected_dct), len(hash_literal.pairs))

        for actual_key, actual_value in hash_literal.pairs.items():
            self.assertIsInstance(actual_key, BooleanLiteral)
            expected_value = expected_dct.get(str(actual_key))
            self.assert_int_literal(expected_value, actual_value)

    def test_parsing_hash_literals_integer_keys(self):
        lexer = Lexer("{1: 1, 2: 2, 3: 3}")
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)

        hash_literal = program.statements[0].expression

        self.assertIsInstance(hash_literal, HashLiteral)

        self.assertEqual(3, len(hash_literal.pairs))

        expected_dct = {"1": 1, "2": 2, "3": 3}

        self.assertEqual(len(expected_dct), len(hash_literal.pairs))

        for actual_key, actual_value in hash_literal.pairs.items():
            self.assertIsInstance(actual_key, IntegerLiteral)
            expected_value = expected_dct.get(str(actual_key))
            self.assert_int_literal(expected_value, actual_value)

    def test_parsing_hash_literals_with_expressions(self):
        lexer = Lexer('{"one": 0 + 1, "two": 10 - 8, "three": 15 / 5}')
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assert_parser_errors(parser)

        hash_literal = program.statements[0].expression
        self.assertIsInstance(hash_literal, HashLiteral)

        self.assertEqual(3, len(hash_literal.pairs))

        expected_dct = {
            "one": lambda e: self.assert_infix_expression(0, "+", 1, e),
            "two": lambda e: self.assert_infix_expression(10, "-", 8, e),
            "three": lambda e: self.assert_infix_expression(15, "/", 5, e),
        }

        self.assertEqual(len(expected_dct), len(hash_literal.pairs))

        for actual_key, actual_value in hash_literal.pairs.items():
            self.assertIsInstance(actual_key, StringLiteral)
            test_fn = expected_dct.get(str(actual_key))
            test_fn(actual_value)

    def assert_literal_expression(self, expected, exp):
        if isinstance(expected, bool):
            self.assert_bool_literal(expected, exp)
        elif isinstance(expected, int):
            self.assert_int_literal(expected, exp)
        elif isinstance(expected, str):
            self.assert_identifier(expected, exp)
        else:
            self.fail(f"Cannot assert expression '{exp}'")

    def assert_identifier(self, value, exp):
        self.assertIsInstance(exp, Identifier)
        self.assertEqual(value, exp.value)
        self.assertEqual(value, exp.token_literal())

    def assert_infix_expression(self, left, operator, right, exp):
        self.assertIsInstance(exp, InfixExpression)
        self.assert_literal_expression(left, exp.left)
        self.assertEqual(operator, exp.operator)
        self.assert_literal_expression(right, exp.right)

    def assert_let_statement(self, name, statement):
        self.assertEqual("let", statement.token_literal())
        self.assertIsInstance(statement, LetStatement)
        self.assertEqual(name, statement.name.value)
        self.assertEqual(name, statement.name.token_literal())

    def assert_int_literal(self, value, literal):
        self.assertIsInstance(literal, IntegerLiteral)
        self.assertEqual(value, literal.value)
        self.assertEqual(str(value), literal.token_literal())

    def assert_bool_literal(self, value, bl):
        self.assertIsInstance(bl, BooleanLiteral)
        self.assertEqual(value, bl.value)
        self.assertEqual(str(value).lower(), bl.token_literal())

    def assert_parser_errors(self, parser):
        if parser.errors:
            parser.print_errors()
            self.fail("Parser encountered errors!")


if __name__ == "__main__":
    unittest.main()
