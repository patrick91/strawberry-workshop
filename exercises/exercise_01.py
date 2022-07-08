def a_function_that_has_type_hints(name: str) -> int:
    return len(name)


def print_type_hints(func):
    return_type = func.__annotations__["return"]
    arguments = {k: v for k, v in func.__annotations__.items() if k != "return"}

    print(f"Type hints for {func.__name__}:")
    print(f"Return type: {return_type}")
    print("Arguments:")

    for name, type_hint in arguments.items():
        print(f"    {name}: {type_hint}")


print_type_hints(a_function_that_has_type_hints)
