from typing import Dict, Any
Function = Any

registry: Dict[str, Function] = dict()


def export(*arg, **kwargs):
    """decorator to export functions in the registry
    """

    def export_inner(func):
        registry[kwargs['name']] = func

    return export_inner


if __name__ == "__main__":
    test_name = 'sum'

    @export(name=test_name)
    def func_sum(a, b):
        return a + b

    print(registry[test_name](2, 3))
