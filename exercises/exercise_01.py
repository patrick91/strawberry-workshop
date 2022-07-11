def a_function_that_has_type_hints(name: str) -> int:
    return len(name)


def print_type_hints(func):
    ...


print_type_hints(a_function_that_has_type_hints)
