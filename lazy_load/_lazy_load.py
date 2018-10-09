# -*- coding: utf-8 -*-
from typing import Callable, TypeVar, Type, Any, get_type_hints
from functools import wraps
from lazy_object_proxy import Proxy
import inspect

_T = TypeVar('T')
def lazy(f: Callable[..., _T], *args: str, **kwargs: str) -> _T:
    if not callable(f):
        raise ValueError('Invalid target function.')
    return Proxy(lambda: f(*args, **kwargs))
lz = lazy

_A, _R = TypeVar('A'), TypeVar('R')
class _LazyFunc:
    def __call__(self, original_function: Callable[[_A], _R]) -> Callable[[_A], _R]:
        @wraps(original_function)
        def _lazy_function(*args, **kwargs):
            return lazy(lambda: original_function(*args, **kwargs))
        return _lazy_function
    def __getitem__(self, original_function: Callable[[_A], _R]) -> Callable[[_A], _R]:
        return self(original_function)
lazy_func = _LazyFunc()
lf = lazy_func
ℒ = lazy_func

def lazy_class(cls: Type) -> Type:
    for name, f in inspect.getmembers(cls, predicate=inspect.isfunction):
        if name and name[0] == '_':
            continue
        if get_type_hints(f).get('return', None) is not None:
            setattr(cls, name, lazy_func[f])
    return cls
lc = lazy_class

def force_eval(obj: Any) -> Any:
    if type(obj) == Proxy:
        return obj.__wrapped__
    return obj
fe = force_eval


