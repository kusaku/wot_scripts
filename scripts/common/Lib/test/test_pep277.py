# Embedded file name: scripts/common/Lib/test/test_pep277.py
import sys, os, unittest
from unicodedata import normalize
from test import test_support
filenames = ['1_abc',
 u'2_ascii',
 u'3_Gr\xfc\xdf-Gott',
 u'4_\u0393\u03b5\u03b9\u03ac-\u03c3\u03b1\u03c2',
 u'5_\u0417\u0434\u0440\u0430\u0432\u0441\u0442\u0432\u0443\u0439\u0442\u0435',
 u'6_\u306b\u307d\u3093',
 u'7_\u05d4\u05e9\u05e7\u05e6\u05e5\u05e1',
 u'8_\u66e8\u66e9\u66eb',
 u'9_\u66e8\u05e9\u3093\u0434\u0393\xdf',
 u'10_\u1fee\u1ffd']
if sys.platform != 'darwin':
    filenames.extend([u'11_\u0385\u03d3\u03d4',
     u'12_\xa8\u0301\u03d2\u0301\u03d2\u0308',
     u'13_ \u0308\u0301\u038e\u03ab',
     u'14_\u1e9b\u1fc1\u1fcd\u1fce\u1fcf\u1fdd\u1fde\u1fdf\u1fed',
     u'15_\u1fee\u1ffd\ufad1',
     u'16_\u2000\u2000\u2000A',
     u'17_\u2001\u2001\u2001A',
     u'18_\u2003\u2003\u2003A',
     u'19_   A'])
if not os.path.supports_unicode_filenames:
    fsencoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
    try:
        for name in filenames:
            name.encode(fsencoding)

    except UnicodeEncodeError:
        raise unittest.SkipTest('only NT+ and systems with Unicode-friendly filesystem encoding')

def deltree(dirname):
    if os.path.exists(dirname):
        for fname in os.listdir(unicode(dirname)):
            os.unlink(os.path.join(dirname, fname))

        os.rmdir(dirname)


class UnicodeFileTests(unittest.TestCase):
    files = set(filenames)
    normal_form = None

    def setUp(self):
        try:
            os.mkdir(test_support.TESTFN)
        except OSError:
            pass

        files = set()
        for name in self.files:
            name = os.path.join(test_support.TESTFN, self.norm(name))
            with open(name, 'w') as f:
                f.write((name + '\n').encode('utf-8'))
            os.stat(name)
            files.add(name)

        self.files = files

    def tearDown(self):
        deltree(test_support.TESTFN)

    def norm(self, s):
        if self.normal_form and isinstance(s, unicode):
            return normalize(self.normal_form, s)
        return s

    def _apply_failure(self, fn, filename, expected_exception, check_fn_in_exception = True):
        with self.assertRaises(expected_exception) as c:
            fn(filename)
        exc_filename = c.exception.filename
        if isinstance(exc_filename, str):
            filename = filename.encode(sys.getfilesystemencoding())
        if check_fn_in_exception:
            self.assertEqual(exc_filename, filename, "Function '%s(%r) failed with bad filename in the exception: %r" % (fn.__name__, filename, exc_filename))

    def test_failures(self):
        for name in self.files:
            name = 'not_' + name
            self._apply_failure(open, name, IOError)
            self._apply_failure(os.stat, name, OSError)
            self._apply_failure(os.chdir, name, OSError)
            self._apply_failure(os.rmdir, name, OSError)
            self._apply_failure(os.remove, name, OSError)
            self._apply_failure(os.listdir, name, OSError, False)

    def test_open(self):
        for name in self.files:
            f = open(name, 'w')
            f.write((name + '\n').encode('utf-8'))
            f.close()
            os.stat(name)

    @unittest.skipIf(sys.platform == 'darwin', 'irrelevant test on Mac OS X')
    def test_normalize(self):
        files = set((f for f in self.files if isinstance(f, unicode)))
        others = set()
        for nf in set(['NFC',
         'NFD',
         'NFKC',
         'NFKD']):
            others |= set((normalize(nf, file) for file in files))

        others -= files
        for name in others:
            self._apply_failure(open, name, IOError)
            self._apply_failure(os.stat, name, OSError)
            self._apply_failure(os.chdir, name, OSError)
            self._apply_failure(os.rmdir, name, OSError)
            self._apply_failure(os.remove, name, OSError)
            self._apply_failure(os.listdir, name, OSError, False)

    @unittest.skipIf(sys.platform == 'darwin', 'irrelevant test on Mac OS X')
    def test_listdir(self):
        sf0 = set(self.files)
        f1 = os.listdir(test_support.TESTFN)
        f2 = os.listdir(unicode(test_support.TESTFN, sys.getfilesystemencoding()))
        sf2 = set((os.path.join(unicode(test_support.TESTFN), f) for f in f2))
        self.assertEqual(sf0, sf2)
        self.assertEqual(len(f1), len(f2))

    def test_rename(self):
        for name in self.files:
            os.rename(name, 'tmp')
            os.rename('tmp', name)

    def test_directory(self):
        dirname = os.path.join(test_support.TESTFN, u'Gr\xfc\xdf-\u66e8\u66e9\u66eb')
        filename = u'\xdf-\u66e8\u66e9\u66eb'
        oldwd = os.getcwd()
        os.mkdir(dirname)
        os.chdir(dirname)
        try:
            with open(filename, 'w') as f:
                f.write((filename + '\n').encode('utf-8'))
            os.access(filename, os.R_OK)
            os.remove(filename)
        finally:
            os.chdir(oldwd)
            os.rmdir(dirname)


class UnicodeNFCFileTests(UnicodeFileTests):
    normal_form = 'NFC'


class UnicodeNFDFileTests(UnicodeFileTests):
    normal_form = 'NFD'


class UnicodeNFKCFileTests(UnicodeFileTests):
    normal_form = 'NFKC'


class UnicodeNFKDFileTests(UnicodeFileTests):
    normal_form = 'NFKD'


def test_main():
    try:
        test_support.run_unittest(UnicodeFileTests, UnicodeNFCFileTests, UnicodeNFDFileTests, UnicodeNFKCFileTests, UnicodeNFKDFileTests)
    finally:
        deltree(test_support.TESTFN)


if __name__ == '__main__':
    test_main()