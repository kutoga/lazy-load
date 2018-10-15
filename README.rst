ℒazy-ℒoad
=========

.. image:: https://img.shields.io/pypi/v/lazy_load.svg
    :target: https://pypi.python.org/pypi/lazy_load
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/kutoga/lazy-load.png
   :target: https://travis-ci.org/kutoga/lazy-load
   :alt: Latest Travis CI build status

A minimalistic interface that allows lazy evaluation of expressions and function calls.

Note: This small library is highly based on `python-lazy-object-proxy`.

Why using ℒazy-ℒoad? Lazy loading in general may make some software implementations much more efficient.
Especially if it is not known if some data has to be loaded or not. Often the resulting code is less efficient,
because eager loading is used or the code is not elegant, because one has to program (somehow) lazy loading.

Advantages of this library are that lazy-loading may be used quite elegant and effective.

Examples
^^^^^^^^

In a loop it might happen that a special condition appears once or even more often. If this is the case,
an expensive function `expensive_function` is called and on the resulting object an operation has
to be done. If the expensive function had to called more than once, than the result object may be reused.

Possible implementation:


.. code:: python

    def expensive_function():
        print("function evaluation")
        ...
        return result

    obj = None
    for x, y, p in get_coordinates():
        if test_for_something(x, y, p):
            if obj is None:
                obj = expensive_function()
            obj.do_something(x, y)

Given this library, it might be done like this:


.. code:: python

    from lazy_load import lazy

    def expensive_function():
        print("function evaluation")
        ...
        return result

    obj = lazy(expensive_function)
    for x, y, p in get_coordinates():
        if test_for_something(x, y, p):
            obj.do_something(x, y)

There are similar situations outside of loops. The implementation without `lazy-load` might look like this:


.. code:: python

    def expensive_function():
        print("function evaluation")
        ...
        return result

    obj = None
    def get_obj():
        global obj
        if obj is None:
            obj = expensive_function()
        return obj

    if condition_a:
        get_obj().xyz()
    if condition_b:
        do_something()
    if condition_c:
        get_obj().abc()

This code can be realized much easier with `lazy-load`. Not only is the code shorter, but it is also more readable:


.. code:: python

    from lazy_load import lazy

    def expensive_function():
        print("function evaluation")
        ...
        return result

    obj = lazy(expensive_function)

    if condition_a:
        obj.xyz()
    if condition_b:
        do_something()
    if condition_c:
        obj.abc()

It might be the case that the expensive function is used more often and always a lazy evaluation is done.
In this case, a decorator might be used to indicate that all function calls to this function shall be lazily
evaluated. This makes it possible to normally use the function. The behaviour is still the same like in the first example:


.. code:: python

    from lazy_load import lazy_func

    @lazy_func
    def expensive_function():
        print("function evaluation")
        ...
        return result

    obj = expensive_function()
    for x, y, p in get_coordinates():
        if test_for_something(x, y, p):
            obj.do_something(x, y)

A lazy evaluation of functions / methods calls might be done with the `@lazy_func` decorator of with the `lazy`-call. This was already
shown, therefore the following examples show how to do a one-shot lazy evaluation of a function call:


.. code:: python

    from lazy_load import lazy, lz

    def expensive_func(x, y):
        print(f"function evaluation with arguments x={x}, y={y}")
        ...
        return result

    # Possibility 1: Use `lazy` with a callable
    obj = lazy(lambda: expensive_func(a, b))

    # Possibility 2: If it doesn't matter if the argument expressions for the expensive-function are eager evaluated, the call may be simplified:
    obj = lazy(expensive_func, a, b)

    # Possibility 3: `lazy` has a short version / alias: `lz`
    obj = lz(expensive_func, a, b)

