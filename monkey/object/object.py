from enum import Enum


class ObjectType(Enum):
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    STRING = "STRING"
    NULL = "NULL"

    ARRAY = "ARRAY"
    HASH = "HASH"

    RETURN_VALUE = "RETURN_VALUE"
    FUNCTION = "FUNCTION"
    BUILTIN = "BUILTIN"
    ERROR = "ERROR"


class Object:
    def type(self):
        raise NotImplementedError()


class Hashable:
    def hash_key(self):
        raise NotImplementedError()


class Integer(Object, Hashable):
    def __init__(self, value):
        self.value = value

    def type(self):
        return ObjectType.INTEGER

    def __str__(self):
        return str(self.value)

    def hash_key(self):
        return HashKey(self.type(), hash(self.value))


class Boolean(Object, Hashable):
    def __init__(self, value):
        self.value = value

    def type(self):
        return ObjectType.BOOLEAN

    def __str__(self):
        return str(self.value).lower()

    def hash_key(self):
        value = 1 if self.value else 0
        return HashKey(self.type(), value)


class Null(Object):
    def type(self):
        return ObjectType.NULL

    def __str__(self):
        return "null"


class ReturnValue(Object):
    def __init__(self, value):
        self.value = value

    def type(self):
        return ObjectType.RETURN_VALUE

    def __str__(self):
        return str(self.value)


class Error(Object):
    def __init__(self, message):
        self.message = message

    def type(self):
        return ObjectType.ERROR

    def __str__(self):
        return f"ERROR: {self.message}"


class Function(Object):
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def type(self):
        return ObjectType.FUNCTION

    def __str__(self):
        fn = f"fn({', '.join(str(p) for p in self.params)}) "
        fn += "{"
        fn += f"  {str(self.body)}  "
        fn += "}"
        return fn


class String(Object, Hashable):
    def __init__(self, value):
        self.value = value

    def type(self):
        return ObjectType.STRING

    def __str__(self):
        return self.value

    def hash_key(self):
        return HashKey(self.type(), hash(self.value))


class BuiltIn(Object):
    def __init__(self, function):
        self.function = function

    def type(self):
        return ObjectType.BUILTIN

    def __str__(self):
        return "builtin function"


class Array(Object):
    def __init__(self, elements):
        self.elements = elements

    def type(self):
        return ObjectType.ARRAY

    def __str__(self):
        elements = [str(e) for e in self.elements]
        return f"[{', '.join(elements)}]"


class HashKey:
    def __init__(self, obj_type, value):
        self.type = obj_type
        self.value = value

    def __eq__(self, other) -> bool:
        if isinstance(other, HashKey):
            if other.type == self.type and other.value == self.value:
                return True

        return False

    def __ne__(self, other) -> bool:
        if isinstance(other, HashKey):
            if other.type == self.type and other.value == self.value:
                return False

        return True

    def __hash__(self) -> int:
        return hash(f"{self.type}-{self.value}")


class HashPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Hash(Object):
    def __init__(self, pairs):
        self.pairs = pairs

    def type(self):
        return ObjectType.HASH

    def __len__(self):
        return len(self.pairs)

    def __str__(self):
        fmt = "{"
        pairs = [
            f"{str(pair.key)}: {str(pair.value)}"
            for pair in self.pairs.values()
        ]
        fmt += ", ".join(pairs) + "}"
        return fmt


NULL = Null()
TRUE = Boolean(True)
FALSE = Boolean(False)
