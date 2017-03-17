# Embedded file name: scripts/common/Lib/test/test_copy_reg.py
import copy_reg
import unittest
from test import test_support
from test.pickletester import ExtensionSaver

class C:
    pass


class WithoutSlots(object):
    pass


class WithWeakref(object):
    __slots__ = ('__weakref__',)


class WithPrivate(object):
    __slots__ = ('__spam',)


class WithSingleString(object):
    __slots__ = 'spam'


class WithInherited(WithSingleString):
    __slots__ = ('eggs',)


class CopyRegTestCase(unittest.TestCase):

    def test_class(self):
        self.assertRaises(TypeError, copy_reg.pickle, C, None, None)
        return

    def test_noncallable_reduce(self):
        self.assertRaises(TypeError, copy_reg.pickle, type(1), 'not a callable')

    def test_noncallable_constructor(self):
        self.assertRaises(TypeError, copy_reg.pickle, type(1), int, 'not a callable')

    def test_bool(self):
        import copy
        self.assertEqual(True, copy.copy(True))

    def test_extension_registry(self):
        mod, func, code = ('junk1 ', ' junk2', 43981)
        e = ExtensionSaver(code)
        try:
            self.assertRaises(ValueError, copy_reg.remove_extension, mod, func, code)
            copy_reg.add_extension(mod, func, code)
            self.assertTrue(copy_reg._extension_registry[mod, func] == code)
            self.assertTrue(copy_reg._inverted_registry[code] == (mod, func))
            self.assertNotIn(code, copy_reg._extension_cache)
            copy_reg.add_extension(mod, func, code)
            self.assertRaises(ValueError, copy_reg.add_extension, mod, func, code + 1)
            self.assertRaises(ValueError, copy_reg.remove_extension, mod, func, code + 1)
            self.assertRaises(ValueError, copy_reg.add_extension, mod[1:], func, code)
            self.assertRaises(ValueError, copy_reg.remove_extension, mod[1:], func, code)
            self.assertRaises(ValueError, copy_reg.add_extension, mod, func[1:], code)
            self.assertRaises(ValueError, copy_reg.remove_extension, mod, func[1:], code)
            if code + 1 not in copy_reg._inverted_registry:
                self.assertRaises(ValueError, copy_reg.remove_extension, mod[1:], func[1:], code + 1)
        finally:
            e.restore()

        self.assertNotIn((mod, func), copy_reg._extension_registry)
        for code in (1, 2147483647):
            e = ExtensionSaver(code)
            try:
                copy_reg.add_extension(mod, func, code)
                copy_reg.remove_extension(mod, func, code)
            finally:
                e.restore()

        for code in (-1, 0, 2147483648L):
            self.assertRaises(ValueError, copy_reg.add_extension, mod, func, code)

    def test_slotnames(self):
        self.assertEqual(copy_reg._slotnames(WithoutSlots), [])
        self.assertEqual(copy_reg._slotnames(WithWeakref), [])
        expected = ['_WithPrivate__spam']
        self.assertEqual(copy_reg._slotnames(WithPrivate), expected)
        self.assertEqual(copy_reg._slotnames(WithSingleString), ['spam'])
        expected = ['eggs', 'spam']
        expected.sort()
        result = copy_reg._slotnames(WithInherited)
        result.sort()
        self.assertEqual(result, expected)


def test_main():
    test_support.run_unittest(CopyRegTestCase)


if __name__ == '__main__':
    test_main()