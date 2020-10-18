import sys

from evaluator.nodevisitor import NodeVisitor
from lexer.lexer import Lexer
from object.environment import Environment
from parser.parser import Parser


def main():
    if len(sys.argv) > 1:
        program = open_file_or_fail(sys.argv[1])
        run_program(program)
    else:
        repl()


def open_file_or_fail(file):
    try:
        with open(file, "r") as f:
            return f.read()
    except OSError as e:
        print(f"Could not open {file}!")
        sys.exit(e.errno)


def repl():
    print("Use exit() or Ctrl-D (i.e. EOF) to exit")

    env = Environment()

    while True:
        try:
            i = input(">> ")
        except EOFError:
            return

        if i == "exit()":
            return

        run_program(i, env)


def run_program(p, env=None):
    env = Environment() if env is None else env

    evaluator = NodeVisitor()
    lexer = Lexer(p)
    parser = Parser(lexer)
    program = parser.parse_program()

    if parser.errors:
        parser.print_errors()
        return

    evaluated = evaluator.evaluate(program, env)

    if evaluated is not None:
        print(evaluated)


if __name__ == "__main__":
    main()
