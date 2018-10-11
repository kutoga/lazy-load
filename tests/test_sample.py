from lazy_object_proxy import Proxy
from lazy_load import *


def test_aliases():
    assert lazy is lz

    assert lazy_func is lf
    assert lazy_func is ℒ

    assert lazy_class is lc

    assert force_eval is fe

def test_lazy_simple_expression_evaluation():
    evaluated = False
    def add(x, y):
        nonlocal evaluated
        evaluated = True
        return x + y

    res = lazy(lambda: add(1, 2))
    assert not evaluated
    assert isinstance(res, Proxy)
    assert res == 3
    assert evaluated
    assert isinstance(res, int)

def test_lazy_function_with_eagle_argument_evaluation():
    evaluated = False
    def add(x, y):
        nonlocal evaluated
        evaluated = True
        return x + y

    res = lazy(add, 1, 2)
    assert not evaluated
    assert isinstance(res, Proxy)
    assert res == 3
    assert evaluated
    assert isinstance(res, int)

def test_lazy_function_evaluation():
    evaluated = False
    def add(x, y):
        nonlocal evaluated
        evaluated = True
        return x + y

    lazy_add = ℒ[add] # this is equivalent to lazy_func(add)
    res = lazy_add(1, 2)
    assert not evaluated
    assert isinstance(res, Proxy)
    assert res == 3
    assert evaluated
    assert isinstance(res, int)

def test_lazy_function_decorator():
    evaluated = False

    @lazy_func
    def lazy_add(x, y):
        nonlocal evaluated
        evaluated = True
        return x + y

    res = lazy_add(1, 2)
    assert not evaluated
    assert isinstance(res, Proxy)
    assert res == 3
    assert evaluated
    assert isinstance(res, int)

def test_lazy_class():
    evaluated = False

    @lazy_class
    class LazyClass:
        def __init__(self, n):
            self._n = n

        def add(self, m) -> int:
            nonlocal evaluated
            evaluated = True
            return self._n + m

        def sub(self, m) -> None: # Return type is None: This function should not be lazy evaluated
            nonlocal evaluated
            evaluated = True
            return self._n - m

        @lazy_func
        def mul(self, m) -> None: # Return type is None: This function should not be lazy evaluated; BUT there is the decorater: it makes the function lazy
            nonlocal evaluated
            evaluated = True
            return self._n * m

        def _div(self, m) -> int: # Non-public functions are never made lazy by lazy_class
            nonlocal evaluated
            evaluated = True
            return self._n // m

    lazy_obj = LazyClass(1)

    res = lazy_obj.add(2)
    assert not evaluated
    assert isinstance(res, Proxy)
    assert res == 3
    assert evaluated
    assert isinstance(res, int)

    evaluated = False
    res = lazy_obj.sub(2)
    assert not isinstance(res, Proxy)
    assert evaluated
    assert res == -1

    evaluated = False
    res = lazy_obj.mul(2)
    assert not evaluated
    assert isinstance(res, Proxy)
    assert res == 2
    assert evaluated
    assert isinstance(res, int)

    evaluated = False
    res = lazy_obj._div(1)
    assert not isinstance(res, Proxy)
    assert evaluated
    assert res == 1

def test_force_eval_on_objects():
    evaluated = False
    def do_something(x, y):
        nonlocal evaluated
        evaluated = True

    res = lazy(do_something, 1, 2)
    assert not evaluated
    force_eval(res)
    assert evaluated

def test_force_eval_on_callables():
    evaluated = False
    def do_something():
        nonlocal evaluated
        evaluated = True
    do_something_lazy = ℒ[do_something]
    assert do_something_lazy is not do_something
    assert fe(do_something_lazy) is do_something
    assert not evaluated

def test_multiple_lazy_on_expression():
    evaluated = False
    def add(x, y):
        nonlocal evaluated
        evaluated = True
        return x + y

    res = lazy(lambda: add(1, 2))
    assert res is not add
    res2 = lazy(res)
    assert res is res2
    assert not evaluated
    assert res == 3
    assert evaluated
    assert res2 == 3

    evaluated = False
    res = lazy(lazy(lazy(lambda: add(1, 2))))
    assert res is not add
    assert not evaluated
    assert res == 3
    assert evaluated

def test_multiple_lazy_onfunction():
    evaluated = False
    def add(x, y):
        nonlocal evaluated
        evaluated = True
        return x + y

    add_l1 = ℒ[add]
    add_l2 = ℒ[add_l1]

    assert add_l1 is not add
    assert add_l1 is add_l2
    res = add_l2(1, 2)
    assert not evaluated
    assert res == 3
    assert evaluated
