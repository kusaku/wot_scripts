# Embedded file name: scripts/common/Lib/test/test_future1.py
"""This is a test"""
from __future__ import nested_scopes, nested_scopes

def f(x):

    def g(y):
        return x + y

    return g


result = f(2)(4)