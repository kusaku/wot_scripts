# Embedded file name: scripts/common/Lib/test/test_pipes.py
import pipes
import os
import string
import unittest
from test.test_support import TESTFN, run_unittest, unlink, reap_children
if os.name != 'posix':
    raise unittest.SkipTest('pipes module only works on posix')
TESTFN2 = TESTFN + '2'
s_command = 'tr %s %s' % (string.ascii_lowercase, string.ascii_uppercase)

class SimplePipeTests(unittest.TestCase):

    def tearDown(self):
        for f in (TESTFN, TESTFN2):
            unlink(f)

    def testSimplePipe1(self):
        t = pipes.Template()
        t.append(s_command, pipes.STDIN_STDOUT)
        f = t.open(TESTFN, 'w')
        f.write('hello world #1')
        f.close()
        with open(TESTFN) as f:
            self.assertEqual(f.read(), 'HELLO WORLD #1')

    def testSimplePipe2(self):
        with open(TESTFN, 'w') as f:
            f.write('hello world #2')
        t = pipes.Template()
        t.append(s_command + ' < $IN > $OUT', pipes.FILEIN_FILEOUT)
        t.copy(TESTFN, TESTFN2)
        with open(TESTFN2) as f:
            self.assertEqual(f.read(), 'HELLO WORLD #2')

    def testSimplePipe3(self):
        with open(TESTFN, 'w') as f:
            f.write('hello world #2')
        t = pipes.Template()
        t.append(s_command + ' < $IN', pipes.FILEIN_STDOUT)
        with t.open(TESTFN, 'r') as f:
            self.assertEqual(f.read(), 'HELLO WORLD #2')

    def testEmptyPipeline1(self):
        d = 'empty pipeline test COPY'
        with open(TESTFN, 'w') as f:
            f.write(d)
        with open(TESTFN2, 'w') as f:
            f.write('')
        t = pipes.Template()
        t.copy(TESTFN, TESTFN2)
        with open(TESTFN2) as f:
            self.assertEqual(f.read(), d)

    def testEmptyPipeline2(self):
        d = 'empty pipeline test READ'
        with open(TESTFN, 'w') as f:
            f.write(d)
        t = pipes.Template()
        with t.open(TESTFN, 'r') as f:
            self.assertEqual(f.read(), d)

    def testEmptyPipeline3(self):
        d = 'empty pipeline test WRITE'
        t = pipes.Template()
        with t.open(TESTFN, 'w') as f:
            f.write(d)
        with open(TESTFN) as f:
            self.assertEqual(f.read(), d)

    def testQuoting(self):
        safeunquoted = string.ascii_letters + string.digits + '@%_-+=:,./'
        unsafe = '"`$\\!'
        self.assertEqual(pipes.quote(''), "''")
        self.assertEqual(pipes.quote(safeunquoted), safeunquoted)
        self.assertEqual(pipes.quote('test file name'), "'test file name'")
        for u in unsafe:
            self.assertEqual(pipes.quote('test%sname' % u), "'test%sname'" % u)

        for u in unsafe:
            self.assertEqual(pipes.quote("test%s'name'" % u), '\'test%s\'"\'"\'name\'"\'"\'\'' % u)

    def testRepr(self):
        t = pipes.Template()
        self.assertEqual(repr(t), '<Template instance, steps=[]>')
        t.append('tr a-z A-Z', pipes.STDIN_STDOUT)
        self.assertEqual(repr(t), "<Template instance, steps=[('tr a-z A-Z', '--')]>")

    def testSetDebug(self):
        t = pipes.Template()
        t.debug(False)
        self.assertEqual(t.debugging, False)
        t.debug(True)
        self.assertEqual(t.debugging, True)

    def testReadOpenSink(self):
        t = pipes.Template()
        t.append('boguscmd', pipes.SINK)
        self.assertRaises(ValueError, t.open, 'bogusfile', 'r')

    def testWriteOpenSource(self):
        t = pipes.Template()
        t.prepend('boguscmd', pipes.SOURCE)
        self.assertRaises(ValueError, t.open, 'bogusfile', 'w')

    def testBadAppendOptions(self):
        t = pipes.Template()
        self.assertRaises(TypeError, t.append, 7, pipes.STDIN_STDOUT)
        self.assertRaises(ValueError, t.append, 'boguscmd', 'xx')
        self.assertRaises(ValueError, t.append, 'boguscmd', pipes.SOURCE)
        t = pipes.Template()
        t.append('boguscmd', pipes.SINK)
        self.assertRaises(ValueError, t.append, 'boguscmd', pipes.SINK)
        t = pipes.Template()
        self.assertRaises(ValueError, t.append, 'boguscmd $OUT', pipes.FILEIN_FILEOUT)
        t = pipes.Template()
        self.assertRaises(ValueError, t.append, 'boguscmd', pipes.FILEIN_STDOUT)
        t = pipes.Template()
        self.assertRaises(ValueError, t.append, 'boguscmd $IN', pipes.FILEIN_FILEOUT)
        t = pipes.Template()
        self.assertRaises(ValueError, t.append, 'boguscmd', pipes.STDIN_FILEOUT)

    def testBadPrependOptions(self):
        t = pipes.Template()
        self.assertRaises(TypeError, t.prepend, 7, pipes.STDIN_STDOUT)
        self.assertRaises(ValueError, t.prepend, 'tr a-z A-Z', 'xx')
        self.assertRaises(ValueError, t.prepend, 'boguscmd', pipes.SINK)
        t = pipes.Template()
        t.prepend('boguscmd', pipes.SOURCE)
        self.assertRaises(ValueError, t.prepend, 'boguscmd', pipes.SOURCE)
        t = pipes.Template()
        self.assertRaises(ValueError, t.prepend, 'boguscmd $OUT', pipes.FILEIN_FILEOUT)
        t = pipes.Template()
        self.assertRaises(ValueError, t.prepend, 'boguscmd', pipes.FILEIN_STDOUT)
        t = pipes.Template()
        self.assertRaises(ValueError, t.prepend, 'boguscmd $IN', pipes.FILEIN_FILEOUT)
        t = pipes.Template()
        self.assertRaises(ValueError, t.prepend, 'boguscmd', pipes.STDIN_FILEOUT)

    def testBadOpenMode(self):
        t = pipes.Template()
        self.assertRaises(ValueError, t.open, 'bogusfile', 'x')

    def testClone(self):
        t = pipes.Template()
        t.append('tr a-z A-Z', pipes.STDIN_STDOUT)
        u = t.clone()
        self.assertNotEqual(id(t), id(u))
        self.assertEqual(t.steps, u.steps)
        self.assertNotEqual(id(t.steps), id(u.steps))
        self.assertEqual(t.debugging, u.debugging)


def test_main():
    run_unittest(SimplePipeTests)
    reap_children()


if __name__ == '__main__':
    test_main()