Python allows it to pass functions around: This is often used for callbacks, but also for other use cases.
Assuming an expensive function is passed to an object which calls this function and stores the result of
the function call in an attribute. Later it might happen that this attribute is used. Depending on the
program flow it also might happen that this attribute is not used. With a lazily evaluated function the
expensive function call is only executed if the result is really used. The lazily evaluated version of
a function has the exact same signature as the original function.

One might now like to have the possibility to on-the-fly convert a callable to a lazily evaluated callable.
This might be done in the following way:


.. code:: python

    from lazy_load import lazy_func, lf

    def expensive_func(x):
        print(f"function evaluation with argument x={x}")
        ...
        return result

    # Possibility 1: Use `lazy_func`.
    my_obj.do_something(f=lazy_func(expensive_func))

    # Possibility 2: Use `lf` which is an alias of `lazy_func`
    my_obj.do_something(f=lf(expensive_func))

    # Possibility 3: Use the `ℒ`-"operator"
    my_obj.do_something(f=ℒ[expensive_func])

Actually, I want to go deeper into the `ℒ`azy- or `ℒ`-"operator". This operator converts on-the-fly a function
to a lazily evaluated function. Another example:


.. code:: python

    from lazy_load import ℒ

    def test(name):
        print(f"hey {name}")
        return True

    res = test("peter")
    # prints "hey peter"

    test_l = ℒ[test]
    res = test_l("hans")
    # prints nothing

    if res:
        print("res is True")
    # prints "hey hans\nres is True"

It is also possible to convert multiple functions to lazily evaluated functions using `ℒ`:


.. code:: python

    from lazy_load import ℒ

    def f1(x):
        print(f"f1 {x}")
        return True

    def f2(x):
        print(f"f1 {x}")
        return True

    f1_l, f2_l, f3_l = ℒ[f1, f2, lambda x: x == 1]
    # This is equal to:
    f1_l = ℒ[f1]
    f2_l = ℒ[f2]
    f3_l = ℒ[lambda x: x == 1]

Finally, one might like to decorate a class in a way that all its public methods which have a return
value are lazily evaluated. Public methods are all methods that have a name not starting with `_`.
Methods with a return value are identificated by the given return type hint which must not be `None`.
This behaviour might be done with the `@lazy_class`-decorator (alias: `lc`):


.. code:: python

    from lazy_load import lazy_class

    @lazy_class
    class MyClass:
        def __init__(self):
            # Method name starts with "_" => is not public; therefore it is eager evaluated
            pass

        def setX(x) -> None:
            # Method does not return a value => therefore it is eager evaluated
            ...

        def do():
            # Method does not hav a return value type hint =>  therefore it is eager evaluated
            ...

        def compute() -> int:
            # Method will always be lazily evaluated
            ...
            return result

Finally, it is also possible to force the evaluation of a lazy loading object by using `force_eval` (alias `fe`).
This function can safely to used to non-lazy loading objects: It is then just equal to the identity function.


.. code:: python

    from lazy_load import lazy, force_eval

    def f1(x):
        print(f"f1 {x}")
        return True

    lazy_obj = lazy(f1, 1)

    # The following expression prints "f1 1" and returns "True"
    force_eval(lazy_obj)

The `force_eval` function may also be applied to lazy-functions (which are created with `lazy_func(x)`, `@lazy_func`
or with `ℒ`). This restores the original non-lazy / eager function. For non-lazy functions this call has no effect:


.. code:: python

    from lazy_load import lazy_func, force_eval

    @lazy_func
    def f(x):
        print("hey")
        return x**2

    # The following line prints nothing
    obj = f(2)

    f_eager = force_eval(f)

    # The following line prints "hey" and "obj" has immediatly the value "4"
    obj = f_eager(2)


Installation
------------

`pip install lazy-load`

Requirements
^^^^^^^^^^^^

Python 3.6 or Python 3.7.

Licence
-------

MIT

Authors
-------

`lazy_load` was written by `Benjamin Bruno Meier <benjamin.meier70@gmail.com>`_.
