from typing import get_type_hints, Tuple

def allow_packing(func):
    typehints = get_type_hints(func)
    type_list = tuple([ typehints[item] for item in typehints if item != 'return' ])
    def f(x: Tuple[type_list]) -> typehints['return']:
        return func(*x)

    f.__name__ = f"{func.__name__}_packed"
    return f


def allow_void(func):
    func_typehints = get_type_hints(func)
    del func_typehints['return']
    def f(*args, **kwargs) -> None:
        _ = func(*args, **kwargs)
        return

    f.__annotations__ = func_typehints
    f.__annotations__['return'] = type(None)
    f.__name__ = f"{func.__name__}_voided"
    return f


def convert_void(func):
    func_typehints = get_type_hints(func)
    def f(*args, **kwargs):
        return func()

    f.__annotations__ = {'n': type(None), 'return': func_typehints['return']}
    f.__name__ = f"{func.__name__}_void_converted"
    return f


def compose(f, g, doc_string=None, name=None):
    f_typehints = get_type_hints(f)
    g_typehints = get_type_hints(g)
    try:
        assert 'return' in f_typehints
    except Exception:
        raise AttributeError("Must be explicit in your void return types for first function")
    try:
        assert 'return' in g_typehints
    except Exception:
        raise AttributeError("Must be explicit in your void return types for second function")
    #Want to create pipeline of functions so turn multiple arguments into tuples
    if len(g_typehints) > 2:
        raise AttributeError("Cannot compose second function, try using 'allow_packing'")
        return
    if len(g_typehints) == 1:
        raise AttributeError("Cannot compose both functions, try using 'allow_void' and/or 'convert_void'")
        return             
    g_param_type = [ g_typehints[item] for item in g_typehints.keys() if item != 'return' ][0]
    f_return_type = f_typehints['return']
    if f_return_type != g_param_type:
        raise AttributeError("Cannot compose functions due to type mismatch")
    def gof(*args, **kwargs) -> g_typehints['return']:
        return g(f(*args, **kwargs))

    new_typehints = f_typehints.copy()
    del new_typehints['return']
    new_typehints.update({'return': g_typehints['return']})
    gof.__annotations__ = new_typehints
    if doc_string:
        gof.__doc__ = doc_string
    if name:
        gof.__name__ = name
    else:
        gof.__name__ = f"{g.__name__}_composed_{f.__name__}"
    return gof


class Composer:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def compose(self, g):
        try:
            return Composer(compose(self.func, g))
        except Exception:
            raise AttributeError(f"Unable to compose {g.__name__} and {self.func.__name__}")