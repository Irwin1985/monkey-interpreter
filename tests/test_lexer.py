import unittest

from lexer.lexer import Lexer
from tok.tok import Token


class TestLexer(unittest.TestCase):
    def test_tokens(self):
        lexer = Lexer(
            """
        let five = 5;
        let ten = 10;
        
        let add = fn(x, y) {
            x + y;
        };
        
        let result = add(five, ten);
        !-/*5;
        5 < 10 > 5;
        
        if (5 < 10) {
            return true;
        } else {
            return false;
        }
        
        10 == 10;
        10 != 9;
        "foobar"
        "foo bar"
        [1, 2];
        {"foo": "bar"}
        """
        )

        expected_tokens = [
            Token(Token.LET, "let"),
            Token(Token.IDENT, "five"),
            Token(Token.ASSIGN, "="),
            Token(Token.INT, "5"),
            Token(Token.SEMICOLON, ";"),
            Token(Token.LET, "let"),
            Token(Token.IDENT, "ten"),
            Token(Token.ASSIGN, "="),
            Token(Token.INT, "10"),
            Token(Token.SEMICOLON, ";"),
            Token(Token.LET, "let"),
            Token(Token.IDENT, "add"),
            Token(Token.ASSIGN, "="),
            Token(Token.FUNCTION, "fn"),
            Token(Token.LPAREN, "("),
            Token(Token.IDENT, "x"),
            Token(Token.COMMA, ","),
            Token(Token.IDENT, "y"),
            Token(Token.RPAREN, ")"),
            Token(Token.LBRACE, "{"),
            Token(Token.IDENT, "x"),
            Token(Token.PLUS, "+"),
            Token(Token.IDENT, "y"),
            Token(Token.SEMICOLON, ";"),
            Token(Token.RBRACE, "}"),
            Token(Token.SEMICOLON, ";"),
            Token(Token.LET, "let"),
            Token(Token.IDENT, "result"),
            Token(Token.ASSIGN, "="),
            Token(Token.IDENT, "add"),
            Token(Token.LPAREN, "("),
            Token(Token.IDENT, "five"),
            Token(Token.COMMA, ","),
            Token(Token.IDENT, "ten"),
            Token(Token.RPAREN, ")"),
            Token(Token.SEMICOLON, ";"),
            Token(Token.BANG, "!"),
            Token(Token.MINUS, "-"),
            Token(Token.SLASH, "/"),
            Token(Token.ASTERISK, "*"),
            Token(Token.INT, "5"),
            Token(Token.SEMICOLON, ";"),
            Token(Token.INT, "5"),
            Token(Token.LT, "<"),
            Token(Token.INT, "10"),
            Token(Token.GT, ">"),
            Token(Token.INT, "5"),
            Token(Token.SEMICOLON, ";"),
            Token(Token.IF, "if"),
            Token(Token.LPAREN, "("),
            Token(Token.INT, "5"),
            Token(Token.LT, "<"),
            Token(Token.INT, "10"),
            Token(Token.RPAREN, ")"),
            Token(Token.LBRACE, "{"),
            Token(Token.RETURN, "return"),
            Token(Token.TRUE, "true"),
            Token(Token.SEMICOLON, ";"),
            Token(Token.RBRACE, "}"),
            Token(Token.ELSE, "else"),
            Token(Token.LBRACE, "{"),
            Token(Token.RETURN, "return"),
            Token(Token.FALSE, "false"),
            Token(Token.SEMICOLON, ";"),
            Token(Token.RBRACE, "}"),
            Token(Token.INT, "10"),
            Token(Token.EQ, "=="),
            Token(Token.INT, "10"),
            Token(Token.SEMICOLON, ";"),
            Token(Token.INT, "10"),
            Token(Token.NOT_EQ, "!="),
            Token(Token.INT, "9"),
            Token(Token.SEMICOLON, ";"),
            Token(Token.STRING, "foobar"),
            Token(Token.STRING, "foo bar"),
            Token(Token.LBRACKET, "["),
            Token(Token.INT, "1"),
            Token(Token.COMMA, ","),
            Token(Token.INT, "2"),
            Token(Token.RBRACKET, "]"),
            Token(Token.SEMICOLON, ";"),
            Token(Token.LBRACE, "{"),
            Token(Token.STRING, "foo"),
            Token(Token.COLON, ":"),
            Token(Token.STRING, "bar"),
            Token(Token.RBRACE, "}"),
            Token(Token.EOF, ""),
        ]

        for expected_token in expected_tokens:
            actual = lexer.next_token()

            self.assertEqual(expected_token.token_type, actual.token_type)
            self.assertEqual(expected_token.literal, actual.literal)


if __name__ == "__main__":
    unittest.main()
