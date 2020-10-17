import unittest

from evaluator.evaluator import Evaluator
from lexer.lexer import Lexer
from object.environment import Environment
from object.object import Integer, Boolean, Null
from object.object import String, Error, Function, Array, TRUE, FALSE, Hash
from parser.parser import Parser


class TestEvaluator(unittest.TestCase):
    def test_eval_integer_expression(self):
        tests = [
            ["5", 5],
            ["10", 10],
            ["-5", -5],
            ["-10", -10],
            ["5 + 5 + 5 + 5 - 10", 10],
            ["2 * 2 * 2 * 2 * 2", 32],
            ["-50 + 100 + -50", 0],
            ["5 * 2 + 10", 20],
            ["5 + 2 * 10", 25],
            ["20 + 2 * -10", 0],
            ["50 / 2 * 2 + 10", 60],
            ["2 * (5 + 10)", 30],
            ["3 * 3 * 3 + 10", 37],
            ["3 * (3 * 3) + 10", 37],
            ["(5 + 10 * 2 + 15 / 3) * 2 + -10", 50],
        ]

        for tt in tests:
            actual = self.eval(tt[0])
            expected = tt[1]
            self.assert_integer_object(expected, actual)

    def test_eval_boolean_expression(self):
        tests = [
            ["true", True],
            ["false", False],
            ["1 < 2", True],
            ["1 > 2", False],
            ["1 < 1", False],
            ["1 > 1", False],
            ["1 == 1", True],
            ["1 != 1", False],
            ["1 == 2", False],
            ["1 != 2", True],
            ["true == true", True],
            ["false == false", True],
            ["true == false", False],
            ["true != false", True],
            ["false != true", True],
            ["(1 < 2) == true", True],
            ["(1 < 2) == false", False],
            ["(1 > 2) == true", False],
            ["(1 > 2) == false", True],
        ]

        for tt in tests:
            actual = self.eval(tt[0])
            expected = tt[1]
            self.assert_boolean_object(expected, actual)

    def test_bang_operator(self):
        tests = [
            ["!true", False],
            ["!false", True],
            ["!5", False],
            ["!!true", True],
            ["!!false", False],
            ["!!5", True],
        ]

        for tt in tests:
            actual = self.eval(tt[0])
            expected = tt[1]
            self.assert_boolean_object(expected, actual)

    def test_if_else_expressions(self):
        tests = [
            ["if (true) { 10 }", 10],
            ["if (false) { 10 }", "null"],
            ["if (1) { 10 }", 10],
            ["if (1 < 2) { 10 }", 10],
            ["if (1 > 2) { 10 }", "null"],
            ["if (1 > 2) { 10 } else { 20 }", 20],
            ["if (1 < 2) { 10 } else { 20 }", 10],
        ]

        for tt in tests:
            actual = self.eval(tt[0])
            if isinstance(tt[1], int):
                expected = tt[1]
                self.assert_integer_object(expected, actual)
            else:
                self.assertIsInstance(actual, Null)

    def test_while_expressions(self):
        test = "let x = 10; while (x > 0) { let x = x - 1; }; x;"

        actual = self.eval(test)
        self.assert_integer_object(0, actual)

    def test_return_statements(self):
        tests = [
            ["return 10;", 10],
            ["return 10; 9;", 10],
            ["return 2 * 5; 9;", 10],
            ["9; return 2 * 5; 9;", 10],
            [
                """if (10 > 1) {
                    if (10 > 1) {
                        return 10;
                    }
                    return 1;
                }""",
                10,
            ],
        ]

        for tt in tests:
            actual = self.eval(tt[0])
            expected = tt[1]
            self.assert_integer_object(expected, actual)

    def test_error_handling(self):
        tests = [
            ["5 + true;", "type mismatch: INTEGER + BOOLEAN"],
            ["5 + true; 5;", "type mismatch: INTEGER + BOOLEAN"],
            ["-true;", "unknown operator: -BOOLEAN"],
            ["true + false;", "unknown operator: BOOLEAN + BOOLEAN"],
            [
                "true + false + true + false;",
                "unknown operator: BOOLEAN + BOOLEAN",
            ],
            ["5; true + false; 5", "unknown operator: BOOLEAN + BOOLEAN"],
            [
                "if (10 > 1) { true + false; }",
                "unknown operator: BOOLEAN + BOOLEAN",
            ],
            [
                "foobar",
                "identifier not found: foobar",
            ],
            ['"Hello" - "World"', "unknown operator: STRING - STRING"],
            [
                '{"name": "Monkey"}[fn(x) { x }];',
                "unusable as hash key: FUNCTION",
            ],
        ]

        for tt in tests:
            actual = self.eval(tt[0])
            expected = tt[1]
            self.assertIsInstance(actual, Error)
            self.assertEqual(expected, actual.message)

    def test_let_statements(self):
        tests = [
            ["let a = 5; a;", 5],
            ["let a = 5 * 5; a;", 25],
            ["let a = 5; let b = a; b;", 5],
            ["let a = 5; let b = a; let c = a + b + 5; c", 15],
        ]

        for tt in tests:
            actual = self.eval(tt[0])
            expected = tt[1]
            self.assert_integer_object(expected, actual)

    def test_function_object(self):
        test = "fn(x) { x + 2; };"

        actual = self.eval(test)

        self.assertIsInstance(actual, Function)
        self.assertEqual(1, len(actual.params))
        self.assertEqual("x", str(actual.params[0]))
        self.assertEqual("(x + 2)", str(actual.body))

    def test_function_application(self):
        tests = [
            ["let identity = fn(x) { x; }; identity(5);", 5],
            ["let identity = fn(x) { return x; }; identity(5);", 5],
            ["let double = fn(x) { x * 2; }; double(5);", 10],
            ["let add = fn(x, y) { x + y; }; add(5, 5);", 10],
            ["let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", 20],
            ["fn(x) { x; }(5)", 5],
        ]

        for tt in tests:
            actual = self.eval(tt[0])
            expected = tt[1]
            self.assert_integer_object(expected, actual)

    def test_closures(self):
        test = """
        let newAdder = fn(x) {
            fn(y) { x + y };
        };
        
        let addTwo = newAdder(2);
        addTwo(2);
        """

        actual = self.eval(test)
        self.assert_integer_object(4, actual)

    def test_string_literal(self):
        test = '"Hello World!"'
        actual = self.eval(test)
        self.assert_string_object("Hello World!", actual)

    def test_string_concatenation(self):
        test = '"Hello" + " " + "World!"'
        actual = self.eval(test)
        self.assert_string_object("Hello World!", actual)

    def test_built_in_functions(self):
        tests = [
            ['len("")', 0],
            ['len("four")', 4],
            ['len("hello world")', 11],
            ["len(1)", "argument to 'len' not supported, got INTEGER"],
            ['len("one", "two")', "wrong number of arguments. got=2, want=1"],
        ]

        for tt in tests:
            evaluated = self.eval(tt[0])
            expected = tt[1]

            if isinstance(expected, int):
                self.assert_integer_object(expected, evaluated)
            elif isinstance(expected, str):
                self.assertIsInstance(evaluated, Error)
                self.assertEqual(expected, evaluated.message)

    def test_array_literals(self):
        test = "[1, 2 * 2, 3 + 3]"

        evaluated = self.eval(test)

        self.assertIsInstance(evaluated, Array)
        self.assertEqual(3, len(evaluated.elements))

        self.assert_integer_object(1, evaluated.elements[0])
        self.assert_integer_object(4, evaluated.elements[1])
        self.assert_integer_object(6, evaluated.elements[2])

    def test_array_index_expressions(self):
        tests = [
            ["[1, 2, 3][0]", 1],
            ["[1, 2, 3][1]", 2],
            ["[1, 2, 3][2]", 3],
            ["let i = 0; [1][i];", 1],
            ["[1, 2, 3][1 + 1];", 3],
            ["let myArray = [1, 2, 3]; myArray[2];", 3],
            [
                "let myArray = [1, 2, 3]; myArray[0] + myArray[1] + myArray[2];",
                6,
            ],
            ["let myArray = [1, 2, 3]; let i = myArray[0]; myArray[i];", 2],
            ["[1, 2, 3][3]", None],
            ["[1, 2, 3][-1]", None],
        ]

        for tt in tests:
            evaluated = self.eval(tt[0])

            if isinstance(evaluated, Integer):
                self.assert_integer_object(tt[1], evaluated)
            else:
                self.assertIsInstance(evaluated, Null)

    def test_hash_literals(self):
        test = """
            let two = "two";
            {
                "one": 10 - 9,
                two: 1 + 1,
                "thr" + "ee": 6 / 2,
                4: 4,
                true: 5,
                false: 6
            }
        """
        actual = self.eval(test)

        self.assertIsInstance(actual, Hash)

        expected = {
            String("one").hash_key(): 1,
            String("two").hash_key(): 2,
            String("three").hash_key(): 3,
            Integer(4).hash_key(): 4,
            TRUE.hash_key(): 5,
            FALSE.hash_key(): 6,
        }

        self.assertEqual(len(expected), len(actual))

        for expected_key, expected_value in expected.items():
            actual_value = actual.pairs.get(expected_key).value
            self.assert_integer_object(expected_value, actual_value)

    def test_hash_index_expressions(self):
        tests = [
            ['{"foo": 5}["foo"]', 5],
            ['{"foo": 5}["bar"]', None],
            ['let key = "foo"; {"foo": 5}[key]', 5],
            ['{}["foo"]', None],
            ['{"foo": 5}["bar"]', None],
            ["{5: 5}[5]", 5],
            ["{true: 5}[true]", 5],
            ["{false: 5}[false]", 5],
        ]

        for tt in tests:
            actual = self.eval(tt[0])

            if isinstance(actual, Integer):
                expected = tt[1]
                self.assert_integer_object(expected, actual)
            else:
                self.assertIsInstance(actual, Null)

    def assert_integer_object(self, expected_value, int_obj):
        self.assertIsInstance(int_obj, Integer)
        self.assertEqual(expected_value, int_obj.value)

    def assert_boolean_object(self, expected_value, bool_obj):
        self.assertIsInstance(bool_obj, Boolean)
        self.assertEqual(expected_value, bool_obj.value)

    def assert_string_object(self, expected_value, string_obj):
        self.assertIsInstance(string_obj, String)
        self.assertEqual(expected_value, string_obj.value)

    @staticmethod
    def eval(test_input):
        lexer = Lexer(test_input)
        parser = Parser(lexer)
        program = parser.parse_program()
        return Evaluator().evaluate(program, Environment())


if __name__ == "__main__":
    unittest.main()
