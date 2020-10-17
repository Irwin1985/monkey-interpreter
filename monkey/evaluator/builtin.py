from object.object import Error, Integer, BuiltIn, String, Array, NULL


def len_fn(args):
    if len(args) != 1:
        return Error(f"wrong number of arguments. got={len(args)}, want=1")

    arg = args[0]
    if isinstance(arg, String):
        return Integer(len(arg.value))
    elif isinstance(arg, Array):
        return Integer(len(arg.elements))
    else:
        return Error(
            f"argument to 'len' not supported, got {arg.type().value}"
        )


def first_fn(args):
    if len(args) != 1:
        return Error(f"wrong number of arguments. got={len(args)}, want=1")

    if not isinstance(args[0], Array):
        return Error(
            f"argument to 'first' must be ARRAY, got {args[0].type().value}"
        )

    arr = args[0]

    return arr.elements[0] if len(arr.elements) > 0 else NULL


def last_fn(args):
    if len(args) != 1:
        return Error(f"wrong number of arguments. got={len(args)}, want=1")

    if not isinstance(args[0], Array):
        return Error(
            f"argument to 'last' must be ARRAY, got {args[0].type().value}"
        )

    arr = args[0].elements
    length = len(arr)

    return arr.elements[length - 1] if length > 0 else NULL


def rest_fn(args):
    if len(args) != 1:
        return Error(f"wrong number of arguments. got={len(args)}, want=1")

    if not isinstance(args[0], Array):
        return Error(
            f"argument to 'rest' must be ARRAY, got {args[0].type().value}"
        )

    arr = args[0].elements

    return Array(list(arr[1:])) if len(arr) > 0 else NULL


def push_fn(args):
    if len(args) != 2:
        return Error(f"wrong number of arguments. got={len(args)}, want=2")

    if not isinstance(args[0], Array):
        return Error(
            f"argument to 'push' must be ARRAY, got {args[0].type().value}"
        )

    new_arr = list(args[0].elements)
    new_arr.append(args[1])
    return Array(new_arr)


def puts_fn(args):
    print("\n".join([str(arg) for arg in args]))
    return NULL


BUILTIN = {
    "len": BuiltIn(len_fn),
    "first": BuiltIn(first_fn),
    "last": BuiltIn(last_fn),
    "rest": BuiltIn(rest_fn),
    "push": BuiltIn(push_fn),
    "puts": BuiltIn(puts_fn),
}
