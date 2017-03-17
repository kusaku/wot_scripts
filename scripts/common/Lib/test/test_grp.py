# Embedded file name: scripts/common/Lib/test/test_grp.py
"""Test script for the grp module."""
import unittest
from test import test_support
grp = test_support.import_module('grp')

class GroupDatabaseTestCase(unittest.TestCase):

    def check_value(self, value):
        self.assertEqual(len(value), 4)
        self.assertEqual(value[0], value.gr_name)
        self.assertIsInstance(value.gr_name, basestring)
        self.assertEqual(value[1], value.gr_passwd)
        self.assertIsInstance(value.gr_passwd, basestring)
        self.assertEqual(value[2], value.gr_gid)
        self.assertIsInstance(value.gr_gid, int)
        self.assertEqual(value[3], value.gr_mem)
        self.assertIsInstance(value.gr_mem, list)

    def test_values(self):
        entries = grp.getgrall()
        for e in entries:
            self.check_value(e)

        if len(entries) > 1000:
            return
        for e in entries:
            e2 = grp.getgrgid(e.gr_gid)
            self.check_value(e2)
            self.assertEqual(e2.gr_gid, e.gr_gid)
            name = e.gr_name
            if name.startswith('+') or name.startswith('-'):
                continue
            e2 = grp.getgrnam(name)
            self.check_value(e2)
            self.assertEqual(e2.gr_name.lower(), name.lower())

    def test_errors(self):
        self.assertRaises(TypeError, grp.getgrgid)
        self.assertRaises(TypeError, grp.getgrnam)
        self.assertRaises(TypeError, grp.getgrall, 42)
        bynames = {}
        bygids = {}
        for n, p, g, mem in grp.getgrall():
            if not n or n == '+':
                continue
            bynames[n] = g
            bygids[g] = n

        allnames = bynames.keys()
        namei = 0
        fakename = allnames[namei]
        while fakename in bynames:
            chars = list(fakename)
            for i in xrange(len(chars)):
                if chars[i] == 'z':
                    chars[i] = 'A'
                    break
                elif chars[i] == 'Z':
                    continue
                else:
                    chars[i] = chr(ord(chars[i]) + 1)
                    break
            else:
                namei = namei + 1
                try:
                    fakename = allnames[namei]
                except IndexError:
                    break

            fakename = ''.join(chars)

        self.assertRaises(KeyError, grp.getgrnam, fakename)
        fakegid = 4127
        while fakegid in bygids:
            fakegid = fakegid * 3 % 65536

        self.assertRaises(KeyError, grp.getgrgid, fakegid)


def test_main():
    test_support.run_unittest(GroupDatabaseTestCase)


if __name__ == '__main__':
    test_main()