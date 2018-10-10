# -*- coding: utf-8 -*-
from typing import Callable, TypeVar, Type, Any, get_type_hints
from functools import wraps
from lazy_object_proxy import Proxy
import inspect

_T = TypeVar('T')
def lazy(target: Callable[..., _T], *args: str, **kwargs: str) -> _T:
    if not callable(target):
        raise ValueError('Invalid target.')
    return Proxy(lambda: target(*args, **kwargs))
lz = lazy

_A, _R = TypeVar('A'), TypeVar('R')
class _LazyFunc:
    def __call__(self, original_function: Callable[[_A], _R]) -> Callable[[_A], _R]:
        @wraps(original_function)
        def _lazy_function(*args, **kwargs):
            return lazy(lambda: original_function(*args, **kwargs))
        _lazy_function.__wrapped_non_lazy_function__ = original_function
        return _lazy_function
    def __getitem__(self, original_functions: Callable) -> Callable:
        if isinstance(original_functions, tuple):
            return [self(original_function) for original_function in original_functions]
        else:
            return self(original_functions)
lazy_func = _LazyFunc()
lf = lazy_func
ℒ = lazy_func

def lazy_class(cls: Type) -> Type:
    for name, f in inspect.getmembers(cls, predicate=inspect.isfunction):
        if name and name[0] == '_':
            continue
        if get_type_hints(f).get('return', type(None)) is not type(None):
            setattr(cls, name, lazy_func[f])
    return cls
lc = lazy_class

def force_eval(obj: Any) -> Any:
    if type(obj) is Proxy:
        return obj.__wrapped__
    if callable(obj) and hasattr(obj, '__wrapped_non_lazy_function__'):
        return obj.__wrapped_non_lazy_function__
    return obj
fe = force_eval


