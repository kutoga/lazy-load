# -*- coding: utf-8 -*-
"""
ℒazy-ℒoad - A minimalistic interface that allows the lazy evaluation of expressions.
Additional functions and wrappers allow it to easily use the lazy evaluation for functions
and classes.
"""

from ._lazy_load import lazy, lz, lazy_func, lf, ℒ, lazy_class, lc, force_eval, fe

__version__ = '0.1.0'
__author__ = 'Benjamin Bruno Meier <benjamin.meier70@gmail.com>'

# __all__ is not used, because it is not possible to include there "ℒ":
# AttributeError: module 'lazy_load' has no attribute 'ℒ'
