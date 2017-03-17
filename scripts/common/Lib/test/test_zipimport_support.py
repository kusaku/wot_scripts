# Embedded file name: scripts/common/Lib/test/test_zipimport_support.py
import test.test_support
import os
import os.path
import sys
import textwrap
import zipfile
import zipimport
import doctest
import inspect
import linecache
import pdb
import warnings
from test.script_helper import spawn_python, kill_python, run_python, temp_dir, make_script, make_zip_script
verbose = test.test_support.verbose
from test import test_doctest, sample_doctest
from test.test_importhooks import ImportHooksBaseTestCase

def _run_object_doctest(obj, module):
    save_stdout = sys.stdout
    sys.stdout = test.test_support.get_original_stdout()
    try:
        finder = doctest.DocTestFinder(verbose=verbose, recurse=False)
        runner = doctest.DocTestRunner(verbose=verbose)
        try:
            name = '%s.%s' % (obj.__module__, obj.__name__)
        except AttributeError:
            name = module.__name__

        for example in finder.find(obj, name, module):
            runner.run(example)

        f, t = runner.failures, runner.tries
        if f:
            raise test.test_support.TestFailed('%d of %d doctests failed' % (f, t))
    finally:
        sys.stdout = save_stdout

    if verbose:
        print 'doctest (%s) ... %d tests with zero failures' % (module.__name__, t)
    return (f, t)


class ZipSupportTests(ImportHooksBaseTestCase):

    def setUp(self):
        linecache.clearcache()
        zipimport._zip_directory_cache.clear()
        ImportHooksBaseTestCase.setUp(self)

    def test_inspect_getsource_issue4223(self):
        test_src = 'def foo(): pass\n'
        with temp_dir() as d:
            init_name = make_script(d, '__init__', test_src)
            name_in_zip = os.path.join('zip_pkg', os.path.basename(init_name))
            zip_name, run_name = make_zip_script(d, 'test_zip', init_name, name_in_zip)
            os.remove(init_name)
            sys.path.insert(0, zip_name)
            import zip_pkg
            self.assertEqual(inspect.getsource(zip_pkg.foo), test_src)

    def test_doctest_issue4197(self):
        test_src = inspect.getsource(test_doctest)
        test_src = test_src.replace('from test import test_doctest', 'import test_zipped_doctest as test_doctest')
        test_src = test_src.replace('test.test_doctest', 'test_zipped_doctest')
        test_src = test_src.replace('test.sample_doctest', 'sample_zipped_doctest')
        sample_src = inspect.getsource(sample_doctest)
        sample_src = sample_src.replace('test.test_doctest', 'test_zipped_doctest')
        with temp_dir() as d:
            script_name = make_script(d, 'test_zipped_doctest', test_src)
            zip_name, run_name = make_zip_script(d, 'test_zip', script_name)
            z = zipfile.ZipFile(zip_name, 'a')
            z.writestr('sample_zipped_doctest.py', sample_src)
            z.close()
            if verbose:
                zip_file = zipfile.ZipFile(zip_name, 'r')
                print 'Contents of %r:' % zip_name
                zip_file.printdir()
                zip_file.close()
            os.remove(script_name)
            sys.path.insert(0, zip_name)
            import test_zipped_doctest
            known_good_tests = [test_zipped_doctest.SampleClass,
             test_zipped_doctest.SampleClass.NestedClass,
             test_zipped_doctest.SampleClass.NestedClass.__init__,
             test_zipped_doctest.SampleClass.__init__,
             test_zipped_doctest.SampleClass.a_classmethod,
             test_zipped_doctest.SampleClass.a_property,
             test_zipped_doctest.SampleClass.a_staticmethod,
             test_zipped_doctest.SampleClass.double,
             test_zipped_doctest.SampleClass.get,
             test_zipped_doctest.SampleNewStyleClass,
             test_zipped_doctest.SampleNewStyleClass.__init__,
             test_zipped_doctest.SampleNewStyleClass.double,
             test_zipped_doctest.SampleNewStyleClass.get,
             test_zipped_doctest.old_test1,
             test_zipped_doctest.old_test2,
             test_zipped_doctest.old_test3,
             test_zipped_doctest.old_test4,
             test_zipped_doctest.sample_func,
             test_zipped_doctest.test_DocTest,
             test_zipped_doctest.test_DocTestParser,
             test_zipped_doctest.test_DocTestRunner.basics,
             test_zipped_doctest.test_DocTestRunner.exceptions,
             test_zipped_doctest.test_DocTestRunner.option_directives,
             test_zipped_doctest.test_DocTestRunner.optionflags,
             test_zipped_doctest.test_DocTestRunner.verbose_flag,
             test_zipped_doctest.test_Example,
             test_zipped_doctest.test_debug,
             test_zipped_doctest.test_pdb_set_trace,
             test_zipped_doctest.test_pdb_set_trace_nested,
             test_zipped_doctest.test_testsource,
             test_zipped_doctest.test_trailing_space_in_test,
             test_zipped_doctest.test_DocTestSuite,
             test_zipped_doctest.test_DocTestFinder]
            fail_due_to_missing_data_files = [test_zipped_doctest.test_DocFileSuite, test_zipped_doctest.test_testfile, test_zipped_doctest.test_unittest_reportflags]
            deprecations = [('class Tester is deprecated', DeprecationWarning)]
            if sys.py3kwarning:
                deprecations += [('backquote not supported', SyntaxWarning), ('execfile.. not supported', DeprecationWarning)]
            with test.test_support.check_warnings(*deprecations):
                for obj in known_good_tests:
                    _run_object_doctest(obj, test_zipped_doctest)

    def test_doctest_main_issue4197(self):
        test_src = textwrap.dedent('                    class Test:\n                        ">>> \'line 2\'"\n                        pass\n\n                    import doctest\n                    doctest.testmod()\n                    ')
        pattern = 'File "%s", line 2, in %s'
        with temp_dir() as d:
            script_name = make_script(d, 'script', test_src)
            exit_code, data = run_python(script_name)
            expected = pattern % (script_name, '__main__.Test')
            if verbose:
                print 'Expected line', expected
                print 'Got stdout:'
                print data
            self.assertIn(expected, data)
            zip_name, run_name = make_zip_script(d, 'test_zip', script_name, '__main__.py')
            exit_code, data = run_python(zip_name)
            expected = pattern % (run_name, '__main__.Test')
            if verbose:
                print 'Expected line', expected
                print 'Got stdout:'
                print data
            self.assertIn(expected, data)

    def test_pdb_issue4201(self):
        test_src = textwrap.dedent('                    def f():\n                        pass\n\n                    import pdb\n                    pdb.runcall(f)\n                    ')
        with temp_dir() as d:
            script_name = make_script(d, 'script', test_src)
            p = spawn_python(script_name)
            p.stdin.write('l\n')
            data = kill_python(p)
            self.assertIn(script_name, data)
            zip_name, run_name = make_zip_script(d, 'test_zip', script_name, '__main__.py')
            p = spawn_python(zip_name)
            p.stdin.write('l\n')
            data = kill_python(p)
            self.assertIn(run_name, data)


def test_main():
    test.test_support.run_unittest(ZipSupportTests)
    test.test_support.reap_children()


if __name__ == '__main__':
    test_main()